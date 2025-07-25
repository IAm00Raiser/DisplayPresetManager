@echo off
echo Building Display Preset Manager...
echo.

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Build the executable
python build_exe.py

echo.
echo Build complete! Check the dist/ folder for the executable.
pause
