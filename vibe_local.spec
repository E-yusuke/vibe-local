# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller specification file for vibe-local.
This file is used to build the standalone EXE application.

Usage:
    pyinstaller vibe_local.spec
"""

import os
import sys

# Get the absolute path of this spec file's directory
spec_dir = os.path.dirname(os.path.abspath(__file__))

a = Analysis(
    [os.path.join(spec_dir, 'vibe_local_chat.py')],
    pathex=[spec_dir],
    binaries=[],
    datas=[
        # Include any data files needed (none currently)
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[
        # Exclude unnecessary modules to reduce EXE size
        'matplotlib',
        'numpy',
        'scipy',
        'sklearn',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='vibe-local',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console window (required for interactive chat)
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Optional: add icon.ico here if you have one
)

# Create a folder (onedir mode) - recommended for distribution
# Uncomment if you prefer one-folder distribution instead of one-file
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='vibe-local'
# )
