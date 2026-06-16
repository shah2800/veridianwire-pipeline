# Install Veridian Wire pipeline as a Windows scheduled task (runs at startup, auto-restarts)
# Run once in PowerShell (as Administrator for startup trigger):
#   powershell -ExecutionPolicy Bypass -File scripts\install_windows_daemon.ps1
$ErrorActionPreference = "Stop"

$rootPath = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = $null
foreach ($candidate in @("py -3.12", "py -3.11", "python")) {
    try {
        $ver = Invoke-Expression "$candidate -c `"import sys; print(sys.version_info[:2])`"" 2>$null
        if ($ver) { $python = $candidate; break }
    } catch {}
}
if (-not $python) { throw "Install Python 3.11 or 3.12 first." }

$venvDir = Join-Path $rootPath ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$daemonScript = Join-Path $rootPath "start_daemon.py"
$taskName = "VeridianWirePipeline"
$logDir = Join-Path $rootPath "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

Write-Host "==> Python venv at $rootPath (using $python)"
if (-not (Test-Path $venvPython)) {
    Invoke-Expression "$python -m venv `"$venvDir`""
    if (-not (Test-Path $venvPython)) { throw "Failed to create venv with $python" }
}

& $venvPython -m pip install -q --upgrade pip
& $venvPython -m pip install -q -r (Join-Path $rootPath "requirements-daemon.txt")

if (-not (Test-Path (Join-Path $rootPath ".env"))) {
    throw "Missing .env in project root. Copy .env.example and add API keys first."
}

Write-Host "==> Register auto-start (logon + Startup folder)..."
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

$action = New-ScheduledTaskAction `
    -Execute $venvPython `
    -Argument "`"$daemonScript`"" `
    -WorkingDirectory $rootPath

$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Days 3650)

$registered = $false
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -User $env:USERNAME `
        -Description "Veridian Wire autonomous news pipeline (24/7)" | Out-Null
    $registered = $true
    Write-Host "Scheduled task registered (runs at logon)."
} catch {
    Write-Host "Scheduled task skipped (need admin): $($_.Exception.Message)"
}

$startup = [Environment]::GetFolderPath("Startup")
$shortcutPath = Join-Path $startup "VeridianWirePipeline.lnk"
$runner = Join-Path $rootPath "scripts\run_daemon_background.bat"
$WshShell = New-Object -ComObject WScript.Shell
$sc = $WshShell.CreateShortcut($shortcutPath)
$sc.TargetPath = $runner
$sc.WorkingDirectory = $rootPath
$sc.WindowStyle = 7
$sc.Description = "Veridian Wire news pipeline"
$sc.Save()
Write-Host "Startup shortcut: $shortcutPath"

Write-Host "==> Start daemon now (background)..."
Start-Process -FilePath $venvPython -ArgumentList "`"$daemonScript`"" -WorkingDirectory $rootPath -WindowStyle Hidden
Write-Host ""
Write-Host "Installed. Pipeline starts at logon and is running now."
Write-Host "Logs: $logDir\daemon.log"
if ($registered) {
    Write-Host "Task: Get-ScheduledTask -TaskName $taskName"
}
