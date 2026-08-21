@echo off
title Push Cosmic Matrix Bot to GitHub
cd /d "%~dp0"
echo ============================================================
echo       PUSHING COSMIC MATRIX BOT TO GITHUB CLOUD
echo ============================================================
echo.

git init
git config --global user.name "editing85198"
git config --global user.email "kuchhbhi85198@gmail.com"

git branch -M main
git add .
git commit -m "Cosmic Matrix 5-in-1 Autopilot Bot"

echo.
echo Enter your GitHub Repository URL (e.g. https://github.com/editing85198-oss/cosmic-matrix-autopilot.git):
set /p REPO_URL="👉 Repo URL: "

git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git push -u origin main --force

echo.
echo ============================================================
echo [SUCCESS] Code pushed to GitHub!
echo Now run: export_cloud_secrets.bat to get your GitHub Secrets!
echo ============================================================
pause
