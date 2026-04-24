# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file para Netpoint Report Generator.
Gera executável Windows com ícone personalizado.
"""

import os

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    ['netpoint_report_generator.py'],
    pathex=[BASE_DIR],
    binaries=[],
    datas=[
        # Incluir pasta assets (ícones)
        ('assets', 'assets'),
        # Incluir pasta config
        ('config', 'config'),
        # Incluir pasta core
        ('core', 'core'),
        # Incluir pasta ui
        ('ui', 'ui'),
        # Incluir pasta utils
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'openpyxl.cell._writer',
        'PIL',
        'tkinter',
        'packaging',
        'packaging.version',
        'urllib.request',
        'urllib.error',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Excluir módulos desnecessários para reduzir tamanho
        'matplotlib',
        'scipy',
        'numpy.random._examples',
        'pytest',
        'unittest',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Netpoint Report Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = sem janela de console (GUI apenas)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',  # Ícone da Netpoint
)
