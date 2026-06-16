# Push project to GitHub + set Actions secrets for 24/7 cloud pipeline (not local PC)
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$envFile = Join-Path $root ".env"
$repoName = "veridianwire-pipeline"

Set-Location $root

function Read-DotEnv($path) {
    $vars = @{}
    if (-not (Test-Path $path)) { return $vars }
    Get-Content $path | ForEach-Object {
        if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
        $k, $v = $_ -split '=', 2
        $vars[$k.Trim()] = $v.Trim().Trim('"')
    }
    return $vars
}

function Ensure-GhAuth {
    gh auth status 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "GitHub login required - browser will open."
        Write-Host "Run: scripts\github_login.bat"
        Write-Host ""
        gh auth login -h github.com -p https -w -s repo,workflow,read:org
        if ($LASTEXITCODE -ne 0) { throw "GitHub login failed." }
    }
    Write-Host "GitHub CLI authenticated."
}

function Stop-LocalDaemon {
    Write-Host "==> Stopping local PC daemon (cloud will take over)..."
    Get-ScheduledTask -TaskName VeridianWirePipeline -ErrorAction SilentlyContinue |
        Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue
    $startup = Join-Path ([Environment]::GetFolderPath("Startup")) "VeridianWirePipeline.lnk"
    if (Test-Path $startup) { Remove-Item $startup -Force }
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -match 'start_daemon\.py' } |
        ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
}

Write-Host "==> Veridian Wire - GitHub cloud 24/7 setup"
Ensure-GhAuth
Stop-LocalDaemon

if (-not (Test-Path $envFile)) { throw "Missing .env at $envFile" }
$envVars = Read-DotEnv $envFile

$secretMap = @{
    GROQ_API_KEY         = $envVars['GROQ_API_KEY']
    OPENAI_API_KEY       = $envVars['OPENAI_API_KEY']
    NEWSAPI_API_KEY      = $envVars['NEWSAPI_API_KEY']
    SUPABASE_URL         = $envVars['SUPABASE_URL']
    SUPABASE_SERVICE_KEY = $envVars['SUPABASE_SERVICE_KEY']
    SUPABASE_ANON_KEY      = $envVars['SUPABASE_ANON_KEY']
    SERPAPI_API_KEY      = $envVars['SERPAPI_API_KEY']
}

if (-not (Test-Path (Join-Path $root ".git"))) {
    git init -b main
}

$hasOrigin = [bool](git remote 2>$null | Where-Object { $_ -eq 'origin' })
if (-not $hasOrigin) {
    $user = gh api user -q .login
    Write-Host "==> Creating GitHub repo: $user/$repoName"
    gh repo create $repoName --private --source=. --remote=origin --description "Veridian Wire autonomous news pipeline" 2>$null
    if ($LASTEXITCODE -ne 0) {
        gh repo create "$user/$repoName" --private --description "Veridian Wire autonomous news pipeline"
        git remote add origin "https://github.com/$user/$repoName.git"
    }
}

Write-Host "==> Setting GitHub Actions secrets from .env..."
foreach ($entry in $secretMap.GetEnumerator()) {
    if ([string]::IsNullOrWhiteSpace($entry.Value)) {
        Write-Host "  skip $($entry.Key) (empty)"
        continue
    }
    $entry.Value | gh secret set $entry.Key --repo (gh repo view --json nameWithOwner -q .nameWithOwner)
    Write-Host "  set $($entry.Key)"
}

Write-Host "==> Commit and push..."
git add -A
git status --short
$status = git status --porcelain
if ($status) {
    git commit -m "Enable GitHub Actions 24/7 news pipeline in the cloud."
}
git push -u origin main

$repoUrl = gh repo view --json url -q .url
Write-Host ""
Write-Host "SUCCESS - pipeline runs in GitHub cloud every 30 minutes"
Write-Host "  Repo:    $repoUrl"
Write-Host "  Actions: $repoUrl/actions"
Write-Host "  Manual:  gh workflow run pipeline-cron.yml"
Write-Host ""
Write-Host "Reload Cursor to connect GitHub MCP (Settings -> Tools & MCP)."
