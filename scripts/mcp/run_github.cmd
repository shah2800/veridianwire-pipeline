@echo off
REM GitHub MCP via official hosted endpoint (no Docker required)
set "TOKEN="
if defined GITHUB_TOKEN set "TOKEN=%GITHUB_TOKEN%"
if not defined TOKEN if exist "%~dp0..\..\.env" (
  for /f "usebackq tokens=1,* delims==" %%A in (`findstr /B /I "GITHUB_TOKEN=" "%~dp0..\..\.env" 2^>nul`) do set "TOKEN=%%B"
)
if not defined TOKEN (
  where gh >nul 2>&1 && for /f "delims=" %%T in ('gh auth token 2^>nul') do set "TOKEN=%%T"
)
if not defined TOKEN (
  echo ERROR: Run scripts\github_login.bat first, or set GITHUB_TOKEN in .env
  echo Token: https://github.com/settings/tokens ^(scopes: repo, workflow^)
  exit /b 1
)
npx -y mcp-remote@latest https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer %TOKEN%"
