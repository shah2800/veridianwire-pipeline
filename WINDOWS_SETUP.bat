@echo off
REM Autonomous News Business - Windows Setup Script
REM This script installs all dependencies and sets up the system

echo.
echo ============================================
echo Autonomous News Business - Windows Setup
echo ============================================
echo.

REM Step 1: Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python OK

REM Step 2: Install Python packages
echo.
echo [2/5] Installing Python packages (this may take 5-10 minutes)...
echo Using minimal requirements for faster install...
pip install -r requirements-minimal.txt --user --default-timeout=1000 --retries 5
if errorlevel 1 (
    echo ERROR: Failed to install Python packages
    echo Make sure your internet connection is stable
    echo Try running: pip install --upgrade pip
    echo Then: pip install -r requirements-minimal.txt --user --default-timeout=1000
    pause
    exit /b 1
)
echo Python packages installed OK

REM Step 3: Create .env file
echo.
echo [3/5] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env created. Please edit it with your API keys:
    echo   - OPENAI_API_KEY (from https://platform.openai.com)
    echo   - GROQ_API_KEY (from https://console.groq.com)
    echo   - NEWSAPI_API_KEY (from https://newsapi.org)
    echo   - SUPABASE_URL and SUPABASE_SERVICE_KEY (from https://supabase.com)
    pause
) else (
    echo .env already exists
)

REM Step 4: Install Node.js packages
echo.
echo [4/5] Installing Node.js packages...
call npm cache clean --force
call npm install --legacy-peer-deps --no-audit
if errorlevel 1 (
    echo WARNING: npm install had issues, but continuing...
)
echo Node packages installed

REM Step 5: Summary
echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run the daemon: python daemon.py
echo 3. In another terminal: cd website && npm run dev
echo 4. Open: http://localhost:3000
echo.
pause
