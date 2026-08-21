@echo off
title 🔐 Export GitHub Cloud Secrets
cd /d "%~dp0"
.venv\Scripts\python.exe export_cloud_secrets.py
pause
