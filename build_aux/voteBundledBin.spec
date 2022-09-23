# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# inserting current dir where votm package exists
sys.path.insert(0, str(Path(".").resolve()))

from build_aux._data import *
from build_aux._data import __version__

block_cipher = None


a = Analysis(
    [BASE_DIR.resolve().joinpath("vote.py")],
    pathex=[BASE_DIR_ABS],
    binaries=[],
    datas=[],
    hiddenimports=['toml'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries
    + [
        DATA_FILES[i]
        for i in DATA_FILES
        if i in ["app.gif", "bg.png", "logo.png", "LICENSE"]
    ],
    a.zipfiles,
    a.datas,
    [],
    name="vote_bin_" + __version__,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=["vcruntime140.dll"],
    runtime_tmpdir=None,
    console=False,
    icon=ICON_PATH,
    uac_admin=False,
)
