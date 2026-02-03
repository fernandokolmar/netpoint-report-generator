"""
Configurações e constantes do projeto PRSA Report Generator.
"""

from .settings import *
from .column_mappings import *

__all__ = [
    'CSV_ENCODING',
    'CSV_SEPARATOR',
    'DATE_FORMAT',
    'MAX_FILE_SIZE_MB',
    'EXCEL_TABLE_STYLE',
    'COLUMN_RENAMES',
    'REQUIRED_COLUMNS',
    'OPTIONAL_COLUMNS'
]
