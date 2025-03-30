# screenspeak.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
from os import path
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Set the base directory to your project root
project_root = path.abspath(".")

a = Analysis(
    ['scripts/program.py'],  # main entry point
    pathex=[project_root],
    binaries=[],
    datas=[
        # Include images folder (Windows: use semicolon as separator)
        ('images', 'images'),
        # Include tesseract folder with tesseract.exe
        ('tesseract', 'tesseract'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=["old_program", "unit_test"],  # Exclude development files
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ScreenSpeak',   # Name of .exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True      # Set to False to remove the console
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='ScreenSpeak'
)
