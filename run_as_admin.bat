@echo off
echo Starting Display Presets App as Administrator...
powershell -Command "Start-Process python -ArgumentList 'display_presets.py' -Verb RunAs -WorkingDirectory '%~dp0'"
pause 