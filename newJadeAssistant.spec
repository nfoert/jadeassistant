# -*- mode: python -*-

block_cipher = None


a = Analysis(['newJadeAssistant.py'],
             pathex=['newJadeAssistant.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [
		('main.ui','./ui/main.ui', "DATA"),
		('medium.ui','./ui/medium.ui', "DATA"),
		('small.ui','./ui/small.ui', "DATA"),
		('mini.ui','./ui/mini.ui', "DATA"),
		('sizeSelect.ui','./ui/sizeSelect.ui', "DATA")
]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Jade Assistant',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon="favicon.ico")