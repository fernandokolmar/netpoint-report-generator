"""
Exceções customizadas do projeto PRSA Report Generator.

Define hierarquia de exceções para tratamento específico de erros.
"""


class PRSAException(Exception):
    """Exceção base do projeto PRSA."""
    pass


class DataLoadError(PRSAException):
    """Erro ao carregar dados."""
    pass


class EmptyDataFrameError(DataLoadError):
    """DataFrame está vazio (0 registros)."""
    pass


class MissingColumnsError(DataLoadError):
    """Colunas obrigatórias ausentes no DataFrame."""
    pass


class InvalidDateFormatError(DataLoadError):
    """Formato de data inválido."""
    pass


class DataProcessingError(PRSAException):
    """Erro ao processar dados."""
    pass


class ExcelGenerationError(PRSAException):
    """Erro ao gerar arquivo Excel."""
    pass


class ValidationError(PRSAException):
    """Erro de validação de dados."""
    pass
