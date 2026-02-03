"""
Core module - Business logic do Gerador de Relatórios PRSA.

Este módulo contém a lógica de negócio separada da interface gráfica,
permitindo reutilização e testabilidade.
"""

from .data_loader import CSVLoader
from .data_processor import ReportDataProcessor
from .excel_generator import ExcelGenerator
from .controller import ReportController

__all__ = [
    'CSVLoader',
    'ReportDataProcessor',
    'ExcelGenerator',
    'ReportController'
]
