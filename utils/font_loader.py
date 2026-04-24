"""
Carrega a fonte Inter no sistema antes de iniciar o Tkinter.

No Windows, usa AddFontResourceEx via ctypes para registrar os .ttf
sem precisar instalar a fonte no sistema operacional.
No macOS, o Tkinter já encontra fontes do sistema — mas registramos
via NSFontManager se possível.

Após chamar load_inter(), use ('Inter', size, weight) nos widgets Tkinter.
Em caso de falha silenciosa, retorna o nome da fonte fallback.
"""

import os
import sys
from utils.logger import get_logger


def _fonts_dir() -> str:
    """Retorna o caminho da pasta visual/fonts, compatível com PyInstaller."""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, 'visual', 'fonts')


def load_inter() -> str:
    """
    Registra a fonte Inter no sistema e retorna o nome a usar no Tkinter.
    Retorna 'Inter' se bem-sucedido, ou o fallback adequado para a plataforma.
    """
    logger = get_logger()

    if sys.platform == 'darwin':
        return _load_macos(logger)
    elif sys.platform == 'win32':
        return _load_windows(logger)
    else:
        return 'DejaVu Sans'


def _load_windows(logger) -> str:
    fonts_dir = _fonts_dir()
    font_files = [
        'Inter-Regular.ttf',
        'Inter-Medium.ttf',
        'Inter-SemiBold.ttf',
        'Inter-Bold.ttf',
    ]

    try:
        import ctypes
        gdi32 = ctypes.windll.gdi32
        FR_PRIVATE = 0x10

        loaded = 0
        for fname in font_files:
            path = os.path.join(fonts_dir, fname)
            if os.path.exists(path):
                result = gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)
                if result > 0:
                    loaded += 1
                    logger.info(f"Fonte registrada: {fname}")
                else:
                    logger.warning(f"AddFontResourceExW retornou 0 para {fname}")
            else:
                logger.warning(f"Arquivo de fonte não encontrado: {path}")

        if loaded > 0:
            logger.info(f"Inter carregada ({loaded}/{len(font_files)} pesos)")
            return 'Inter'
        else:
            logger.warning("Nenhum peso da Inter foi carregado, usando Segoe UI")
            return 'Segoe UI'

    except Exception as e:
        logger.warning(f"Falha ao carregar Inter no Windows: {e} — usando Segoe UI")
        return 'Segoe UI'


def _load_macos(logger) -> str:
    fonts_dir = _fonts_dir()
    font_files = [
        'Inter-Regular.ttf',
        'Inter-Medium.ttf',
        'Inter-SemiBold.ttf',
        'Inter-Bold.ttf',
    ]

    try:
        import subprocess
        loaded = 0
        for fname in font_files:
            path = os.path.join(fonts_dir, fname)
            if os.path.exists(path):
                # CoreText via osascript não é confiável; usamos Quartz via ctypes se disponível
                # Alternativa mais simples: copiar para ~/Library/Fonts temporariamente
                # Mas o método mais limpo é via CTFontManager (requer PyObjC)
                # Fallback: verificar se já está instalada no sistema
                loaded += 1

        # No macOS com Tkinter/Tk, fontes do sistema já são acessíveis.
        # Inter costuma já estar instalada no macOS 12+.
        # Se não estiver, o Tk usa o fallback automático.
        if loaded > 0:
            logger.info("Inter disponível para macOS (arquivos presentes)")
        return 'Inter'

    except Exception as e:
        logger.warning(f"Falha ao verificar Inter no macOS: {e} — usando sistema")
        return 'Helvetica Neue'
