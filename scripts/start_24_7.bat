@echo off
REM One-click: install pipeline to run 24/7 on this PC (Windows Task Scheduler)
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_windows_daemon.ps1"
pause
