"""
Sistema de logging para aplicação PRSA.

Salva logs em arquivo para debug e auditoria.
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional


class PRSALogger:
    """
    Logger customizado para aplicação PRSA.

    Salva logs tanto em arquivo quanto no console,
    com rotação automática para evitar arquivos muito grandes.
    """

    def __init__(
        self,
        log_dir: str = "~/.prsa/logs",
        log_level: int = logging.INFO,
        max_log_files: int = 10
    ):
        """
        Inicializa o logger.

        Args:
            log_dir: Diretório onde salvar logs
            log_level: Nível mínimo de log (DEBUG, INFO, WARNING, ERROR)
            max_log_files: Número máximo de arquivos de log a manter
        """
        self.log_dir = Path(log_dir).expanduser()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.max_log_files = max_log_files

        # Criar arquivo de log com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = self.log_dir / f"prsa_{timestamp}.log"

        # Configurar logging
        self._setup_logging(log_level)

        # Limpar logs antigos
        self._cleanup_old_logs()

    def _setup_logging(self, log_level: int) -> None:
        """
        Configura handlers de logging.

        Args:
            log_level: Nível de log
        """
        # Criar logger
        self.logger = logging.getLogger('PRSA')
        self.logger.setLevel(log_level)

        # Remover handlers existentes (evitar duplicação)
        self.logger.handlers.clear()

        # Formato das mensagens
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para arquivo
        file_handler = logging.FileHandler(
            self.log_file,
            encoding='utf-8',
            mode='w'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Handler para console (apenas WARNING e acima)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _cleanup_old_logs(self) -> None:
        """Remove logs antigos, mantendo apenas os últimos N arquivos."""
        # Listar todos os arquivos de log
        log_files = sorted(
            self.log_dir.glob("prsa_*.log"),
            key=lambda p: p.stat().st_mtime,
            reverse=True  # Mais recentes primeiro
        )

        # Deletar logs além do limite
        for log_file in log_files[self.max_log_files:]:
            try:
                log_file.unlink()
                self.logger.debug(f"Log antigo removido: {log_file.name}")
            except Exception as e:
                self.logger.warning(f"Erro ao remover log antigo: {e}")

    def info(self, message: str) -> None:
        """
        Loga mensagem de informação.

        Args:
            message: Mensagem a logar
        """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """
        Loga mensagem de aviso.

        Args:
            message: Mensagem a logar
        """
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False) -> None:
        """
        Loga mensagem de erro.

        Args:
            message: Mensagem a logar
            exc_info: Se True, inclui informações da exceção atual
        """
        self.logger.error(message, exc_info=exc_info)

    def debug(self, message: str) -> None:
        """
        Loga mensagem de debug.

        Args:
            message: Mensagem a logar
        """
        self.logger.debug(message)

    def critical(self, message: str, exc_info: bool = False) -> None:
        """
        Loga mensagem crítica.

        Args:
            message: Mensagem a logar
            exc_info: Se True, inclui informações da exceção atual
        """
        self.logger.critical(message, exc_info=exc_info)

    def exception(self, message: str) -> None:
        """
        Loga exceção com stack trace completo.

        Deve ser chamado dentro de um bloco except.

        Args:
            message: Mensagem descritiva do erro
        """
        self.logger.exception(message)

    def get_log_path(self) -> Path:
        """
        Retorna caminho do arquivo de log atual.

        Returns:
            Path do arquivo de log
        """
        return self.log_file

    def get_log_content(self, last_n_lines: Optional[int] = None) -> str:
        """
        Retorna conteúdo do log atual.

        Args:
            last_n_lines: Se especificado, retorna apenas últimas N linhas

        Returns:
            Conteúdo do arquivo de log
        """
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                if last_n_lines:
                    lines = f.readlines()
                    return ''.join(lines[-last_n_lines:])
                else:
                    return f.read()
        except Exception as e:
            return f"Erro ao ler log: {e}"


# Singleton global (opcional)
_logger_instance: Optional[PRSALogger] = None


def get_logger() -> PRSALogger:
    """
    Retorna instância singleton do logger.

    Returns:
        Instância de PRSALogger

    Example:
        >>> logger = get_logger()
        >>> logger.info("Aplicação iniciada")
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = PRSALogger()
    return _logger_instance
