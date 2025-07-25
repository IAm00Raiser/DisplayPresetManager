@echo off
echo Installing Display Presets App dependencies...
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Setup complete! You can now run the app using:
echo   - run_as_admin.bat (recommended)
echo   - python display_presets.py (as administrator)
echo.
pause 