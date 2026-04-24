# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file para Netpoint Report Generator - macOS.
Gera aplicativo .app para macOS.
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
    [],
    exclude_binaries=True,
    name='Netpoint Report Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # False = sem janela de console (GUI apenas)
    disable_windowed_traceback=False,
    argv_emulation=True,  # Necessário para macOS
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.png',  # macOS usa PNG ou ICNS
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Netpoint Report Generator',
)

app = BUNDLE(
    coll,
    name='Netpoint Report Generator.app',
    icon='assets/icon.png',
    bundle_identifier='com.netpoint.reportgenerator',
    info_plist={
        'CFBundleName': 'Netpoint Report Generator',
        'CFBundleDisplayName': 'Netpoint Report Generator',
        'CFBundleVersion': '1.7.0',
        'CFBundleShortVersionString': '1.7.0',
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',
    },
)
