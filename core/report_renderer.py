"""Renders a metrics dict into a complete self-contained HTML report string."""

import base64
import html
import json
import pathlib
import sys
from typing import Any, Dict, List


def _load_logo_base64(filename: str) -> str:
    if getattr(sys, "frozen", False):
        base = pathlib.Path(sys._MEIPASS)
    else:
        base = pathlib.Path(__file__).parent.parent
    path = base / "visual" / filename
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


_CSS = """
:root {
  --np-blue: #3db3f5;
  --np-purple: #9b59f5;
  --np-dark: #2c2c3e;
  --np-grad: linear-gradient(135deg, #3db3f5 0%, #7b4ff5 50%, #9b59f5 100%);
  --np-grad-light: linear-gradient(135deg, rgba(61,179,245,0.06) 0%, rgba(155,89,245,0.06) 100%);
  --green: #27ae60; --red: #e74c3c; --orange: #f39c12;
  --muted: #6c757d; --border: #e0e0f0; --bg: #f5f5fb;
  --card-bg: #ffffff; --text: #1e1e2e;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; background: var(--bg); color: var(--text); font-size: 12px; line-height: 1.5; }

/* ── HEADER ── */
.header { background: var(--np-grad); color: #fff; padding: 28px 40px 22px; position: relative; overflow: hidden; }
.header::before { content:''; position:absolute; right:-80px; top:-80px; width:320px; height:320px; border-radius:50%; background:rgba(255,255,255,0.07); }
.header::after  { content:''; position:absolute; right:60px; bottom:-100px; width:220px; height:220px; border-radius:50%; background:rgba(255,255,255,0.04); }
.header-brand { display:flex; align-items:center; gap:10px; margin-bottom:16px; }
.header-icon { width:36px; height:36px; opacity:.92; }
.header-brand-name { font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; opacity:.85; }
.header h1 { font-size:26px; font-weight:800; line-height:1.2; letter-spacing:-.3px; }
.header-sub { font-size:12px; opacity:.75; margin-top:6px; }
.header-meta { margin-top:16px; display:flex; gap:10px; flex-wrap:wrap; font-size:10.5px; opacity:.8; }
.header-meta span { background:rgba(255,255,255,0.15); border-radius:4px; padding:3px 10px; }

/* ── VISÃO GERAL ── */
.overview-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px; }
.overview-card { background:var(--card-bg); border-radius:10px; padding:14px 18px; box-shadow:0 2px 8px rgba(100,80,200,.08); display:flex; flex-direction:column; gap:2px; }
.overview-label { font-size:9.5px; color:var(--muted); text-transform:uppercase; letter-spacing:.6px; }
.overview-value { font-size:15px; font-weight:700; color:var(--np-dark); }
.overview-value.accent { background:var(--np-grad); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-size:17px; }

/* ── LAYOUT ── */
.container { max-width:1140px; margin:0 auto; padding:0 24px 28px; }
section { margin-top:22px; }
h2 { font-size:13px; font-weight:700; color:var(--np-dark); border-left:4px solid var(--np-purple); padding-left:10px; margin-bottom:14px; }

/* ── KPI CARDS ── */
.kpi-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(148px,1fr)); gap:10px; }
.kpi-card { background:var(--card-bg); border-radius:10px; padding:14px 16px; box-shadow:0 2px 8px rgba(100,80,200,.08); border-top:3px solid var(--np-blue); }
.kpi-card.green  { border-top-color:var(--green); }
.kpi-card.orange { border-top-color:var(--orange); }
.kpi-card.red    { border-top-color:var(--red); }
.kpi-value { font-size:28px; font-weight:800; background:var(--np-grad); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.kpi-card.green  .kpi-value { background:none; -webkit-text-fill-color:var(--green); }
.kpi-card.orange .kpi-value { background:none; -webkit-text-fill-color:var(--orange); }
.kpi-card.red    .kpi-value { background:none; -webkit-text-fill-color:var(--red); }
.kpi-label { font-size:10px; color:var(--muted); margin-top:3px; text-transform:uppercase; letter-spacing:.5px; }
.kpi-sub { font-size:10px; color:var(--muted); margin-top:1px; }

/* ── CHART / TABLE CARDS ── */
.chart-card { background:var(--card-bg); border-radius:10px; padding:16px; box-shadow:0 2px 8px rgba(100,80,200,.08); margin-top:10px; }
.chart-hint { font-size:10px; color:var(--muted); margin-top:8px; text-align:center; opacity:.7; }
.chart-wrap { position:relative; height:240px; }
.chart-wrap-sm { position:relative; height:180px; }
.table-card { background:var(--card-bg); border-radius:10px; padding:0; box-shadow:0 2px 8px rgba(100,80,200,.08); overflow:hidden; }
.table-scroll { overflow-x:auto; max-height:420px; overflow-y:auto; }
table { width:100%; border-collapse:collapse; font-size:10.5px; }
thead th { background:var(--np-grad); color:#fff; padding:9px 14px; text-align:left; font-weight:600; position:sticky; top:0; }
tbody tr:nth-child(even) { background:var(--np-grad-light); }
tbody tr:hover { background:rgba(61,179,245,0.1); }
tbody td { padding:7px 14px; border-bottom:1px solid var(--border); vertical-align:middle; }
.rank { font-weight:700; color:var(--np-purple); width:32px; }
.badge { display:inline-block; padding:1px 7px; border-radius:10px; font-size:9.5px; font-weight:600; }
.badge-green  { background:#e8f8f0; color:#27ae60; }
.badge-orange { background:#fef5e7; color:#f39c12; }
.badge-red    { background:#fdecea; color:#e74c3c; }

/* ── ENQUETES ── */
.enquete-block { background:var(--card-bg); border-radius:10px; padding:16px; box-shadow:0 2px 8px rgba(100,80,200,.08); margin-bottom:12px; }
.enquete-title { font-size:13px; font-weight:700; color:var(--np-dark); margin-bottom:2px; }
.enquete-pergunta { font-size:11px; color:#444; margin-bottom:4px; font-style:italic; }
.enquete-meta { font-size:10px; color:var(--muted); margin-bottom:10px; }

/* ── INSIGHTS IA ── */
.insights-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; }
.insight-card { background:var(--card-bg); border-radius:10px; padding:18px 20px; box-shadow:0 2px 8px rgba(100,80,200,.08); border-left:4px solid var(--np-purple); position:relative; overflow:hidden; }
.insight-card::after { content:''; position:absolute; right:-20px; bottom:-20px; width:80px; height:80px; border-radius:50%; background:var(--np-grad-light); }
.insight-icon { font-size:26px; margin-bottom:10px; }
.insight-title { font-size:12px; font-weight:700; color:var(--np-dark); margin-bottom:6px; }
.insight-body { font-size:11px; color:#444; line-height:1.6; }
.ai-badge { display:inline-block; font-size:9px; letter-spacing:.8px; text-transform:uppercase; background:var(--np-grad); color:#fff; border-radius:4px; padding:2px 7px; margin-left:8px; vertical-align:middle; }

/* ── FOOTER ── */
.footer { text-align:center; font-size:10px; color:var(--muted); margin-top:24px; padding-top:14px; border-top:1px solid var(--border); }
.footer-brand { display:inline-flex; align-items:center; gap:6px; margin-top:5px; opacity:.55; }
.footer-icon { height:16px; }

/* ── DIVIDER ── */
.divider { border:none; border-top:1px solid var(--border); margin:6px 0 14px; }

@media print {
  body { background:#fff; font-size:11px; }
  .header { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .kpi-card, .chart-card, .table-card, .enquete-block, .insight-card, .overview-card { break-inside:avoid; box-shadow:none; border:1px solid var(--border); }
  .kpi-value { -webkit-text-fill-color:var(--np-blue) !important; }
  .overview-value.accent { -webkit-text-fill-color:var(--np-purple) !important; }
  .table-scroll { max-height:none; overflow:visible; }
  thead th { background:var(--np-dark) !important; }
}
"""


def _e(value: Any) -> str:
    return html.escape(str(value) if value is not None else '')


def _kpi(value: Any, label: str, sub: str = '', color: str = '') -> str:
    cls = f'kpi-card {color}' if color else 'kpi-card'
    sub_html = f'<div class="kpi-sub">{_e(sub)}</div>' if sub else ''
    return (
        f'<div class="{cls}">'
        f'<div class="kpi-value">{_e(value)}</div>'
        f'<div class="kpi-label">{_e(label)}</div>'
        f'{sub_html}'
        f'</div>'
    )


def _overview_item(label: str, value: Any, accent: bool = False) -> str:
    cls = 'overview-value accent' if accent else 'overview-value'
    return (
        f'<div class="overview-card">'
        f'<div class="overview-label">{_e(label)}</div>'
        f'<div class="{cls}">{_e(value)}</div>'
        f'</div>'
    )


def _table(headers: List[str], rows: List[List[Any]], ranked: bool = False) -> str:
    th = ''.join(f'<th>{_e(h)}</th>' for h in headers)
    trs = ''
    for i, row in enumerate(rows):
        rank_cell = f'<td class="rank">#{i+1}</td>' if ranked else ''
        cells = ''.join(f'<td>{_e(c)}</td>' for c in row)
        trs += f'<tr>{rank_cell}{cells}</tr>'
    return f'<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


def render_html(metrics: Dict[str, Any], insights: List[Dict] = None) -> str:
    """Takes a metrics dict from report_engine and returns a full HTML string."""
    icon_b64 = _load_logo_base64("netpoint_logo.jpg")
    logo_b64 = _load_logo_base64("logo-netpoint-gray.png")
    icon_src = f"data:image/jpeg;base64,{icon_b64}" if icon_b64 else ""
    logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""

    evento_nome = metrics.get('zoom_topico') or 'Evento'
    evento_data = metrics.get('evento_data', '')
    evento_hora_inicio = metrics.get('evento_hora_inicio', '')
    evento_hora_fim = metrics.get('evento_hora_fim', '')
    evento_duracao_fmt = metrics.get('evento_duracao_fmt', '') or metrics.get('evento_duracao', '')
    zoom_host = metrics.get('zoom_host', '')
    data_emissao = metrics.get('data_emissao', '')

    # ── Cabeçalho ──────────────────────────────────────────────────────────
    header_sub_parts = []
    if evento_data:
        horario = f'{evento_hora_inicio} – {evento_hora_fim}' if evento_hora_inicio and evento_hora_fim else evento_hora_inicio
        header_sub_parts.append(evento_data + (f'  ·  {horario}' if horario else ''))
    if evento_duracao_fmt:
        header_sub_parts.append(f'Duração: {evento_duracao_fmt}')

    header_meta_parts = []
    if evento_data:
        header_meta_parts.append(f'<span>📅 {_e(evento_data)}</span>')
    if evento_hora_inicio:
        horario = f'{evento_hora_inicio} – {evento_hora_fim}' if evento_hora_fim else evento_hora_inicio
        header_meta_parts.append(f'<span>🕐 {_e(horario)}</span>')
    if evento_duracao_fmt:
        header_meta_parts.append(f'<span>⏱ {_e(evento_duracao_fmt)}</span>')
    header_meta_parts.append(f'<span>📄 Emitido em {_e(data_emissao)}</span>')

    sections = []

    # ── 1. Visão Geral do Evento ─────────────────────────────────────────
    overview_items = []
    if evento_data:
        overview_items.append(_overview_item('Data do evento', evento_data))
    if evento_hora_inicio:
        horario = f'{evento_hora_inicio} – {evento_hora_fim}' if evento_hora_fim else evento_hora_inicio
        overview_items.append(_overview_item('Horário', horario))
    if evento_duracao_fmt:
        overview_items.append(_overview_item('Duração total', evento_duracao_fmt, accent=True))
    if data_emissao:
        overview_items.append(_overview_item('Relatório emitido em', data_emissao))

    if overview_items:
        sections.append(
            '<section>'
            '<h2>Visão Geral do Evento</h2>'
            '<div class="overview-grid">' + ''.join(overview_items) + '</div>'
            '</section>'
        )

    # ── 2. KPIs Executivos ───────────────────────────────────────────────
    kpi_cards = []
    if metrics.get('has_inscritos') and metrics.get('total_inscritos') is not None:
        kpi_cards.append(_kpi(metrics['total_inscritos'], 'Inscritos'))
    if metrics.get('total_presentes') is not None:
        kpi_cards.append(_kpi(metrics['total_presentes'], 'Presentes únicos'))
    if metrics.get('total_ausentes') is not None and metrics.get('has_inscritos'):
        kpi_cards.append(_kpi(metrics['total_ausentes'], 'Ausentes'))
    if metrics.get('taxa_presenca') is not None:
        taxa = metrics['taxa_presenca']
        color = 'green' if taxa >= 70 else ('orange' if taxa >= 40 else 'red')
        kpi_cards.append(_kpi(f'{taxa}%', 'Taxa de presença', '', color))
    if metrics.get('pico_audiencia') is not None:
        sub = f'às {metrics["hora_pico"]}' if metrics.get('hora_pico') else 'simultâneos'
        kpi_cards.append(_kpi(metrics['pico_audiencia'], 'Pico de audiência', sub))
    if metrics.get('tempo_medio_fmt'):
        kpi_cards.append(_kpi(metrics['tempo_medio_fmt'], 'Tempo médio assistido'))
    if metrics.get('total_interacoes'):
        kpi_cards.append(_kpi(metrics['total_interacoes'], 'Total de interações', 'mensagens + chat'))

    if kpi_cards:
        sections.append(
            '<section>'
            '<h2>Indicadores do Evento</h2>'
            '<div class="kpi-grid">' + ''.join(kpi_cards) + '</div>'
            '</section>'
        )

    # ── 3. Retenção de Audiência ─────────────────────────────────────────
    rlabels = metrics.get('retencao_labels', [])
    rvalues = metrics.get('retencao_values', [])
    if rlabels and rvalues:
        sections.append(
            '<section>'
            '<h2>Retenção de Audiência ao Longo do Evento</h2>'
            '<div class="chart-card">'
            '<div class="chart-wrap"><canvas id="chartRetencao"></canvas></div>'
            '<p class="chart-hint">💡 Passe o mouse sobre o gráfico para ver o número de usuários em cada momento</p>'
            '</div>'
            '</section>'
        )

    # ── 4. Insights IA ───────────────────────────────────────────────────
    if insights:
        cards_html = ''
        for ins in insights:
            cards_html += (
                f'<div class="insight-card">'
                f'<div class="insight-icon">{_e(ins.get("icon", "💡"))}</div>'
                f'<div class="insight-title">{_e(ins.get("title", ""))}</div>'
                f'<div class="insight-body">{_e(ins.get("body", ""))}</div>'
                f'</div>'
            )
        sections.append(
            '<section>'
            '<h2>Análise <span class="ai-badge">IA</span></h2>'
            '<div class="insights-grid">' + cards_html + '</div>'
            '</section>'
        )

    # ── 5. Engajamento ───────────────────────────────────────────────────
    eng_cards = []
    if metrics.get('has_mensagens'):
        eng_cards.append(_kpi(metrics['total_mensagens'], 'Mensagens enviadas'))
    if metrics.get('has_chat'):
        eng_cards.append(_kpi(metrics['total_chat'], 'Mensagens no chat'))
    if eng_cards:
        sections.append(
            '<section>'
            '<h2>Engajamento — Participação Ativa</h2>'
            '<div class="kpi-grid">' + ''.join(eng_cards) + '</div>'
            '</section>'
        )

    # ── 6. Enquetes ──────────────────────────────────────────────────────
    if metrics.get('has_enquetes'):
        enq_html = ''
        for i, enq in enumerate(metrics.get('enquetes', [])):
            canvas_id = f'chartEnquete{i}'
            enq_html += (
                f'<div class="enquete-block">'
                f'<div class="enquete-title">{_e(enq["titulo"])}</div>'
            )
            if enq.get('pergunta'):
                enq_html += f'<div class="enquete-pergunta">"{_e(enq["pergunta"])}"</div>'
            enq_html += f'<div class="enquete-meta">{_e(enq["total_respostas"])} respostas recebidas</div>'
            if enq.get('labels'):
                enq_html += f'<div class="chart-wrap-sm"><canvas id="{canvas_id}"></canvas></div>'
            enq_html += '</div>'

        sections.append(
            '<section>'
            '<h2>Enquetes Realizadas</h2>'
            + enq_html +
            '</section>'
        )

    # ── 7. Lista completa de participantes ───────────────────────────────
    todos = metrics.get('todos_participantes', [])
    if todos:
        rows = [[p['nome'], f"{p['minutos']} min"] for p in todos]
        sections.append(
            '<section>'
            f'<h2>Lista de Participantes <span style="font-size:11px;font-weight:400;color:var(--muted)">({len(todos)} presentes)</span></h2>'
            '<div class="table-card">'
            '<div class="table-scroll">'
            + _table(['#', 'Nome', 'Tempo assistido'], rows, ranked=True) +
            '</div>'
            '</div>'
            '</section>'
        )

    # ── 8. Presença no Zoom ──────────────────────────────────────────────
    if metrics.get('has_zoom'):
        zoom_rows = [
            [p['nome'], p['email'], f"{p['permanencia']} min"]
            for p in metrics.get('zoom_participantes', [])
        ]
        sections.append(
            '<section>'
            f'<h2>Participantes no Zoom <span style="font-size:11px;font-weight:400;color:var(--muted)">({len(zoom_rows)} registros)</span></h2>'
            '<div class="table-card">'
            '<div class="table-scroll">'
            + _table(['Nome', 'E-mail', 'Permanência'], zoom_rows) +
            '</div>'
            '</div>'
            '</section>'
        )

    # ── Script Chart.js ──────────────────────────────────────────────────
    script_lines = [
        "Chart.defaults.font.family = \"'Inter', 'Segoe UI', Arial, sans-serif\";",
        "Chart.defaults.font.size = 11;",
    ]

    if rlabels and rvalues:
        pico_idx = rvalues.index(max(rvalues)) if rvalues else 0
        # Pico: sempre visível em laranja. Demais: invisíveis em repouso,
        # aparecem com bolinha branca ao hover (hitRadius alto facilita encontrar)
        point_radii = [0] * len(rvalues)
        point_radii[pico_idx] = 7
        point_hover_radii = [6] * len(rvalues)
        point_hover_radii[pico_idx] = 9
        point_colors = ['rgba(0,0,0,0)'] * len(rvalues)
        point_colors[pico_idx] = '#f39c12'
        point_hover_colors = ['rgba(255,255,255,0.95)'] * len(rvalues)
        point_hover_colors[pico_idx] = '#f39c12'
        point_border_colors = ['rgba(0,0,0,0)'] * len(rvalues)
        point_border_colors[pico_idx] = '#ffffff'
        point_hover_border_colors = ['#7b4ff5'] * len(rvalues)
        point_hover_border_colors[pico_idx] = '#ffffff'
        script_lines.append(f"""
(function(){{
  var picoIdx = {pico_idx};
  new Chart(document.getElementById('chartRetencao'), {{
    type: 'line',
    data: {{
      labels: {json.dumps(rlabels, ensure_ascii=False)},
      datasets: [{{
        data: {json.dumps(rvalues)},
        borderColor: '#7b4ff5',
        backgroundColor: 'rgba(123,79,245,0.08)',
        tension: 0.4,
        fill: true,
        pointRadius: {json.dumps(point_radii)},
        pointHoverRadius: {json.dumps(point_hover_radii)},
        pointHitRadius: 20,
        pointBackgroundColor: {json.dumps(point_colors)},
        pointHoverBackgroundColor: {json.dumps(point_hover_colors)},
        pointBorderColor: {json.dumps(point_border_colors)},
        pointHoverBorderColor: {json.dumps(point_hover_border_colors)},
        pointBorderWidth: 2,
        pointHoverBorderWidth: 2,
        borderWidth: 2.5
      }}]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          mode: 'index',
          intersect: false,
          callbacks: {{
            label: function(c) {{
              var suffix = c.dataIndex === picoIdx ? ' ★ Pico' : '';
              return c.parsed.y + ' usuários' + suffix;
            }}
          }}
        }}
      }},
      scales: {{
        x: {{ ticks: {{ maxTicksLimit: 12, color: '#888' }}, grid: {{ display: false }} }},
        y: {{ ticks: {{ color: '#888' }}, grid: {{ color: 'rgba(0,0,0,0.05)' }} }}
      }}
    }}
  }});
}})();
""")

    if metrics.get('has_enquetes'):
        colors = ['#3db3f5','#9b59f5','#27ae60','#f39c12','#e74c3c',
                  '#7b4ff5','#e67e22','#1abc9c','#3498db','#e91e63']
        for i, enq in enumerate(metrics.get('enquetes', [])):
            if not enq.get('labels'):
                continue
            canvas_id = f'chartEnquete{i}'
            bg = json.dumps(colors[:len(enq['labels'])])
            script_lines.append(
                f"new Chart(document.getElementById('{canvas_id}'), {{"
                f"type:'bar',"
                f"data:{{"
                f"labels:{json.dumps(enq['labels'], ensure_ascii=False)},"
                f"datasets:[{{data:{json.dumps(enq['values'])},backgroundColor:{bg},borderRadius:5}}]"
                f"}},"
                f"options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,"
                f"plugins:{{legend:{{display:false}}}},"
                f"scales:{{x:{{ticks:{{color:'#888'}},grid:{{color:'rgba(0,0,0,0.05)'}}}},"
                f"y:{{ticks:{{color:'#555'}},grid:{{display:false}}}}}}}}"
                f"}});"
            )

    script_block = '<script>\n' + '\n'.join(script_lines) + '\n</script>'
    body = '\n'.join(sections)
    icon_tag = f'<img class="header-icon" src="{icon_src}" alt="Netpoint"/>' if icon_src else ''
    logo_tag = f'<img class="footer-icon" src="{logo_src}" alt="Netpoint"/>' if logo_src else ''

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Relatório — {_e(evento_nome)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet"/>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>{_CSS}</style>
</head>
<body>
<div class="header">
  <div class="header-brand">
    {icon_tag}
    <span class="header-brand-name">Netpoint &nbsp;·&nbsp; Relatório de Evento</span>
  </div>
  <h1>{_e(evento_nome)}</h1>
  <div class="header-sub">{_e('  ·  '.join(header_sub_parts))}</div>
  <div class="header-meta">{''.join(header_meta_parts)}</div>
</div>
<div class="container">
{body}
  <div class="footer">
    <p>Documento gerado em {_e(data_emissao)} · Uso interno e para o cliente · Confidencial</p>
    <div class="footer-brand">{logo_tag}</div>
  </div>
</div>
{script_block}
</body>
</html>"""
