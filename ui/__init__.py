"""
Módulo de interface do usuário.

Contém componentes visuais reutilizáveis.
"""

from .preview_window import PreviewWindow, show_preview
from .stats_window import StatsWindow

__all__ = ['PreviewWindow', 'show_preview', 'StatsWindow']
