import PyInstaller.__main__
import os

# Build the executable
PyInstaller.__main__.run([
    'display_presets.py',
    '--onefile',
    '--windowed',
    '--name=DisplayPresetManager',
    '--add-data=display_presets.json;.',
    '--hidden-import=PyQt5.QtCore',
    '--hidden-import=PyQt5.QtGui',
    '--hidden-import=PyQt5.QtWidgets',
    '--hidden-import=win32api',
    '--hidden-import=win32con',
    '--hidden-import=win32gui',
    '--hidden-import=win32print',
    '--hidden-import=ctypes',
    '--hidden-import=psutil',
])
