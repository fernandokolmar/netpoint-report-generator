# -*- mode: python ; coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.abspath(SPEC))

extra_datas = []
config_path = os.path.join(BASE_DIR, 'anthropic_config.json')
if os.path.exists(config_path):
    extra_datas.append(('anthropic_config.json', '.'))

a = Analysis(
    ['netpoint_report_generator.py'],
    pathex=[BASE_DIR],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('config', 'config'),
        ('core', 'core'),
        ('ui', 'ui'),
        ('utils', 'utils'),
        ('visual', 'visual'),
    ] + extra_datas,
    hiddenimports=[
        'pandas',
        'openpyxl',
        'openpyxl.cell._writer',
        'PIL',
        'tkinter',
        'packaging',
        'packaging.version',
        'anthropic',
        'httpx',
        'anyio',
        'anyio._backends._asyncio',
        'anyio._backends._trio',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
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
    name='Netpoint Reports',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.png',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Netpoint Reports',
)

app = BUNDLE(
    coll,
    name='Netpoint Reports.app',
    icon='assets/icon.png',
    bundle_identifier='com.netpoint.reportgenerator',
    info_plist={
        'CFBundleName': 'Netpoint Reports',
        'CFBundleDisplayName': 'Netpoint Reports',
        'CFBundleVersion': '1.9.1',
        'CFBundleShortVersionString': '1.9.1',
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',
    },
)
