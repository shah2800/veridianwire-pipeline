@echo off
echo.
echo ========================================
echo  Fix Cursor MCP (Windows startup bug)
echo ========================================
echo.
echo Step 1: Pre-warming MCP packages...
set "PATH=C:\Users\x\.local\bin;C:\Program Files\nodejs;%PATH%"
if not exist "%APPDATA%\npm\node_modules\@vmandic\searchconsole-mcp\dist\server.js" (
  echo Installing Search Console MCP...
  npm install -g @vmandic/searchconsole-mcp
)
echo Warming Oracle MCP cache...
uvx oracle.oci-api-mcp-server --version >nul 2>&1
echo.
echo Step 2: In Cursor, press Ctrl+Shift+P
echo         Type: Developer: Reload Window
echo         Press Enter
echo.
echo Step 3: Wait 10 seconds, then Settings - Tools ^& MCP
echo         Toggle each red server OFF then ON
echo.
echo If still red: File - Exit (full quit), reopen Cursor, wait 90 sec, reload again.
echo.
pause
