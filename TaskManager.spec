# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller build spec for Task Manager.

Build with:
    pyinstaller TaskManager.spec

Produces dist/TaskManager/TaskManager.exe (onedir build - recommended for
apps that use PySide6, since onefile builds are slower to start and can
trip some antivirus heuristics). To force a single-file exe instead, add
--onefile when invoking pyinstaller directly on main.py, or see the
commented EXE-only block at the bottom of this file.
"""
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hidden_imports = (
    collect_submodules("pymongo")
    + collect_submodules("bson")
    + collect_submodules("windows_toasts")
)

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("assets/icon.ico", "assets"),
        ("assets/icon.svg", "assets"),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TaskManager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon="assets/icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="TaskManager",
)
