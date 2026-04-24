"""Computes metrics from processed DataFrames for the Relatório Inteligente."""

from datetime import date
from typing import Any, Dict, List, Optional

import pandas as pd


def compute_metrics(processed: Dict[str, Any]) -> Dict[str, Any]:
    """Takes processed_dataframes dict and returns a metrics dict for the renderer."""
    today = date.today().strftime('%d/%m/%Y')

    relatorio: Optional[pd.DataFrame] = processed.get('relatorio_processed')
    inscritos: Optional[pd.DataFrame] = processed.get('inscritos_processed')
    totalizado: Optional[pd.DataFrame] = processed.get('totalizado_processed')
    mensagens: Optional[pd.DataFrame] = processed.get('mensagens_processed')
    chat: Optional[pd.DataFrame] = processed.get('chat_processed')
    zoom_consol: Optional[pd.DataFrame] = processed.get('presenca_zoom_consolidado')
    zoom_meta: Dict = processed.get('presenca_zoom_meta') or {}

    # --- Dados temporais do evento ---
    evento_data = ''
    evento_hora_inicio = ''
    evento_hora_fim = ''
    evento_duracao = ''
    evento_duracao_fmt = ''
    retencao_labels: List[str] = []
    retencao_values: List[int] = []
    pico_audiencia: Optional[int] = None
    hora_pico: Optional[str] = None

    if totalizado is not None and not totalizado.empty:
        col_data = 'Data'
        col_usu = 'Usuarios conectados'
        if col_data in totalizado.columns:
            datas = pd.to_datetime(totalizado[col_data], errors='coerce').dropna()
            if not datas.empty:
                dt_inicio = datas.min()
                dt_fim = datas.max()
                evento_data = dt_inicio.strftime('%d/%m/%Y')
                evento_hora_inicio = dt_inicio.strftime('%H:%M')
                evento_hora_fim = dt_fim.strftime('%H:%M')
                duracao_min = int((dt_fim - dt_inicio).total_seconds() / 60)
                evento_duracao = f'{duracao_min} min'
                h = duracao_min // 60
                m = duracao_min % 60
                evento_duracao_fmt = f'{h}h{m:02d}min' if h > 0 else f'{m} min'
                retencao_labels = datas.dt.strftime('%H:%M').tolist()
        if col_usu in totalizado.columns:
            usu = pd.to_numeric(totalizado[col_usu], errors='coerce').fillna(0)
            retencao_values = [int(v) for v in usu.tolist()]
            if not usu.empty:
                idx_pico = int(usu.idxmax())
                pico_audiencia = int(usu.max())
                if retencao_labels and idx_pico < len(retencao_labels):
                    hora_pico = retencao_labels[idx_pico]

    if not evento_duracao and zoom_meta.get('Duração (minutos)'):
        try:
            duracao_min = int(float(zoom_meta['Duração (minutos)']))
            evento_duracao = f'{duracao_min} min'
            h = duracao_min // 60
            m = duracao_min % 60
            evento_duracao_fmt = f'{h}h{m:02d}min' if h > 0 else f'{m} min'
        except (ValueError, TypeError):
            pass

    # --- Inscritos ---
    total_inscritos: Optional[int] = None
    if inscritos is not None and not inscritos.empty:
        total_inscritos = len(inscritos)

    # --- Presentes, tempo médio, todos participantes ---
    total_presentes: Optional[int] = None
    tempo_medio_min: Optional[float] = None
    tempo_medio_fmt: Optional[str] = None
    top_participantes: List[Dict] = []
    todos_participantes: List[Dict] = []

    if relatorio is not None and not relatorio.empty:
        col_nome = 'Nome'
        col_tempo = 'Tempo_Minutos'

        if col_nome in relatorio.columns:
            total_presentes = int(relatorio[col_nome].dropna().nunique())

        if col_tempo in relatorio.columns:
            tempos = pd.to_numeric(relatorio[col_tempo], errors='coerce').fillna(0)
            media = tempos.mean()
            if pd.notna(media):
                tempo_medio_min = round(float(media), 1)
                h = int(tempo_medio_min // 60)
                m = int(tempo_medio_min % 60)
                tempo_medio_fmt = f'{h}h{m:02d}min' if h > 0 else f'{m}min'

            if col_nome in relatorio.columns:
                top_df = relatorio[[col_nome, col_tempo]].copy()
                top_df[col_tempo] = pd.to_numeric(top_df[col_tempo], errors='coerce').fillna(0)
                agrupado = (
                    top_df.groupby(col_nome, as_index=False)[col_tempo]
                    .max()
                    .sort_values(col_tempo, ascending=False)
                )
                top_participantes = [
                    {'nome': str(row[col_nome]), 'minutos': round(float(row[col_tempo]), 1)}
                    for _, row in agrupado.head(10).iterrows()
                ]
                todos_participantes = [
                    {'nome': str(row[col_nome]), 'minutos': round(float(row[col_tempo]), 1)}
                    for _, row in agrupado.iterrows()
                ]

    # --- Taxa de presença ---
    taxa_presenca: Optional[float] = None
    if total_inscritos and total_presentes:
        taxa_presenca = round(total_presentes / total_inscritos * 100, 1)

    # --- Ausentes ---
    total_ausentes: Optional[int] = None
    if total_inscritos is not None and total_presentes is not None:
        total_ausentes = total_inscritos - total_presentes

    # --- Mensagens / chat ---
    total_mensagens = len(mensagens) if mensagens is not None and not mensagens.empty else 0
    total_chat = len(chat) if chat is not None and not chat.empty else 0
    total_interacoes = total_mensagens + total_chat

    # --- Enquetes ---
    enquetes: List[Dict] = []
    enquete_keys = sorted([k for k in processed if k.startswith('enquete_') and k.endswith('_processed')])
    for i, key in enumerate(enquete_keys):
        df_enq: Optional[pd.DataFrame] = processed.get(key)
        if df_enq is None or df_enq.empty:
            continue
        num = i + 1
        pergunta = ''
        if 'Pergunta' in df_enq.columns:
            mode = df_enq['Pergunta'].mode()
            pergunta = str(mode.iloc[0]) if not mode.empty else ''
        total_resp = len(df_enq)
        labels: List[str] = []
        values: List[int] = []
        if 'Resposta' in df_enq.columns:
            counts = df_enq['Resposta'].value_counts().head(10)
            labels = [str(l) for l in counts.index.tolist()]
            values = [int(v) for v in counts.values.tolist()]
        enquetes.append({
            'titulo': f'Enquete {num:02d}',
            'pergunta': pergunta,
            'total_respostas': total_resp,
            'labels': labels,
            'values': values,
        })

    # --- Zoom participantes ---
    zoom_participantes: List[Dict] = []
    if zoom_consol is not None and not zoom_consol.empty:
        col_znome = 'Nome (nome original)'
        col_zemail = 'E-mail'
        col_zperm = 'Permanência (minutos)'
        for _, row in zoom_consol.iterrows():
            zoom_participantes.append({
                'nome': str(row.get(col_znome, '') or ''),
                'email': str(row.get(col_zemail, '') or ''),
                'permanencia': row.get(col_zperm, 0),
            })

    zoom_topico = str(zoom_meta.get('Tópico', '') or zoom_meta.get('Topic', '') or '')
    zoom_host = str(zoom_meta.get('Anfitrião', '') or zoom_meta.get('Host', '') or '')

    return {
        # Identificação
        'data_emissao': today,
        'zoom_topico': zoom_topico,
        'zoom_host': zoom_host,
        # Temporais
        'evento_data': evento_data,
        'evento_hora_inicio': evento_hora_inicio,
        'evento_hora_fim': evento_hora_fim,
        'evento_duracao': evento_duracao,
        'evento_duracao_fmt': evento_duracao_fmt,
        # Público
        'total_inscritos': total_inscritos,
        'total_presentes': total_presentes,
        'total_ausentes': total_ausentes,
        'taxa_presenca': taxa_presenca,
        # Audiência
        'pico_audiencia': pico_audiencia,
        'hora_pico': hora_pico,
        'tempo_medio_min': tempo_medio_min,
        'tempo_medio_fmt': tempo_medio_fmt,
        # Engajamento
        'total_mensagens': total_mensagens,
        'total_chat': total_chat,
        'total_interacoes': total_interacoes,
        # Participantes
        'top_participantes': top_participantes,
        'todos_participantes': todos_participantes,
        # Retenção
        'retencao_labels': retencao_labels,
        'retencao_values': retencao_values,
        # Enquetes
        'enquetes': enquetes,
        # Zoom
        'zoom_participantes': zoom_participantes,
        # Flags
        'has_inscritos': total_inscritos is not None,
        'has_zoom': len(zoom_participantes) > 0,
        'has_mensagens': total_mensagens > 0,
        'has_chat': total_chat > 0,
        'has_enquetes': len(enquetes) > 0,
        'has_todos_participantes': len(todos_participantes) > 0,
    }
