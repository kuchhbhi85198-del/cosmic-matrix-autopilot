@echo off
cd /d "%~dp0"
"%~dp0.venv\Scripts\python.exe" "%~dp0autopilot.py" --privacy public >> "%~dp0logs\scheduler_output.log" 2>&1
