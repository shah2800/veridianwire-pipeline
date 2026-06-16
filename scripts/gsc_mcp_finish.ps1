# Finishes GSC MCP setup after gcloud auth application-default login
$ErrorActionPreference = "Stop"

$gcloudPaths = @(
    "$env:LOCALAPPDATA\google-cloud-sdk\bin\gcloud.cmd",
    "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
    "${env:ProgramFiles(x86)}\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
    "$env:ProgramFiles\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
)
$gcloud = $gcloudPaths | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $gcloud) {
    Write-Host "gcloud not found. Install: winget install Google.CloudSDK"
    exit 1
}

Write-Host "Using gcloud: $gcloud"

function Invoke-Gcloud {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'SilentlyContinue'
    $out = & $gcloud @Args 2>&1
    $ErrorActionPreference = $prev
    return ($out | Out-String).Trim()
}

# Create or pick project
$project = Invoke-Gcloud config get-value project
if (-not $project -or $project -eq "(unset)") {
    $projectId = "veridianwire-gsc-" + (Get-Random -Maximum 99999)
    Write-Host "Creating GCP project: $projectId"
    Invoke-Gcloud projects create $projectId --name="Veridian Wire GSC" | Out-Host
    Invoke-Gcloud config set project $projectId | Out-Host
    $project = $projectId
}

Write-Host "Project: $project"

Write-Host "Enabling Search Console API..."
Invoke-Gcloud services enable searchconsole.googleapis.com --project=$project | Out-Host

Write-Host "Setting quota project for Application Default Credentials..."
Invoke-Gcloud auth application-default set-quota-project $project | Out-Host

Write-Host ""
Write-Host "GSC MCP backend is ready."
Write-Host "Project ID: $project"
Write-Host ""
Write-Host "Next (you): Restart Cursor -> Settings -> Tools & MCP -> enable searchconsole-mcp"
