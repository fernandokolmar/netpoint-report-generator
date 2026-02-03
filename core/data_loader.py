"""
Módulo responsável por carregar arquivos CSV.
"""

from typing import Dict, Optional, Callable, List
import pandas as pd
import os
from config.settings import CSV_ENCODING, CSV_SEPARATOR, MAX_FILE_SIZE_MB
from config.column_mappings import REQUIRED_COLUMNS
from core.exceptions import DataLoadError, EmptyDataFrameError, MissingColumnsError


class CSVLoader:
    """
    Carrega arquivos CSV e valida tamanho/formato.

    Esta classe é responsável exclusivamente por operações de I/O
    relacionadas a arquivos CSV.
    """

    def __init__(self, progress_callback: Optional[Callable[[str], None]] = None):
        """
        Inicializa o loader com callback opcional de progresso.

        Args:
            progress_callback: Função chamada para reportar progresso.
                              Recebe string com mensagem de status.
        """
        self.progress_callback = progress_callback

    def load_csv(
        self,
        file_path: str,
        encoding: str = CSV_ENCODING,
        sep: str = CSV_SEPARATOR
    ) -> pd.DataFrame:
        """
        Carrega um arquivo CSV único.

        Args:
            file_path: Caminho completo do arquivo CSV
            encoding: Encoding do arquivo (padrão: utf-8-sig)
            sep: Separador de colunas (padrão: ';')

        Returns:
            DataFrame com dados do CSV

        Raises:
            FileNotFoundError: Se arquivo não existe
            PermissionError: Se não tem permissão para ler
            UnicodeDecodeError: Se encoding está incorreto
            pd.errors.ParserError: Se formato CSV é inválido
            DataLoadError: Outros erros de carregamento

        Example:
            >>> loader = CSVLoader()
            >>> df = loader.load_csv('inscritos.csv')
            >>> len(df) > 0
            True
        """
        # Validar que arquivo existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Arquivo não encontrado: {file_path}\n"
                f"Verifique se o caminho está correto."
            )

        # Validar permissões
        if not os.access(file_path, os.R_OK):
            raise PermissionError(
                f"Sem permissão para ler: {file_path}\n"
                f"Verifique as permissões do arquivo."
            )

        # Validar tamanho do arquivo
        self._validate_file_size(file_path)

        # Carregar CSV
        try:
            df = pd.read_csv(file_path, encoding=encoding, sep=sep)
            return df

        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(
                e.encoding,
                e.object,
                e.start,
                e.end,
                f"Erro de codificação no arquivo: {file_path}\n"
                f"Tente salvar o arquivo como UTF-8 no Excel.\n"
                f"Encoding tentado: {encoding}"
            )

        except pd.errors.ParserError as e:
            raise pd.errors.ParserError(
                f"Formato CSV inválido em: {file_path}\n"
                f"Verifique se o separador é ';' (ponto-e-vírgula)\n"
                f"Erro: {str(e)}"
            )

        except Exception as e:
            raise DataLoadError(
                f"Erro inesperado ao carregar {file_path}: {type(e).__name__}\n"
                f"Detalhes: {str(e)}"
            )

    def load_all(self, file_paths: Dict[str, str]) -> Dict[str, pd.DataFrame]:
        """
        Carrega múltiplos arquivos CSV com validação avançada.

        Args:
            file_paths: Dicionário {tipo: caminho_arquivo}
                       Ex: {'inscritos': 'path/to/inscritos.csv'}
                       Arquivos com caminho vazio são ignorados (opcionais)

        Returns:
            Dicionário {tipo: DataFrame}

        Raises:
            EmptyDataFrameError: Se algum CSV estiver vazio
            MissingColumnsError: Se faltar coluna obrigatória
            DataLoadError: Se houver erro ao carregar

        Example:
            >>> loader = CSVLoader()
            >>> dfs = loader.load_all({
            ...     'inscritos': 'inscritos.csv',
            ...     'mensagens': 'mensagens.csv'
            ... })
            >>> 'inscritos' in dfs
            True
        """
        self._notify("Carregando arquivos CSV...")
        dfs = {}

        for key, path in file_paths.items():
            # Ignorar arquivos opcionais (caminho vazio)
            if not path:
                self._notify(f"⊘ {key}: não selecionado (opcional)")
                continue

            self._notify(f"Carregando {key}...")

            try:
                df = self.load_csv(path)

                # Validação 1: Não está vazio
                if df.empty:
                    raise EmptyDataFrameError(
                        f"Arquivo {key} está vazio (0 registros): {path}"
                    )

                # Validação 2: Contém linhas com dados (não apenas header)
                if len(df) == 0:
                    raise EmptyDataFrameError(
                        f"Arquivo {key} contém apenas cabeçalho (0 linhas de dados): {path}"
                    )

                # Validação 3: Colunas obrigatórias presentes
                self._validate_required_columns(df, key, path)

                # Validação 4: Detectar colunas vazias
                self._validate_columns_not_empty(df, key)

                dfs[key] = df

                # Calcular tamanho em MB
                size_mb = os.path.getsize(path) / (1024 * 1024)
                self._notify(
                    f"✓ {key}: {len(df):,} registros, {len(df.columns)} colunas ({size_mb:.1f} MB)"
                )

            except Exception as e:
                self._notify(f"✗ Erro ao carregar {key}: {str(e)}")
                raise

        self._notify(f"✓ {len(dfs)} arquivos carregados com sucesso")
        return dfs

    def _validate_file_size(self, file_path: str) -> None:
        """
        Valida tamanho do arquivo.

        Args:
            file_path: Caminho do arquivo

        Raises:
            DataLoadError: Se arquivo exceder tamanho máximo

        Note:
            Tamanho máximo definido em config.settings.MAX_FILE_SIZE_MB
        """
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)

        if size_mb > MAX_FILE_SIZE_MB:
            raise DataLoadError(
                f"Arquivo muito grande: {size_mb:.1f} MB\n"
                f"Máximo permitido: {MAX_FILE_SIZE_MB} MB\n"
                f"Arquivo: {os.path.basename(file_path)}"
            )

    def _validate_required_columns(
        self,
        df: pd.DataFrame,
        df_type: str,
        file_path: str
    ) -> None:
        """
        Valida que colunas obrigatórias estão presentes.

        Args:
            df: DataFrame para validar
            df_type: Tipo do DataFrame ('inscritos', 'mensagens', etc)
            file_path: Caminho do arquivo (para mensagem de erro)

        Raises:
            MissingColumnsError: Se faltar alguma coluna obrigatória
        """
        if df_type not in REQUIRED_COLUMNS:
            # Sem validação para este tipo
            return

        required = REQUIRED_COLUMNS[df_type]
        missing = [col for col in required if col not in df.columns]

        if missing:
            raise MissingColumnsError(
                f"Arquivo {df_type} não possui colunas obrigatórias: {', '.join(missing)}\n"
                f"Arquivo: {file_path}\n"
                f"Colunas encontradas: {', '.join(df.columns.tolist())}\n"
                f"Colunas obrigatórias: {', '.join(required)}"
            )

    def _validate_columns_not_empty(
        self,
        df: pd.DataFrame,
        df_type: str
    ) -> None:
        """
        Valida que colunas obrigatórias não estão completamente vazias.

        Args:
            df: DataFrame para validar
            df_type: Tipo do DataFrame

        Raises:
            EmptyDataFrameError: Se coluna obrigatória estiver toda vazia
        """
        if df_type not in REQUIRED_COLUMNS:
            return

        required = REQUIRED_COLUMNS[df_type]

        for col in required:
            if col in df.columns:
                # Contar valores não-nulos
                non_null_count = df[col].notna().sum()

                if non_null_count == 0:
                    raise EmptyDataFrameError(
                        f"Coluna obrigatória '{col}' em {df_type} está completamente vazia.\n"
                        f"Verifique se o arquivo está correto."
                    )

                # Warning se mais de 50% vazio (apenas log, não bloqueia)
                null_percentage = (len(df) - non_null_count) / len(df) * 100
                if null_percentage > 50:
                    self._notify(
                        f"⚠ Aviso: Coluna '{col}' em {df_type} tem {null_percentage:.1f}% de valores vazios"
                    )

    def _notify(self, message: str) -> None:
        """
        Notifica progresso via callback.

        Args:
            message: Mensagem de status
        """
        if self.progress_callback:
            self.progress_callback(message)
