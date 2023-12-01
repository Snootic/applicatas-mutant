# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['__init__.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    Tree('./telas', prefix='telas/'),
    Tree('./data', prefix='data/'),
    Tree('./bd', prefix='bd/'),
    [],
    name='Peraeque',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['data/icone.ico']
)
