"""Generates AI-powered insights via Anthropic Claude API."""

import json
import pathlib
import sys
from typing import Any, Dict, List


def _config_path() -> pathlib.Path:
    # PyInstaller: sys._MEIPASS contém o diretório do executável extraído
    if getattr(sys, "frozen", False):
        base = pathlib.Path(sys._MEIPASS)
    else:
        base = pathlib.Path(__file__).parent.parent
    return base / "anthropic_config.json"


def load_api_key() -> str:
    path = _config_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("api_key", "").strip()
    return ""


def _montar_resumo(metrics: Dict[str, Any]) -> str:
    linhas = []

    evento = metrics.get("zoom_topico") or "Evento"
    linhas.append(f"Evento: {evento}")

    if metrics.get("evento_data"):
        linhas.append(f"Data: {metrics['evento_data']}")
    if metrics.get("evento_duracao"):
        linhas.append(f"Duração: {metrics['evento_duracao']}")

    linhas.append("")

    if metrics.get("total_inscritos") is not None:
        linhas.append(f"Inscritos: {metrics['total_inscritos']}")
    if metrics.get("total_presentes") is not None:
        linhas.append(f"Presentes únicos: {metrics['total_presentes']}")
    if metrics.get("taxa_presenca") is not None:
        linhas.append(f"Taxa de presença: {metrics['taxa_presenca']}%")
    if metrics.get("pico_audiencia") is not None:
        hora = f" às {metrics['hora_pico']}" if metrics.get("hora_pico") else ""
        linhas.append(f"Pico de audiência simultânea: {metrics['pico_audiencia']}{hora}")
    if metrics.get("tempo_medio_fmt"):
        linhas.append(f"Tempo médio assistido: {metrics['tempo_medio_fmt']}")
    if metrics.get("has_mensagens"):
        linhas.append(f"Mensagens enviadas: {metrics['total_mensagens']}")
    if metrics.get("has_chat"):
        linhas.append(f"Mensagens no chat: {metrics['total_chat']}")

    top = metrics.get("top_participantes", [])
    if top:
        linhas.append("")
        linhas.append("Top participantes por tempo assistido:")
        for p in top[:5]:
            linhas.append(f"  {p['nome']}: {p['minutos']} min")

    enquetes = metrics.get("enquetes", [])
    if enquetes:
        linhas.append("")
        linhas.append("Enquetes realizadas:")
        for enq in enquetes:
            linhas.append(f"  {enq['titulo']}: \"{enq['pergunta']}\" — {enq['total_respostas']} respostas")
            for label, val in zip(enq.get("labels", [])[:3], enq.get("values", [])[:3]):
                linhas.append(f"    • {label}: {val}")

    if metrics.get("has_zoom"):
        zoom = metrics.get("zoom_participantes", [])
        linhas.append("")
        linhas.append(f"Participantes no Zoom: {len(zoom)}")

    return "\n".join(linhas)


def regerar_insight(
    metrics: Dict[str, Any],
    api_key: str,
    insight_atual: Dict,
    instrucao: str,
) -> Dict:
    """
    Regera apenas um insight com base em uma instrução do usuário.
    Retorna um único dict {icon, title, body}.
    """
    import anthropic

    resumo = _montar_resumo(metrics)
    insight_json = json.dumps(insight_atual, ensure_ascii=False)

    prompt = f"""Você é um analista de dados especializado em eventos online e videoconferências corporativas.

Abaixo estão os dados de um evento e um insight gerado anteriormente que precisa ser corrigido ou melhorado.

DADOS DO EVENTO:
{resumo}

INSIGHT ATUAL:
{insight_json}

INSTRUÇÃO DO USUÁRIO:
{instrucao}

Gere um novo insight levando em conta a instrução acima.
Retorne APENAS um JSON válido com esta estrutura exata, sem texto antes ou depois:
{{"icon": "📈", "title": "Título curto", "body": "Texto do insight com dados específicos (2-3 frases)."}}

Regras:
- Emoji relevante para o tema do novo insight
- Título curto (máx 5 palavras)
- Corpo com números reais dos dados fornecidos
- Linguagem profissional em português brasileiro
"""

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


def gerar_insights_claude(metrics: Dict[str, Any], api_key: str) -> List[Dict]:
    """
    Envia resumo agregado ao Claude e retorna lista de insights.
    Retorna lista de dicts: [{icon, title, body}, ...]
    """
    import anthropic

    resumo = _montar_resumo(metrics)

    prompt = f"""Você é um analista de dados especializado em eventos online e videoconferências corporativas.

Analise os dados abaixo de um evento e gere exatamente 6 insights relevantes, perspicazes e personalizados.

DADOS DO EVENTO:
{resumo}

Retorne APENAS um JSON válido, sem texto antes ou depois, com esta estrutura exata:
[
  {{"icon": "📈", "title": "Título curto", "body": "Texto do insight com dados específicos do evento (2-3 frases)."}},
  ...
]

Regras:
- Use emojis diferentes e relevantes para cada card
- Títulos curtos (máx 5 palavras)
- Corpo com números reais dos dados fornecidos
- Insights variados: engajamento, retenção, destaque positivo, ponto de atenção, comparativo, recomendação
- Linguagem profissional em português brasileiro
- Foque em aspectos acionáveis e relevantes para o organizador do evento
"""

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    insights = json.loads(raw)
    return insights[:6]
