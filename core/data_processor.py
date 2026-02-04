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

        # Processar cada tipo de DataFrame
        self._log("Processando inscritos...")
        processed['inscritos_processed'] = self._process_inscritos(
            dfs['inscritos'].copy()
        )

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

        self._log("Processando totalizado...")
        processed['totalizado_processed'] = self._process_totalizado(
            dfs['totalizado'].copy()
        )

        self._log("Dados processados com sucesso!")

        return processed

    def _process_inscritos(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa DataFrame de inscritos.

        Operações:
        - Detecta se 'Login' é Email ou Celular
        - Renomeia coluna LGPD longa
        - Renomeia 'Comunidade.1' para 'Comunidade2'
        - Remove colunas completamente vazias
        - Seleciona colunas relevantes

        Args:
            df: DataFrame de inscritos bruto

        Returns:
            DataFrame processado com colunas selecionadas
        """
        # Detectar e renomear Login para Email ou Celular
        df = self._smart_rename_login(df)

        # Normalizar nomes de colunas
        df = DataFrameHelper.normalize_columns(
            df,
            column_mappings.COLUMN_RENAMES
        )

        # Remover colunas completamente vazias
        df = self._remove_empty_columns(df)

        # Selecionar colunas disponíveis
        selected_cols = DataFrameHelper.select_available_columns(
            df,
            required=column_mappings.REQUIRED_COLUMNS['inscritos'],
            optional=column_mappings.OPTIONAL_COLUMNS['inscritos']
        )

        # Retornar DataFrame com colunas selecionadas
        if selected_cols:
            return df[selected_cols]

        # Se nenhuma coluna foi selecionada, retornar DataFrame original
        return df

    def _process_relatorio_acesso(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa DataFrame de relatório de acesso com validação avançada.

        Operações:
        - Detecta se 'Login' é Email ou Celular
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
        # Detectar e renomear Login para Email ou Celular
        df = self._smart_rename_login(df)

        # Normalizar nomes de colunas
        renames = column_mappings.COLUMN_RENAMES.copy()
        # Para relatório de acesso, Comunidade.1 vira Comunidade_1 (não Comunidade2)
        renames['Comunidade.1'] = 'Comunidade_1'

        df = DataFrameHelper.normalize_columns(df, renames)

        # Calcular tempo de retenção
        if settings.COL_TEMPO in df.columns:
            # Modo 1: Coluna Tempo já existe em minutos
            # Validar que coluna Tempo contém valores numéricos
            self._validate_numeric_column(df, settings.COL_TEMPO, 'relatorio_acesso')

            df[settings.COL_RETENCAO] = df[settings.COL_TEMPO].apply(
                TimeCalculator.format_minutes_to_time
            )

        elif (settings.COL_DATA_INICIAL in df.columns and
              settings.COL_DATA_FINAL in df.columns):
            # Modo 2: Calcular a partir de datas inicial e final
            # Validar formato de datas
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
        else:
            # Nenhum dos dois modos disponível
            self._log(
                f"⚠ Aviso: Não foi possível calcular retenção. "
                f"Esperava coluna '{settings.COL_TEMPO}' ou "
                f"'{settings.COL_DATA_INICIAL}' e '{settings.COL_DATA_FINAL}'"
            )
            df[settings.COL_RETENCAO] = "0:00:00"

        # Adicionar coluna auxiliar numérica para cálculo de média no Excel
        if settings.COL_RETENCAO in df.columns:
            df['Tempo_Minutos'] = self._convert_time_to_minutes(df[settings.COL_RETENCAO])
            self._log("✓ Coluna 'Tempo_Minutos' calculada para média no Excel")

        # Remover colunas completamente vazias
        df = self._remove_empty_columns(df)

        # Selecionar colunas disponíveis
        selected_cols = DataFrameHelper.select_available_columns(
            df,
            required=column_mappings.REQUIRED_COLUMNS['relatorio_acesso'],
            optional=column_mappings.OPTIONAL_COLUMNS['relatorio_acesso']
        )

        # Garantir que Retenção está incluída se foi calculada
        if settings.COL_RETENCAO in df.columns and settings.COL_RETENCAO not in selected_cols:
            selected_cols.append(settings.COL_RETENCAO)

        # Garantir que Tempo_Minutos está incluída (necessária para fórmulas Excel)
        if 'Tempo_Minutos' in df.columns and 'Tempo_Minutos' not in selected_cols:
            selected_cols.append('Tempo_Minutos')

        # Retornar DataFrame com colunas selecionadas
        if selected_cols:
            return df[selected_cols]

        return df

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

        O chat tem estrutura diferente do arquivo de mensagens:
        - Cliente, Sala, Nome, Mensagem, DataFormatada

        Operações:
        - Mantém apenas colunas relevantes (remove Cliente, Sala)

        Args:
            df: DataFrame de chat bruto

        Returns:
            DataFrame processado
        """
        # O chat geralmente já vem no formato correto
        # Apenas normalizar nomes de colunas se necessário
        df = DataFrameHelper.normalize_columns(
            df,
            column_mappings.COLUMN_RENAMES
        )

        # Retornar DataFrame como está (filtro de colunas será feito no Excel)
        return df

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

        for col in df.columns:
            # Verificar se coluna está completamente vazia
            col_values = df[col].dropna()

            # Se não há valores não-nulos, coluna está vazia
            if len(col_values) == 0:
                columns_to_remove.append(col)
                continue

            # Verificar se todos os valores são strings vazias
            if col_values.dtype == object:
                non_empty = col_values.astype(str).str.strip().str.len() > 0
                if not non_empty.any():
                    columns_to_remove.append(col)

        if columns_to_remove:
            self._log(f"✓ Removidas {len(columns_to_remove)} colunas vazias: {', '.join(columns_to_remove[:5])}{'...' if len(columns_to_remove) > 5 else ''}")
            df = df.drop(columns=columns_to_remove)

        return df
