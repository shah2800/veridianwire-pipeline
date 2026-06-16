@echo off
REM One-click Oracle Cloud login for OCI MCP (browser sign-in)
echo.
echo ========================================
echo  Oracle Cloud - Login for MCP
echo  Region: US West (Phoenix) = us-phoenix-1
echo ========================================
echo.

set "REGION=us-phoenix-1"
set "OCI="

where oci >nul 2>&1 && set "OCI=oci"
if not defined OCI if exist "%USERPROFILE%\.local\bin\oci.exe" set "OCI=%USERPROFILE%\.local\bin\oci.exe"
if not defined OCI if exist "%LOCALAPPDATA%\Programs\Python\Python313\Scripts\oci.exe" set "OCI=%LOCALAPPDATA%\Programs\Python\Python313\Scripts\oci.exe"

if not defined OCI (
  echo Installing OCI CLI via uv...
  set "PATH=%USERPROFILE%\.local\bin;%PATH%"
  uv tool install oci-cli
  if exist "%USERPROFILE%\.local\bin\oci.exe" set "OCI=%USERPROFILE%\.local\bin\oci.exe"
)

if not defined OCI (
  echo ERROR: OCI CLI not found after install.
  echo Run: uv tool install oci-cli
  pause
  exit /b 1
)

echo Using OCI CLI: %OCI%
echo Region: %REGION%
echo.
echo Browser will open — sign in with your Oracle Cloud account.
echo Tenancy name = your cloud account name when prompted.
echo.

"%OCI%" session authenticate --region %REGION% --profile DEFAULT

if errorlevel 1 (
  echo Login failed or cancelled.
  pause
  exit /b 1
)

echo.
echo Login OK. Config: %USERPROFILE%\.oci\config
echo Restart Cursor, enable oracle-oci-api-mcp-server in Settings - Tools ^& MCP
pause
