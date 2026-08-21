@echo off
title Setup 24/7 Cosmic Matrix Dual-Post Tasks
echo ============================================================
echo      ADDING 2 DAILY POSTS TO WINDOWS TASK SCHEDULER
echo ============================================================
echo [*] Slot 1: Morning at 09:00 AM (YouTube + Insta + FB + X + LinkedIn)
echo [*] Slot 2: Evening at 18:00 (6:00 PM) (YouTube + Insta + FB + X + LinkedIn)
echo.

set BATCH_PATH=%~dp0run_scheduled_autopilot.bat

:: 1. Create Morning 9:00 AM Task
schtasks /create /tn "CosmicMatrix_Morning_09AM" /tr "\"%BATCH_PATH%\"" /sc daily /st 09:00 /f

:: 2. Create Evening 18:00 (6:00 PM) Task
schtasks /create /tn "CosmicMatrix_Evening_06PM" /tr "\"%BATCH_PATH%\"" /sc daily /st 18:00 /f

echo.
echo ============================================================
echo [SUCCESS] Both Daily Tasks Scheduled Successfully!
echo [1] Morning Post: 09:00 AM (Daily)
echo [2] Evening Post: 06:00 PM (Daily)
echo ============================================================
pause
