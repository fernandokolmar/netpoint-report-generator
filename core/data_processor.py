"""
Processador de dados para relatórios PRSA.

Este módulo contém a classe ReportDataProcessor que processa e transforma
os DataFrames brutos em DataFrames prontos para exportação Excel.
"""

from typing import Dict, Callable, Optional
import pandas as pd

from utils.dataframe_helpers import DataFrameHelper
from utils.time_calculator import TimeCalculator
from config import column_mappings, settings
from core.exceptions import DataProcessingError


class ReportDataProcessor:
    """
    Processa e transforma DataFrames para geração de relatórios.

    Esta classe é responsável por:
    - Normalizar nomes de colunas
    - Calcular métricas de tempo e retenção
    - Selecionar colunas relevantes
    - Transformar dados em formato adequado para Excel

    Attributes:
        progress_callback: Função opcional para reportar progresso
    """

    def __init__(self, progress_callback: Optional[Callable[[str], None]] = None):
        """
        Inicializa o processador de dados.

        Args:
            progress_callback: Função opcional que recebe mensagens de progresso
        """
        self.progress_callback = progress_callback

    def _log(self, message: str) -> None:
        """
        Envia mensagem de log via callback se disponível.

        Args:
            message: Mensagem a ser logada
        """
        if self.progress_callback:
            self.progress_callback(message)

    def process_all(self, dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Processa todos os DataFrames necessários para o relatório.

        Args:
            dfs: Dicionário com DataFrames brutos
                Chaves esperadas: 'inscritos', 'relatorio_acesso', 'mensagens', 'totalizado'

        Returns:
            Dicionário com DataFrames processados
                Chaves retornadas: 'inscritos_processed', 'relatorio_processed',
                                  'mensagens_processed', 'totalizado_processed'

        Raises:
            KeyError: Se alguma chave esperada estiver faltando
            ValueError: Se dados estiverem em formato inválido

        Example:
            >>> processor = ReportDataProcessor()
            >>> raw_dfs = {
            ...     'inscritos': df_inscritos,
            ...     'relatorio_acesso': df_relatorio,
            ...     'mensagens': df_mensagens,
            ...     'totalizado': df_totalizado
            ... }
            >>> processed = processor.process_all(raw_dfs)
            >>> 'inscritos_processed' in processed
            True
        """
        self._log("Processando dados...")

        processed = {}

        # Processar inscritos (opcional)
        if 'inscritos' in dfs and dfs['inscritos'] is not None:
            self._log("Processando inscritos...")
            processed['inscritos_processed'] = self._process_inscritos(dfs['inscritos'].copy())
        else:
            self._log("⊘ Inscritos: não há dados para processar")
            processed['inscritos_processed'] = None

        self._log("Processando relatório de acesso...")
        processed['relatorio_processed'] = self._process_relatorio_acesso(
            dfs['relatorio_acesso'].copy()
        )

        # Processar mensagens (opcional)
        if 'mensagens' in dfs and dfs['mensagens'] is not None:
            self._log("Processando mensagens...")
            processed['mensagens_processed'] = self._process_mensagens(
                dfs['mensagens'].copy()
            )
        else:
            self._log("⊘ Mensagens: não há dados para processar")
            processed['mensagens_processed'] = None

        # Processar chat (opcional)
        if 'chat' in dfs and dfs['chat'] is not None:
            self._log("Processando chat...")
            processed['chat_processed'] = self._process_chat(
                dfs['chat'].copy()
            )
        else:
            self._log("⊘ Chat: não há dados para processar")
            processed['chat_processed'] = None

        # Processar enquetes (opcionais, múltiplas)
        enquete_keys = sorted([k for k in dfs if k.startswith('enquete_')])
        for key in enquete_keys:
            if dfs[key] is not None:
                num = key.split('_')[1]
                self._log(f"Processando enquete {num}...")
                processed[f'{key}_processed'] = self._process_enquete(dfs[key].copy())
            else:
                processed[f'{key}_processed'] = None

        # Processar presença no Zoom (opcional)
        if 'presenca_zoom' in dfs and dfs['presenca_zoom'] is not None:
            self._log("Processando presença no Zoom...")
            processed['presenca_zoom_processed'] = self._process_presenca_zoom(dfs['presenca_zoom'].copy())
            processed['presenca_zoom_consolidado'] = self._consolidate_presenca_zoom(dfs['presenca_zoom'].copy())
        else:
            self._log("⊘ Presença no Zoom: não há dados para processar")
            processed['presenca_zoom_processed'] = None
            processed['presenca_zoom_consolidado'] = None

        self._log("Processando totalizado...")
        processed['totalizado_processed'] = self._process_totalizado(
            dfs['totalizado'].copy()
        )

        self._log("Dados processados com sucesso!")

        return processed

    def _remove_system_users(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove registros de sistema da plataforma (usuário 'visitante').

        O registro de sistema tem Login = 'visitante' (case-insensitive).
        Este registro existe em alguns eventos e não representa um participante real.
        A remoção é feita antes de qualquer processamento, enquanto a coluna
        ainda se chama 'Login'.

        Args:
            df: DataFrame bruto com possível coluna 'Login'

        Returns:
            DataFrame sem registros de sistema
        """
        if 'Login' not in df.columns:
            return df

        mask = df['Login'].astype(str).str.strip().str.lower() == 'visitante'
        removed = mask.sum()
        if removed > 0:
            df = df[~mask].reset_index(drop=True)
            self._log(f"✓ {removed} registro(s) de sistema removido(s) (Login='visitante')")

        return df

    def _process_inscritos(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa DataFrame de inscritos.

        Operações:
        - Remove registros de sistema (Login='visitante')
        - Renomeia coluna LGPD longa
        - Renomeia 'Comunidade.1' para 'Comunidade2'
        - Remove colunas completamente vazias
        - Seleciona colunas relevantes

        Args:
            df: DataFrame de inscritos bruto

        Returns:
            DataFrame processado com colunas selecionadas
        """
        # Remover registros de sistema antes de qualquer processamento
        df = self._remove_system_users(df)

        # Normalizar nomes de colunas
        df = DataFrameHelper.normalize_columns(
            df,
            column_mappings.COLUMN_RENAMES
        )

        # Remover colunas completamente vazias
        df = self._remove_empty_columns(df)

        # Ordenar colunas: conhecidas primeiro (na ordem definida), depois as demais
        known_order = (
            column_mappings.REQUIRED_COLUMNS['inscritos'] +
            column_mappings.OPTIONAL_COLUMNS['inscritos']
        )
        ordered_cols = [col for col in known_order if col in df.columns]
        remaining_cols = [col for col in df.columns if col not in ordered_cols]
        all_cols = ordered_cols + remaining_cols

        return df[all_cols]

    def _process_relatorio_acesso(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa DataFrame de relatório de acesso com validação avançada.

        Operações:
        - Renomeia coluna LGPD longa
        - Renomeia 'Comunidade.1' para 'Comunidade_1'
        - Calcula tempo de retenção (hh:mm:ss)
        - Remove colunas completamente vazias
        - Valida dados antes do processamento
        - Seleciona colunas relevantes

        Existem dois modos de cálculo de retenção:
        1. Coluna 'Tempo' já existe em minutos - converte para HH:MM:SS
        2. Colunas 'Data Acesso Inicial' e 'Data Acesso Final' - calcula diferença

        Args:
            df: DataFrame de relatório de acesso bruto

        Returns:
            DataFrame processado com coluna 'Retenção (hh:mm)'

        Raises:
            DataProcessingError: Se dados estiverem em formato inválido
        """
        # Remover registros de sistema antes de qualquer processamento
        df = self._remove_system_users(df)

        # Normalizar nomes de colunas
        renames = column_mappings.COLUMN_RENAMES.copy()
        # Para relatório de acesso, Comunidade.1 vira Comunidade_1 (não Comunidade2)
        renames['Comunidade.1'] = 'Comunidade_1'

        df = DataFrameHelper.normalize_columns(df, renames)

        # Detectar modo: novo formato (Permanencia) ou formato legado (Tempo / datas)
        if settings.COL_PERMANENCIA in df.columns:
            # Modo novo: coluna Permanencia já está em minutos
            self._validate_numeric_column(df, settings.COL_PERMANENCIA, 'relatorio_acesso')
            df['Tempo_Minutos'] = pd.to_numeric(df[settings.COL_PERMANENCIA], errors='coerce').fillna(0)
            self._log("✓ Coluna 'Permanencia' detectada — usando minutos diretamente")

            # Tratar coluna NumPessoas
            if settings.COL_NUM_PESSOAS in df.columns:
                self._validate_numeric_column(df, settings.COL_NUM_PESSOAS, 'relatorio_acesso')
                num_pessoas = pd.to_numeric(df[settings.COL_NUM_PESSOAS], errors='coerce').fillna(0)
                if (num_pessoas > 0).any():
                    # Há pessoas extras — criar coluna Total assistindo
                    df[settings.COL_NUM_PESSOAS] = num_pessoas
                    df[settings.COL_TOTAL_ASSISTINDO] = num_pessoas + 1
                    self._log(f"✓ Coluna '{settings.COL_NUM_PESSOAS}' com valores — '{settings.COL_TOTAL_ASSISTINDO}' calculada")
                else:
                    # Todos zeros — remover coluna
                    df = df.drop(columns=[settings.COL_NUM_PESSOAS])
                    self._log(f"✓ Coluna '{settings.COL_NUM_PESSOAS}' zerada — ocultada do relatório")

        elif settings.COL_TEMPO in df.columns:
            # Modo legado 1: Coluna Tempo em minutos → converter para hh:mm
            self._validate_numeric_column(df, settings.COL_TEMPO, 'relatorio_acesso')
            df[settings.COL_RETENCAO] = df[settings.COL_TEMPO].apply(
                TimeCalculator.format_minutes_to_time
            )
            df['Tempo_Minutos'] = self._convert_time_to_minutes(df[settings.COL_RETENCAO])
            self._log("✓ Coluna 'Tempo_Minutos' calculada para média no Excel")

        elif (settings.COL_DATA_INICIAL in df.columns and
              settings.COL_DATA_FINAL in df.columns):
            # Modo legado 2: Calcular a partir de datas inicial e final
            self._validate_date_column(df, settings.COL_DATA_INICIAL, 'relatorio_acesso')
            self._validate_date_column(df, settings.COL_DATA_FINAL, 'relatorio_acesso')

            def calc_retention(row):
                try:
                    return TimeCalculator.calculate_time_from_dates(
                        row[settings.COL_DATA_INICIAL],
                        row[settings.COL_DATA_FINAL],
                        date_format=settings.DATE_FORMAT
                    )
                except (ValueError, KeyError):
                    return "0:00:00"

            df[settings.COL_RETENCAO] = df.apply(calc_retention, axis=1)
            df['Tempo_Minutos'] = self._convert_time_to_minutes(df[settings.COL_RETENCAO])
            self._log("✓ Coluna 'Tempo_Minutos' calculada para média no Excel")

        else:
            self._log(
                f"⚠ Aviso: Não foi possível calcular retenção. "
                f"Esperava coluna '{settings.COL_PERMANENCIA}', '{settings.COL_TEMPO}' ou "
                f"'{settings.COL_DATA_INICIAL}' e '{settings.COL_DATA_FINAL}'"
            )
            df['Tempo_Minutos'] = 0

        # Remover colunas completamente vazias
        df = self._remove_empty_columns(df)

        # Ordenar colunas: conhecidas primeiro (na ordem definida), depois as demais
        known_order = (
            column_mappings.REQUIRED_COLUMNS['relatorio_acesso'] +
            column_mappings.OPTIONAL_COLUMNS['relatorio_acesso']
        )
        ordered_cols = [col for col in known_order if col in df.columns]
        remaining_cols = [col for col in df.columns if col not in ordered_cols]

        # Garantir que Retenção e Tempo_Minutos estão no final (necessários para fórmulas Excel)
        priority_end = []
        for col in [settings.COL_RETENCAO, 'Tempo_Minutos']:
            if col in df.columns and col not in ordered_cols and col not in remaining_cols:
                priority_end.append(col)

        all_cols = ordered_cols + remaining_cols + priority_end
        return df[all_cols]

    def _process_mensagens(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa DataFrame de mensagens.

        Operações:
        - Renomeia coluna LGPD longa
        - Renomeia 'Comunidade.1' para 'Comunidade2'
        - Seleciona colunas relevantes

        Args:
            df: DataFrame de mensagens bruto

        Returns:
            DataFrame processado com colunas selecionadas
        """
        # Normalizar nomes de colunas
        df = DataFrameHelper.normalize_columns(
            df,
            column_mappings.COLUMN_RENAMES
        )

        # Selecionar colunas disponíveis
        selected_cols = DataFrameHelper.select_available_columns(
            df,
            required=column_mappings.REQUIRED_COLUMNS['mensagens'],
            optional=column_mappings.OPTIONAL_COLUMNS['mensagens']
        )

        # Retornar DataFrame com colunas selecionadas
        if selected_cols:
            return df[selected_cols]

        return df

    def _process_chat(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa DataFrame de chat.

        Suporta dois formatos:
        1. Formato padrão Netpoint: Cliente, Sala, Nome, Mensagem, DataFormatada
        2. Formato Minnit: timestamp, username, nickname, message

        Operações:
        - Detecta formato automaticamente
        - Converte Minnit para formato padrão se necessário
        - Mantém apenas colunas relevantes (remove Cliente, Sala)

        Args:
            df: DataFrame de chat bruto

        Returns:
            DataFrame processado
        """
        # Detectar se é formato Minnit
        if self._is_minnit_format(df):
            self._log("✓ Convertendo formato Minnit para formato padrão...")
            df = self._convert_minnit_to_standard(df)
        else:
            # Formato padrão - apenas normalizar nomes de colunas
            df = DataFrameHelper.normalize_columns(
                df,
                column_mappings.COLUMN_RENAMES
            )

        # Retornar DataFrame (filtro de colunas será feito no Excel)
        return df

    def _is_minnit_format(self, df: pd.DataFrame) -> bool:
        """
        Verifica se o DataFrame é do formato Minnit Chat.

        Args:
            df: DataFrame a verificar

        Returns:
            True se for formato Minnit
        """
        df_columns = [col.lower() for col in df.columns]
        minnit_required = ['timestamp', 'username', 'nickname', 'message']
        return all(col in df_columns for col in minnit_required)

    def _convert_minnit_to_standard(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converte DataFrame do formato Minnit para formato padrão de chat.

        Formato Minnit:
        - timestamp: Unix timestamp (segundos desde 1970)
        - username: ID do usuário (ex: guest13528733)
        - nickname: Nome exibido
        - recipient_username: Destinatário (vazio = mensagem pública)
        - recipient_nickname: Nome do destinatário
        - message: Conteúdo da mensagem

        Formato padrão (saída):
        - Nome: nickname
        - Mensagem: message
        - DataFormatada: timestamp convertido para DD/MM/YYYY HH:MM:SS

        Args:
            df: DataFrame no formato Minnit

        Returns:
            DataFrame no formato padrão
        """
        from datetime import datetime

        # Criar novo DataFrame com colunas padrão
        result = pd.DataFrame()

        # Mapear colunas (case-insensitive)
        col_map = {col.lower(): col for col in df.columns}

        # Nome = nickname
        if 'nickname' in col_map:
            result['Nome'] = df[col_map['nickname']]

        # Mensagem = message
        if 'message' in col_map:
            result['Mensagem'] = df[col_map['message']]

        # DataFormatada = timestamp convertido
        if 'timestamp' in col_map:
            def convert_timestamp(ts):
                try:
                    # Unix timestamp para datetime
                    dt = datetime.fromtimestamp(int(ts))
                    return dt.strftime('%d/%m/%Y %H:%M:%S')
                except (ValueError, TypeError, OSError):
                    return ''

            result['DataFormatada'] = df[col_map['timestamp']].apply(convert_timestamp)

        self._log(f"✓ {len(result)} mensagens convertidas do formato Minnit")
        return result

    def _process_enquete(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa DataFrame de enquete.

        Mantém apenas as colunas relevantes:
        Nome, Login, Pergunta, Resposta, Data

        Args:
            df: DataFrame de enquete bruto

        Returns:
            DataFrame processado com colunas selecionadas
        """
        desired = ['Nome', 'Login', 'Pergunta', 'Resposta', 'Data']
        available = [col for col in desired if col in df.columns]

        if available:
            return df[available]
        return df

    def _process_presenca_zoom(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa DataFrame de presença no Zoom.

        O arquivo exportado pelo Zoom tem formato especial:
        - Linha 1: cabeçalho do resumo da reunião (Tópico, ID, Anfitrião, ...)
        - Linha 2: dados do resumo
        - Linha 3: em branco
        - Linha 4: cabeçalho real dos participantes
        - Linhas 5+: dados dos participantes

        O data_loader já faz o parse correto pulando para a linha de
        cabeçalho real (detectada pela coluna "Nome (nome original)").
        Aqui apenas limpamos e selecionamos as colunas relevantes.

        Args:
            df: DataFrame já parseado com cabeçalho real dos participantes

        Returns:
            DataFrame processado
        """
        # Remover colunas completamente vazias
        df = self._remove_empty_columns(df)

        # Colunas relevantes (na ordem preferida)
        desired = [
            'Nome (nome original)', 'E-mail',
            'Ingressar na hora', 'Hora de saída', 'Duração (minutos)',
            'Convidado', 'Na sala de espera'
        ]
        ordered = [col for col in desired if col in df.columns]
        remaining = [col for col in df.columns if col not in ordered]
        return df[ordered + remaining]

    def _consolidate_presenca_zoom(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Consolida presença no Zoom agrupando por participante.

        O arquivo Zoom exporta uma linha por sessão (entrada/saída).
        Um mesmo participante pode ter várias linhas (entrou/saiu/voltou).
        Este método agrupa por nome e soma o tempo total.

        Resultado por participante:
        - Nome
        - E-mail (primeiro valor não vazio)
        - Primeira entrada
        - Última saída
        - Duração total (minutos) — soma de todas as sessões
        - Convidado

        Args:
            df: DataFrame bruto de presença Zoom

        Returns:
            DataFrame consolidado com uma linha por participante
        """
        col_nome = 'Nome (nome original)'
        col_email = 'E-mail'
        col_entrada = 'Ingressar na hora'
        col_saida = 'Hora de saída'
        col_duracao = 'Duração (minutos)'
        col_convidado = 'Convidado'

        if col_nome not in df.columns or col_duracao not in df.columns:
            self._log("⚠ Colunas esperadas não encontradas no arquivo Zoom — retornando sem consolidar")
            return df

        # Converter duração para numérico
        df[col_duracao] = pd.to_numeric(df[col_duracao], errors='coerce').fillna(0)

        # Agrupar por nome
        agg = {col_duracao: 'sum'}

        if col_email in df.columns:
            agg[col_email] = lambda x: next((v for v in x if pd.notna(v) and str(v).strip()), '')

        if col_entrada in df.columns:
            agg[col_entrada] = 'min'

        if col_saida in df.columns:
            agg[col_saida] = 'max'

        if col_convidado in df.columns:
            agg[col_convidado] = 'first'

        consolidado = df.groupby(col_nome, as_index=False).agg(agg)

        # Reordenar colunas
        desired_order = [col_nome, col_email, col_entrada, col_saida, col_duracao, col_convidado]
        ordered = [c for c in desired_order if c in consolidado.columns]
        remaining = [c for c in consolidado.columns if c not in ordered]
        consolidado = consolidado[ordered + remaining]

        # Renomear Duração para deixar claro que é total
        consolidado = consolidado.rename(columns={col_duracao: 'Duração total (minutos)'})

        # Ordenar por nome
        consolidado = consolidado.sort_values(col_nome).reset_index(drop=True)

        self._log(f"✓ Zoom consolidado: {len(consolidado)} participantes únicos")
        return consolidado

    def _process_totalizado(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa DataFrame totalizado (retenção na live) com validação.

        Operações:
        - Valida coluna 'Usuarios conectados' é numérica
        - Converte coluna 'Data' para datetime
        - Mantém estrutura original (Max será calculado no Excel)

        Args:
            df: DataFrame totalizado bruto

        Returns:
            DataFrame processado com Data em formato datetime

        Raises:
            DataProcessingError: Se dados estiverem em formato inválido
        """
        # Validar coluna de usuários conectados
        if settings.COL_USUARIOS_CONECTADOS in df.columns:
            self._validate_numeric_column(
                df,
                settings.COL_USUARIOS_CONECTADOS,
                'totalizado'
            )

        # Converter Data para datetime se existir
        if settings.COL_DATA in df.columns:
            self._validate_date_column(df, settings.COL_DATA, 'totalizado')

            df[settings.COL_DATA] = pd.to_datetime(
                df[settings.COL_DATA],
                format=settings.DATE_FORMAT,
                dayfirst=True,
                errors='coerce'  # Converter inválidos para NaT
            )

            # Detectar linhas com datas inválidas
            invalid_dates = df[settings.COL_DATA].isna().sum()
            if invalid_dates > 0:
                self._log(
                    f"⚠ Aviso: {invalid_dates} linha(s) em totalizado com datas inválidas "
                    f"(foram convertidas para NaT)"
                )

        # Nota: Não adicionar coluna 'Max' aqui - será criada com fórmula no Excel
        return df

    def _validate_numeric_column(
        self,
        df: pd.DataFrame,
        col_name: str,
        df_type: str
    ) -> None:
        """
        Valida que uma coluna contém valores numéricos válidos.

        Args:
            df: DataFrame a validar
            col_name: Nome da coluna
            df_type: Tipo do DataFrame (para mensagens de erro)

        Raises:
            DataProcessingError: Se coluna contiver valores não-numéricos
        """
        if col_name not in df.columns:
            return

        # Tentar converter para numérico
        numeric_series = pd.to_numeric(df[col_name], errors='coerce')

        # Contar valores inválidos (não convertidos)
        invalid_count = numeric_series.isna().sum() - df[col_name].isna().sum()

        if invalid_count > 0:
            # Encontrar exemplos de valores inválidos
            invalid_mask = numeric_series.isna() & df[col_name].notna()
            examples = df[invalid_mask][col_name].head(3).tolist()

            raise DataProcessingError(
                f"Coluna '{col_name}' em {df_type} contém {invalid_count} valores não-numéricos.\n"
                f"Exemplos de valores inválidos: {examples}\n"
                f"Verifique se o arquivo está correto."
            )

        # Warning se mais de 30% dos valores são negativos (suspeito)
        negative_count = (numeric_series < 0).sum()
        if negative_count > len(df) * 0.3:
            self._log(
                f"⚠ Aviso: Coluna '{col_name}' em {df_type} tem {negative_count} valores negativos "
                f"({negative_count/len(df)*100:.1f}%)"
            )

    def _validate_date_column(
        self,
        df: pd.DataFrame,
        col_name: str,
        df_type: str
    ) -> None:
        """
        Valida que uma coluna contém datas em formato válido.

        Args:
            df: DataFrame a validar
            col_name: Nome da coluna
            df_type: Tipo do DataFrame (para mensagens de erro)

        Raises:
            DataProcessingError: Se muitas datas estiverem em formato inválido
        """
        if col_name not in df.columns:
            return

        # Tentar converter para datetime
        date_series = pd.to_datetime(
            df[col_name],
            format=settings.DATE_FORMAT,
            dayfirst=True,
            errors='coerce'
        )

        # Contar valores inválidos
        invalid_count = date_series.isna().sum() - df[col_name].isna().sum()

        # Se mais de 50% inválido, é erro crítico
        if invalid_count > len(df) * 0.5:
            examples = df[date_series.isna() & df[col_name].notna()][col_name].head(3).tolist()

            raise DataProcessingError(
                f"Coluna '{col_name}' em {df_type} tem {invalid_count} datas em formato inválido "
                f"({invalid_count/len(df)*100:.1f}%).\n"
                f"Formato esperado: {settings.DATE_FORMAT}\n"
                f"Exemplos de valores inválidos: {examples}\n"
                f"Verifique se o formato de data está correto."
            )

        # Se 10-50% inválido, é warning
        elif invalid_count > len(df) * 0.1:
            self._log(
                f"⚠ Aviso: Coluna '{col_name}' em {df_type} tem {invalid_count} datas inválidas "
                f"({invalid_count/len(df)*100:.1f}%)"
            )

    def _convert_time_to_minutes(self, time_str_series: pd.Series) -> pd.Series:
        """
        Converte série de tempo HH:MM:SS para minutos (numérico).

        Esta função é necessária para cálculo correto da média no Excel,
        pois AVERAGE não funciona com formato de tempo em texto.

        Args:
            time_str_series: Série com strings no formato "H:MM:SS" ou "HH:MM:SS"

        Returns:
            Série com valores numéricos em minutos (float)

        Example:
            >>> series = pd.Series(["1:30:00", "2:15:30", "0:45:00"])
            >>> result = processor._convert_time_to_minutes(series)
            >>> result.tolist()
            [90.0, 135.5, 45.0]
        """
        def parse_time(time_str: str) -> float:
            """Parse string de tempo para minutos."""
            if pd.isna(time_str) or time_str == "0:00:00" or time_str == "":
                return 0.0

            try:
                parts = str(time_str).split(':')
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2]) if len(parts) > 2 else 0

                # Converter tudo para minutos
                total_minutes = hours * 60 + minutes + seconds / 60
                return round(total_minutes, 2)
            except (ValueError, IndexError):
                # Se não conseguir parsear, retornar 0
                return 0.0

        return time_str_series.apply(parse_time)

    def _smart_rename_login(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detecta automaticamente se a coluna 'Login' contém Email ou Celular.

        Se a maioria dos valores contém '@', renomeia para 'Email'.
        Caso contrário, renomeia para 'Celular'.

        Args:
            df: DataFrame com possível coluna 'Login'

        Returns:
            DataFrame com coluna renomeada apropriadamente
        """
        if 'Login' not in df.columns:
            return df

        # Verificar se maioria contém '@' (indica email)
        login_values = df['Login'].dropna().astype(str)
        if len(login_values) == 0:
            return df

        email_count = login_values.str.contains('@', na=False).sum()
        email_ratio = email_count / len(login_values)

        if email_ratio > 0.5:
            # Maioria é email
            df = df.rename(columns={'Login': 'Email'})
            self._log("✓ Coluna 'Login' detectada como Email")
        else:
            # Maioria é celular/telefone
            df = df.rename(columns={'Login': 'Celular'})
            self._log("✓ Coluna 'Login' detectada como Celular")

        return df

    def _remove_empty_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove colunas que estão completamente vazias em todos os registros.

        Uma coluna é considerada vazia se todos os valores são:
        - None/NaN
        - String vazia ''
        - String com apenas espaços

        Args:
            df: DataFrame a processar

        Returns:
            DataFrame sem colunas completamente vazias
        """
        columns_to_remove = []

        for i, col in enumerate(df.columns):
            # Usar iloc para evitar ambiguidade com colunas de nome duplicado
            col_series = df.iloc[:, i].dropna()

            # Se não há valores não-nulos, coluna está vazia
            if len(col_series) == 0:
                columns_to_remove.append(i)
                continue

            # Verificar se todos os valores são strings vazias
            if col_series.dtype == object:
                non_empty = col_series.astype(str).str.strip().str.len() > 0
                if not non_empty.any():
                    columns_to_remove.append(i)

        if columns_to_remove:
            col_names = [df.columns[i] for i in columns_to_remove]
            self._log(f"✓ Removidas {len(columns_to_remove)} colunas vazias: {', '.join(str(n) for n in col_names[:5])}{'...' if len(columns_to_remove) > 5 else ''}")
            df = df.drop(df.columns[columns_to_remove], axis=1)

        return df
