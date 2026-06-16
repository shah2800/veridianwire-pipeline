@echo off
cd /d "%~dp0.."
echo.
echo ========================================
echo  Fix Cursor MCP (all servers)
echo ========================================
echo.

set "PATH=C:\Users\x\.local\bin;C:\Program Files\nodejs;%PATH%"

echo [1/3] Refresh GitHub MCP token (global ~/.cursor/mcp.json)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0mcp\refresh_mcp_env.ps1"
if errorlevel 1 echo WARNING: GitHub token not refreshed - run scripts\github_login.bat

echo.
echo [2/3] Pre-install Search Console MCP...
if not exist "%APPDATA%\npm\node_modules\@vmandic\searchconsole-mcp\dist\server.js" (
  npm install -g @vmandic/searchconsole-mcp
)

echo.
echo [3/3] Pre-warm GitHub MCP remote...
npx -y mcp-remote@latest --version >nul 2>&1

echo.
echo Done. In Cursor:
echo   1. Ctrl+Shift+P -^> Developer: Reload Window
echo   2. Settings - Tools and MCP
echo   3. For Supabase and Vercel: click Connect if shown
echo   4. Toggle any red server OFF then ON
echo.
pause
