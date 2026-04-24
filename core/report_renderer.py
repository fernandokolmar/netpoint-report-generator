"""Renders a metrics dict into a complete self-contained HTML report string."""

import html
import json
from typing import Any, Dict, List


_CSS = """
:root {
  --blue: #0d3b6e; --teal: #1a7a8a; --light: #e8f4f8;
  --green: #2ecc71; --red: #e74c3c; --orange: #f39c12;
  --muted: #6c757d; --border: #dee2e6; --bg: #f4f7fb;
  --insight-bg: #f0f7ff;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', Arial, sans-serif; background: var(--bg); color: #1a1a2e; font-size: 12px; line-height: 1.5; }
.header { background: linear-gradient(135deg, var(--blue) 0%, var(--teal) 100%); color: #fff; padding: 20px 40px 16px; position: relative; overflow: hidden; }
.header::after { content:''; position:absolute; right:-60px; top:-60px; width:280px; height:280px; border-radius:50%; background:rgba(255,255,255,0.06); }
.header-logo { font-size:10px; letter-spacing:3px; text-transform:uppercase; opacity:.7; margin-bottom:4px; }
.header h1 { font-size:22px; font-weight:700; line-height:1.2; }
.header-sub { font-size:12px; opacity:.8; margin-top:4px; }
.header-meta { margin-top:10px; display:flex; gap:24px; flex-wrap:wrap; font-size:11px; opacity:.75; }
.header-meta span::before { content:'▸ '; }
.container { max-width:1140px; margin:0 auto; padding:0 20px 20px; }
section { margin-top:16px; }
h2 { font-size:14px; font-weight:700; color:var(--blue); border-left:4px solid var(--teal); padding-left:10px; margin-bottom:10px; }
h3 { font-size:11px; font-weight:600; color:var(--muted); margin-bottom:6px; }
.kpi-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(145px,1fr)); gap:10px; }
.kpi-card { background:#fff; border-radius:8px; padding:12px 14px; box-shadow:0 1px 4px rgba(0,0,0,.07); border-top:3px solid var(--teal); }
.kpi-card.green { border-top-color:var(--green); }
.kpi-card.orange { border-top-color:var(--orange); }
.kpi-card.red { border-top-color:var(--red); }
.kpi-value { font-size:28px; font-weight:800; color:var(--blue); }
.kpi-label { font-size:10px; color:var(--muted); margin-top:2px; text-transform:uppercase; letter-spacing:.5px; }
.kpi-sub { font-size:10px; color:var(--muted); margin-top:1px; }
.chart-card { background:#fff; border-radius:8px; padding:14px; box-shadow:0 1px 4px rgba(0,0,0,.07); margin-top:10px; }
.chart-wrap { position:relative; height:240px; }
.chart-wrap-sm { position:relative; height:200px; }
.table-card { background:#fff; border-radius:8px; padding:14px; box-shadow:0 1px 4px rgba(0,0,0,.07); overflow-x:auto; }
table { width:100%; border-collapse:collapse; font-size:10.5px; }
thead th { background:var(--blue); color:#fff; padding:7px 10px; text-align:left; font-weight:600; }
tbody tr:nth-child(even) { background:var(--light); }
tbody td { padding:5px 10px; border-bottom:1px solid var(--border); vertical-align:top; }
.enquete-block { background:#fff; border-radius:8px; padding:14px; box-shadow:0 1px 4px rgba(0,0,0,.07); margin-bottom:12px; }
.enquete-title { font-size:13px; font-weight:700; color:var(--blue); margin-bottom:2px; }
.enquete-pergunta { font-size:11px; color:#444; margin-bottom:4px; font-style:italic; }
.enquete-meta { font-size:10px; color:var(--muted); margin-bottom:8px; }
.insights-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:12px; }
.insight-card { background:var(--insight-bg); border-radius:8px; padding:14px 16px; box-shadow:0 1px 4px rgba(0,0,0,.07); border-left:4px solid var(--teal); }
.insight-icon { font-size:22px; margin-bottom:6px; }
.insight-title { font-size:12px; font-weight:700; color:var(--blue); margin-bottom:4px; }
.insight-body { font-size:11px; color:#333; line-height:1.5; }
.ai-badge { display:inline-block; font-size:9px; letter-spacing:.5px; text-transform:uppercase; background:var(--teal); color:#fff; border-radius:3px; padding:1px 5px; margin-left:8px; vertical-align:middle; }
.footer { text-align:center; font-size:10px; color:var(--muted); margin-top:16px; padding-top:10px; border-top:1px solid var(--border); }
@media print {
  body { background:#fff; }
  .header { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .kpi-card, .chart-card, .table-card, .enquete-block { break-inside:avoid; box-shadow:none; border:1px solid var(--border); }
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


def _table(headers: List[str], rows: List[List[Any]]) -> str:
    th = ''.join(f'<th>{_e(h)}</th>' for h in headers)
    trs = ''
    for row in rows:
        trs += '<tr>' + ''.join(f'<td>{_e(c)}</td>' for c in row) + '</tr>'
    return f'<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


def render_html(metrics: Dict[str, Any], insights: List[Dict] = None) -> str:
    """Takes a metrics dict from report_engine and returns a full HTML string."""
    evento_nome = metrics.get('zoom_topico') or 'Evento'
    evento_data = metrics.get('evento_data', '')
    evento_duracao = metrics.get('evento_duracao', '')
    data_emissao = metrics.get('data_emissao', '')

    header_sub_parts = []
    if evento_data:
        header_sub_parts.append(evento_data)
    if evento_duracao:
        header_sub_parts.append(evento_duracao)

    header_meta_parts = []
    if evento_data:
        header_meta_parts.append(f'<span>Data: {_e(evento_data)}</span>')
    if evento_duracao:
        header_meta_parts.append(f'<span>Duração: {_e(evento_duracao)}</span>')
    header_meta_parts.append(f'<span>Emitido em: {_e(data_emissao)}</span>')
    header_meta_parts.append('<span>Netpoint</span>')

    sections = []

    # --- KPIs executivos ---
    kpi_cards = []
    if metrics.get('has_inscritos') and metrics.get('total_inscritos') is not None:
        kpi_cards.append(_kpi(metrics['total_inscritos'], 'Inscritos'))
    if metrics.get('total_presentes') is not None:
        kpi_cards.append(_kpi(metrics['total_presentes'], 'Presentes únicos'))
    if metrics.get('taxa_presenca') is not None:
        taxa = metrics['taxa_presenca']
        color = 'green' if taxa >= 70 else ('orange' if taxa >= 40 else 'red')
        kpi_cards.append(_kpi(f'{taxa}%', 'Taxa de presença', '', color))
    if metrics.get('pico_audiencia') is not None:
        kpi_cards.append(_kpi(metrics['pico_audiencia'], 'Pico de audiência', 'simultâneos'))
    if metrics.get('hora_pico'):
        kpi_cards.append(_kpi(metrics['hora_pico'], 'Hora do pico'))
    if metrics.get('tempo_medio_fmt'):
        kpi_cards.append(_kpi(metrics['tempo_medio_fmt'], 'Tempo médio assistido'))

    if kpi_cards:
        sections.append(
            '<section>'
            '<h2>KPIs Executivos</h2>'
            '<div class="kpi-grid">' + ''.join(kpi_cards) + '</div>'
            '</section>'
        )

    # --- Retenção ---
    rlabels = metrics.get('retencao_labels', [])
    rvalues = metrics.get('retencao_values', [])
    if rlabels and rvalues:
        sections.append(
            '<section>'
            '<h2>Retenção de Audiência</h2>'
            '<div class="chart-card">'
            '<div class="chart-wrap"><canvas id="chartRetencao"></canvas></div>'
            '</div>'
            '</section>'
        )

    # --- Top participantes ---
    top = metrics.get('top_participantes', [])
    if top:
        rows = [[p['nome'], p['minutos']] for p in top]
        sections.append(
            '<section>'
            '<h2>Top Participantes por Tempo Assistido</h2>'
            '<div class="table-card">'
            + _table(['Nome', 'Minutos'], rows) +
            '</div>'
            '</section>'
        )

    # --- Engajamento ---
    eng_cards = []
    if metrics.get('has_mensagens'):
        eng_cards.append(_kpi(metrics['total_mensagens'], 'Mensagens enviadas'))
    if metrics.get('has_chat'):
        eng_cards.append(_kpi(metrics['total_chat'], 'Mensagens no chat'))
    if eng_cards:
        sections.append(
            '<section>'
            '<h2>Engajamento</h2>'
            '<div class="kpi-grid">' + ''.join(eng_cards) + '</div>'
            '</section>'
        )

    # --- Enquetes ---
    if metrics.get('has_enquetes'):
        enq_html = ''
        for i, enq in enumerate(metrics.get('enquetes', [])):
            canvas_id = f'chartEnquete{i}'
            enq_html += (
                f'<div class="enquete-block">'
                f'<div class="enquete-title">{_e(enq["titulo"])}</div>'
            )
            if enq.get('pergunta'):
                enq_html += f'<div class="enquete-pergunta">{_e(enq["pergunta"])}</div>'
            enq_html += f'<div class="enquete-meta">{_e(enq["total_respostas"])} respostas</div>'
            if enq.get('labels'):
                enq_html += f'<div class="chart-wrap-sm"><canvas id="{canvas_id}"></canvas></div>'
            enq_html += '</div>'

        sections.append(
            '<section>'
            '<h2>Enquetes</h2>'
            + enq_html +
            '</section>'
        )

    # --- Insights IA ---
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
            '<h2>Insights <span class="ai-badge">IA</span></h2>'
            '<div class="insights-grid">' + cards_html + '</div>'
            '</section>'
        )

    # --- Presença Zoom ---
    if metrics.get('has_zoom'):
        zoom_rows = [
            [p['nome'], p['email'], p['permanencia']]
            for p in metrics.get('zoom_participantes', [])
        ]
        sections.append(
            '<section>'
            '<h2>Presença no Zoom</h2>'
            '<div class="table-card">'
            + _table(['Nome', 'E-mail', 'Permanência (min)'], zoom_rows) +
            '</div>'
            '</section>'
        )

    # --- Script Chart.js ---
    script_lines = [
        "Chart.defaults.font.family = \"'Segoe UI', Arial, sans-serif\";",
        "Chart.defaults.font.size = 11;",
    ]

    if rlabels and rvalues:
        script_lines.append(
            f"new Chart(document.getElementById('chartRetencao'), {{"
            f"type:'line',"
            f"data:{{"
            f"labels:{json.dumps(rlabels, ensure_ascii=False)},"
            f"datasets:[{{data:{json.dumps(rvalues)},borderColor:'#1a7a8a',backgroundColor:'rgba(26,122,138,0.1)',tension:0.3,fill:true,pointRadius:0,borderWidth:2}}]"
            f"}},"
            f"options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{maxTicksLimit:12}}}}}}}}"
            f"}});"
        )

    if metrics.get('has_enquetes'):
        for i, enq in enumerate(metrics.get('enquetes', [])):
            if not enq.get('labels'):
                continue
            canvas_id = f'chartEnquete{i}'
            colors = [
                '#0d3b6e','#1a7a8a','#2ecc71','#f39c12','#e74c3c',
                '#9b59b6','#e67e22','#1abc9c','#3498db','#e91e63',
            ]
            bg = json.dumps(colors[:len(enq['labels'])])
            script_lines.append(
                f"new Chart(document.getElementById('{canvas_id}'), {{"
                f"type:'bar',"
                f"data:{{"
                f"labels:{json.dumps(enq['labels'], ensure_ascii=False)},"
                f"datasets:[{{data:{json.dumps(enq['values'])},backgroundColor:{bg},borderRadius:4}}]"
                f"}},"
                f"options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}}}}"
                f"}});"
            )

    script_block = '<script>\n' + '\n'.join(script_lines) + '\n</script>'

    body = '\n'.join(sections)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Relatório Inteligente — {_e(evento_nome)}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>{_CSS}</style>
</head>
<body>
<div class="header">
  <div class="header-logo">Netpoint — Relatório Inteligente</div>
  <h1>{_e(evento_nome)}</h1>
  <div class="header-sub">{_e(' · '.join(header_sub_parts))}</div>
  <div class="header-meta">{''.join(header_meta_parts)}</div>
</div>
<div class="container">
{body}
  <div class="footer"><p>Relatório gerado em {_e(data_emissao)} · Netpoint</p></div>
</div>
{script_block}
</body>
</html>"""
