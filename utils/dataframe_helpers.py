"""
Helpers para operações comuns em DataFrames.
"""

from typing import Dict, List
import pandas as pd


class DataFrameHelper:
    """Funções auxiliares para manipulação de DataFrames."""

    @staticmethod
    def normalize_columns(df: pd.DataFrame, renames: Dict[str, str]) -> pd.DataFrame:
        """
        Renomeia colunas baseado em mapa de renomeação.

        Args:
            df: DataFrame a ser normalizado
            renames: Dicionário {nome_antigo: nome_novo}

        Returns:
            DataFrame com colunas renomeadas

        Example:
            >>> df = pd.DataFrame({'Login': ['31999887766']})
            >>> renames = {'Login': 'Celular'}
            >>> df_normalized = DataFrameHelper.normalize_columns(df, renames)
            >>> 'Celular' in df_normalized.columns
            True
        """
        existing_renames = {
            old: new for old, new in renames.items() if old in df.columns
        }
        if existing_renames:
            return df.rename(columns=existing_renames)
        return df

    @staticmethod
    def select_available_columns(
        df: pd.DataFrame,
        required: List[str],
        optional: List[str]
    ) -> List[str]:
        """
        Seleciona colunas disponíveis no DataFrame.

        Args:
            df: DataFrame fonte
            required: Lista de colunas obrigatórias
            optional: Lista de colunas opcionais

        Returns:
            Lista de colunas disponíveis na ordem especificada

        Example:
            >>> df = pd.DataFrame({'Nome': ['João'], 'Celular': ['31999887766']})
            >>> cols = DataFrameHelper.select_available_columns(
            ...     df,
            ...     required=['Nome'],
            ...     optional=['Celular', 'Email']
            ... )
            >>> cols
            ['Nome', 'Celular']
        """
        selected = []

        # Adicionar obrigatórias
        for col in required:
            if col in df.columns:
                selected.append(col)

        # Adicionar opcionais
        for col in optional:
            if col in df.columns and col not in selected:
                selected.append(col)

        return selected
