@echo off
echo ========================================
echo Starting Autonomous News Website
echo ========================================

cd /d "%~dp0"

echo Installing dependencies (project root)...
call npm install
if errorlevel 1 (
    echo npm install failed. Check your internet connection and try again.
    pause
    exit /b 1
)

echo Creating website environment file...
python scripts\create_website_env.py

echo.
echo ========================================
echo Starting Next.js dev server...
echo ========================================
echo.
echo Website: http://localhost:3000
echo Press Ctrl+C to stop
echo ========================================
echo.

call npm run dev
