@echo off
REM GitHub login for gh CLI + GitHub MCP
echo.
echo ========================================
echo  GitHub Login (CLI + MCP)
echo ========================================
echo.
echo Browser will open. Approve access for repo + workflow scopes.
echo.
gh auth login -h github.com -p https -w -s repo,workflow,read:org
if errorlevel 1 (
  echo Login failed.
  pause
  exit /b 1
)
echo.
echo Login OK. Add GITHUB_TOKEN to .env for MCP, then restart Cursor.
echo Token page: https://github.com/settings/tokens
pause
