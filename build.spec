# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file - Simplificado para Sistemas Óticas
"""

import sys
import os

block_cipher = None

# Caminhos absolutos
project_root = r'c:\Users\lucas\Desktop\semi_final'
app_dir = os.path.join(project_root, 'app')

# Dados a embutir
datas = [
    (os.path.join(app_dir, 'static'), 'app/static'),
    (os.path.join(app_dir, 'templates'), 'app/templates'),
    (os.path.join(project_root, 'data.db'), '.'),
]

a = Analysis(
    [os.path.join(project_root, 'main.py')],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'flask',
        'flask_login',
        'jinja2',
        'werkzeug',
        'dotenv',
        'openpyxl',
        'reportlab',
        'bcrypt',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Gestao_Otica',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
