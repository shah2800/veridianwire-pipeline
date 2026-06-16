@echo off
cd /d "%~dp0.."
start "" /B ".venv\Scripts\python.exe" start_daemon.py >> logs\daemon.log 2>&1
