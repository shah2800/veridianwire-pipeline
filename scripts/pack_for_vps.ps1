# Pack project for VPS upload (excludes secrets, node_modules, caches)
$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$out = Join-Path $root "deploy\veridianwire-pipeline.zip"
New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
if (Test-Path $out) { Remove-Item $out -Force }

$staging = Join-Path $env:TEMP "veridianwire-pack"
if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Force -Path $staging | Out-Null

$skip = @('node_modules', '.next', '.venv', '__pycache__', '.git', 'logs', 'deploy')
Get-ChildItem $root -Force | Where-Object { $_.Name -notin $skip } | ForEach-Object {
    Copy-Item $_.FullName -Destination (Join-Path $staging $_.Name) -Recurse -Force -ErrorAction SilentlyContinue
}
Remove-Item (Join-Path $staging ".env") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $staging "website\.env.local") -Force -ErrorAction SilentlyContinue
Get-ChildItem $staging -Recurse -Directory -Filter node_modules -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem $staging -Recurse -Directory -Filter .next -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $out -Force
Remove-Item $staging -Recurse -Force
Write-Host "Packed: $out ($([math]::Round((Get-Item $out).Length/1MB, 1)) MB)"
