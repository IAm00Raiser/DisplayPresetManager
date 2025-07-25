@echo off
echo Packaging Display Preset Manager...
echo.

REM Create distribution directory
if not exist "dist" mkdir dist

REM Copy files to dist
copy "display_presets.py" "dist\"
copy "display_manager.py" "dist\"
copy "display_presets.json" "dist\"
copy "requirements.txt" "dist\"
copy "README.md" "dist\"
copy "LICENSE.txt" "dist\"
copy "launch.bat" "dist\"
copy "run_as_admin.bat" "dist\"

REM Create zip file
powershell Compress-Archive -Path "dist\*" -DestinationPath "DisplayPresetManager-v1.0.0.zip" -Force

echo.
echo Package created: DisplayPresetManager-v1.0.0.zip
pause
