# Retries Oracle VM creation when Phoenix has capacity (run via Task Scheduler every 6h)
$ErrorActionPreference = "Stop"
$env:Path = "C:\Users\x\.local\bin;C:\Program Files\nodejs;$env:Path"
$log = Join-Path (Resolve-Path (Join-Path $PSScriptRoot "..")) "logs\oracle-retry.log"
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null

function Log($msg) {
    $line = "$(Get-Date -Format o) $msg"
    Add-Content -Path $log -Value $line
    Write-Host $line
}

try {
    $check = oci session validate --region us-phoenix-1 --profile DEFAULT 2>&1 | Out-String
    if ($check -notmatch "Session is valid") {
        Log "OCI session expired - run scripts\oci_login.bat"
        exit 1
    }
    $out = & (Join-Path $PSScriptRoot "oracle_provision.ps1") 2>&1 | Out-String
    Log $out.Trim()
    if ($out -match 'PUBLIC_IP=([0-9.]+)') {
        Log "VM ready at $($Matches[1]) - run scripts\deploy_to_vps.ps1 to upload pipeline"
        exit 0
    }
    if ($out -match "Out of host capacity") {
        Log "Still out of capacity in us-phoenix-1 - will retry later"
        exit 2
    }
} catch {
    Log "ERROR: $($_.Exception.Message)"
    exit 1
}
