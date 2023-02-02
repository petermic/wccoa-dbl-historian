# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['db_plot.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += Tree("C:\\Users\\Michael Peters\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\plotly\\package_data\\", ".\\plotly\\package_data")
a.datas += Tree("C:\\Users\\Michael Peters\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\plotly\\validators\\scatter\\", ".\\plotly\\validators\\scatter")
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='db_plot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='db_plot')
