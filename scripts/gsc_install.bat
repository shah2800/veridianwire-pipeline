@echo off
REM One-time Google Cloud SDK install (needs Admin UAC click)
echo.
echo Installing Google Cloud SDK via winget...
echo When Windows asks, click YES on the Administrator prompt.
echo.
winget install Google.CloudSDK --accept-package-agreements --accept-source-agreements
if errorlevel 1 (
  echo.
  echo Install failed. Download manually:
  echo https://cloud.google.com/sdk/docs/install
  pause
  exit /b 1
)
echo.
echo Install OK. Next: double-click scripts\gsc_login.bat
pause
