@echo off
REM One-click Google login for Search Console MCP (you only do this step)
echo.
echo ========================================
echo  Google Search Console - Login Only
echo ========================================
echo.
echo A browser window will open. Sign in with the Google
echo account that owns your Search Console property.
echo.

set "GCLOUD=%LOCALAPPDATA%\google-cloud-sdk\bin\gcloud.cmd"
if not exist "%GCLOUD%" set "GCLOUD=%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
if not exist "%GCLOUD%" set "GCLOUD=%ProgramFiles(x86)%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
if not exist "%GCLOUD%" set "GCLOUD=%ProgramFiles%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
if not exist "%GCLOUD%" (
  echo ERROR: Google Cloud SDK not found.
  echo Run once: winget install Google.CloudSDK
  echo Or double-click: scripts\gsc_install.bat
  pause
  exit /b 1
)

"%GCLOUD%" auth application-default login --scopes=https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform
if errorlevel 1 (
  echo Login failed or cancelled.
  pause
  exit /b 1
)

echo.
echo Login OK. Running post-login setup...
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\gsc_mcp_finish.ps1"
echo.
echo Done. Restart Cursor, then enable searchconsole-mcp in Settings - Tools ^& MCP
pause
