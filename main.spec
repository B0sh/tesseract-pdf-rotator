# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas=[
    ('/opt/homebrew/bin/tesseract', 'tesseract'),
    ('/opt/homebrew/share/tessdata/', 'tessdata')
]
datas += collect_data_files('fitz')
datas += collect_data_files('pytesseract')



a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['opencv-python', 'PyMuPDF', 'fitz'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Walden PDF',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Walden PDF',
)
app = BUNDLE(
    coll,
    name='Walden PDF.app',
    icon=None,
    bundle_identifier=None,
)
