# End-to-end: provision Oracle VM (if needed), upload pipeline, start 24/7 daemon
$ErrorActionPreference = "Stop"
$env:Path = "C:\Users\x\.local\bin;C:\Program Files\nodejs;$env:Path"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$sshKey = "$env:USERPROFILE\.ssh\oracle_veridianwire"
$zip = Join-Path $root "deploy\veridianwire-pipeline.zip"
$envFile = Join-Path $root ".env"
$remoteScript = Join-Path $PSScriptRoot "remote_vps_install.sh"

function Ensure-OciSession {
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $check = oci session validate --region us-phoenix-1 --profile DEFAULT 2>&1 | Out-String
    $ErrorActionPreference = $prev
    if ($check -match "Session is valid") {
        Write-Host "Oracle session OK"
        return
    }
    Write-Host ""
    Write-Host "Oracle login required - browser will open."
    Write-Host "Run this if it does not open: scripts\oci_login.bat"
    Write-Host ""
    "DEFAULT" | oci session authenticate --region us-phoenix-1 --profile DEFAULT | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Oracle login failed. Run scripts\oci_login.bat then retry." }
    Write-Host "Oracle session OK"
}

function Get-PublicIp {
    $out = & (Join-Path $PSScriptRoot "oracle_provision.ps1") 2>&1 | Out-String
    Write-Host $out
    if ($out -match 'PUBLIC_IP=([0-9.]+)') { return $Matches[1] }
    throw "Could not get PUBLIC_IP from provisioning output"
}

function Wait-Ssh($ip, $maxSec = 180) {
    Write-Host "Waiting for SSH on $ip..."
    for ($i = 0; $i -lt ($maxSec / 5); $i++) {
        $null = ssh -i $sshKey -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 -o BatchMode=yes "ubuntu@$ip" "echo ok" 2>&1
        if ($LASTEXITCODE -eq 0) { Write-Host "SSH ready"; return }
        Start-Sleep -Seconds 5
    }
    throw "SSH not ready on $ip after ${maxSec}s"
}

Ensure-OciSession

Write-Host "==> Pack project..."
& (Join-Path $PSScriptRoot "pack_for_vps.ps1")

Write-Host "==> Provision / find VM..."
$ip = Get-PublicIp
if (-not $ip) { throw "No public IP" }

Wait-Ssh $ip

Write-Host "==> Upload zip + .env to $ip..."
scp -i $sshKey -o StrictHostKeyChecking=accept-new $zip "ubuntu@${ip}:/tmp/veridianwire-pipeline.zip"
if (-not (Test-Path $envFile)) { throw "Missing .env at $envFile" }
scp -i $sshKey $envFile "ubuntu@${ip}:/tmp/veridianwire.env"
scp -i $sshKey $remoteScript "ubuntu@${ip}:/tmp/remote_vps_install.sh"

Write-Host "==> Remote install + systemd..."
ssh -i $sshKey -o StrictHostKeyChecking=accept-new "ubuntu@$ip" "chmod +x /tmp/remote_vps_install.sh && bash /tmp/remote_vps_install.sh"

Write-Host ""
Write-Host "SUCCESS - pipeline running 24/7 on Oracle VM"
Write-Host "  SSH:  ssh -i $sshKey ubuntu@$ip"
Write-Host "  Logs: ssh -i $sshKey ubuntu@$ip 'sudo tail -f /opt/veridianwire/logs/daemon.log'"
Write-Host "  Status: ssh -i $sshKey ubuntu@$ip 'sudo systemctl status veridianwire-daemon'"
