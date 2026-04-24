"""Generates AI-powered insights via configurable AI provider (.env)."""

import json
import pathlib
import sys
from typing import Any, Dict, List, Optional, Tuple


def _project_root() -> pathlib.Path:
    if getattr(sys, "frozen", False):
        return pathlib.Path(sys._MEIPASS)
    return pathlib.Path(__file__).parent.parent


def _load_env() -> Dict[str, str]:
    """Lê o arquivo .env da raiz do projeto. Ignora linhas de comentário."""
    env_path = _project_root() / ".env"
    values = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, val = line.partition("=")
                values[key.strip()] = val.strip()
    return values


def load_ai_config() -> Dict[str, str]:
    """
    Retorna as configurações da IA lidas do .env.
    Fallback para anthropic_config.json legado se .env não existir.
    """
    env = _load_env()

    api_key  = env.get("AI_API_KEY", "")
    base_url = env.get("AI_BASE_URL", "https://api.anthropic.com")
    model    = env.get("AI_MODEL",    "claude-sonnet-4-6")
    provider = env.get("AI_PROVIDER", "anthropic").lower()

    # Fallback para anthropic_config.json legado
    if not api_key:
        legacy = _project_root() / "anthropic_config.json"
        if legacy.exists():
            with open(legacy, "r", encoding="utf-8") as f:
                api_key = json.load(f).get("api_key", "").strip()
            provider = "anthropic"
            base_url = "https://api.anthropic.com"
            model    = "claude-sonnet-4-6"

    return {
        "api_key":  api_key,
        "base_url": base_url,
        "model":    model,
        "provider": provider,
    }


def load_api_key() -> str:
    """Compatibilidade com código existente — retorna apenas a api_key."""
    return load_ai_config().get("api_key", "")


def _call_ai(prompt: str, config: Dict[str, str], max_tokens: int) -> str:
    """
    Chama a API conforme o provider configurado.
    - anthropic: usa o SDK oficial da Anthropic
    - openai:    usa o SDK OpenAI com base_url customizável (Groq, OpenRouter, etc.)
    Retorna o texto da resposta.
    """
    provider = config.get("provider", "anthropic")
    api_key  = config["api_key"]
    model    = config["model"]
    base_url = config["base_url"]

    if provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()

    else:
        # Compatível com OpenAI, Groq, OpenRouter e qualquer API OpenAI-like
        import openai
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()


def _parse_json(raw: str) -> Any:
    """Remove blocos ```json``` e faz parse do JSON."""
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


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
    config = load_ai_config()
    if api_key:
        config["api_key"] = api_key

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

    raw = _call_ai(prompt, config, max_tokens=512)
    return _parse_json(raw)


def gerar_insights_claude(metrics: Dict[str, Any], api_key: str) -> List[Dict]:
    """
    Envia resumo agregado à IA configurada e retorna lista de insights.
    Retorna lista de dicts: [{icon, title, body}, ...]
    """
    config = load_ai_config()
    if api_key:
        config["api_key"] = api_key

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

    raw = _call_ai(prompt, config, max_tokens=1024)
    insights = _parse_json(raw)
    return insights[:6]
