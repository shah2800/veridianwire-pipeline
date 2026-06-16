# Provision Oracle Always Free VM (us-phoenix-1) - uses JSON files for OCI CLI
$ErrorActionPreference = "Stop"
$env:Path = "C:\Users\x\.local\bin;C:\Program Files\nodejs;$env:Path"

$TENANCY = "ocid1.tenancy.oc1..aaaaaaaaoay3mz5ydmwmbdn3x3o4zz3fcyxunsjj6og447ilr24fyrgtzxqa"
$REGION = "us-phoenix-1"
$AUTH = @("--auth", "security_token", "--profile", "DEFAULT", "--region", $REGION)
$TMP = Join-Path $env:TEMP "oci-provision"
New-Item -ItemType Directory -Force -Path $TMP | Out-Null
$SSH_PUB = (Get-Content "$env:USERPROFILE\.ssh\oracle_veridianwire.pub" -Raw).Trim()

function Invoke-Oci {
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $out = & oci @args 2>&1
    $code = $LASTEXITCODE
    $ErrorActionPreference = $prev
    if ($code -ne 0) { throw ($out | Out-String) }
    return $out
}

function Write-OciJsonFile($path, $json) {
    [System.IO.File]::WriteAllText($path, $json, [System.Text.UTF8Encoding]::new($false))
    return ($path -replace '\\', '/')
}

function Oci-JsonArray($items, $name) {
    $p = Join-Path $TMP $name
    $json = ConvertTo-Json -InputObject @($items) -Depth 8 -Compress
    return Write-OciJsonFile $p $json
}

function Oci-JsonObject($obj, $name) {
    $p = Join-Path $TMP $name
    $json = ConvertTo-Json -InputObject $obj -Depth 8 -Compress
    return Write-OciJsonFile $p $json
}

Write-Host "==> Check existing instance..."
$existing = Invoke-Oci compute instance list --compartment-id $TENANCY @AUTH --output json | ConvertFrom-Json
$found = $existing.data | Where-Object { $_.'display-name' -eq 'veridianwire-pipeline' } | Select-Object -First 1
if ($found) {
    $vnics = Invoke-Oci compute vnic-attachment list --compartment-id $TENANCY --instance-id $found.id @AUTH --output json | ConvertFrom-Json
    $vnic = Invoke-Oci network vnic get --vnic-id $vnics.data[0].'vnic-id' @AUTH --output json | ConvertFrom-Json
    Write-Host ("PUBLIC_IP=" + $vnic.data.'public-ip')
    exit 0
}

$ad = (Invoke-Oci iam availability-domain list --compartment-id $TENANCY @AUTH --output json | ConvertFrom-Json).data[0].name

Write-Host "==> VCN..."
$vcns = Invoke-Oci network vcn list --compartment-id $TENANCY @AUTH --output json | ConvertFrom-Json
$vcn = $vcns.data | Where-Object { $_.'display-name' -eq 'veridianwire-vcn' } | Select-Object -First 1
if (-not $vcn) {
    $vcn = (Invoke-Oci network vcn create --compartment-id $TENANCY --cidr-block "10.0.0.0/16" --display-name "veridianwire-vcn" @AUTH --output json | ConvertFrom-Json).data
}
$VCN_ID = $vcn.id
$RT_ID = $vcn.'default-route-table-id'
$SL_ID = $vcn.'default-security-list-id'

Write-Host "==> Internet gateway..."
$igws = Invoke-Oci network internet-gateway list --compartment-id $TENANCY --vcn-id $VCN_ID @AUTH --output json | ConvertFrom-Json
$igw = $igws.data | Select-Object -First 1
if (-not $igw) {
    $igw = (Invoke-Oci network internet-gateway create --compartment-id $TENANCY --vcn-id $VCN_ID --is-enabled true --display-name "veridianwire-igw" @AUTH --output json | ConvertFrom-Json).data
}

Write-Host "==> Route table (0.0.0.0/0 -> IGW)..."
$rt = Invoke-Oci network route-table get --rt-id $RT_ID @AUTH --output json | ConvertFrom-Json
$hasRoute = $rt.data.'route-rules' | Where-Object { $_.destination -eq '0.0.0.0/0' -and $_.'network-entity-id' -eq $igw.id }
if (-not $hasRoute) {
    $routes = Oci-JsonArray @{ cidrBlock = "0.0.0.0/0"; networkEntityId = $igw.id } "routes.json"
    Invoke-Oci network route-table update --rt-id $RT_ID --route-rules "file://$routes" --force @AUTH | Out-Null
}

Write-Host "==> Security list (SSH 22)..."
$ingress = Oci-JsonArray @{ protocol = "6"; source = "0.0.0.0/0"; tcpOptions = @{ destinationPortRange = @{ min = 22; max = 22 } } } "ingress.json"
$egress = Oci-JsonArray @{ protocol = "all"; destination = "0.0.0.0/0"; isStateless = $false } "egress.json"
Invoke-Oci network security-list update --security-list-id $SL_ID --ingress-security-rules "file://$ingress" --egress-security-rules "file://$egress" --force @AUTH | Out-Null

Write-Host "==> Ubuntu ARM image..."
$images = Invoke-Oci compute image list --compartment-id $TENANCY @AUTH --operating-system "Canonical Ubuntu" --operating-system-version "22.04" --shape "VM.Standard.A1.Flex" --all --output json | ConvertFrom-Json
$image = $images.data | Where-Object { $_.'display-name' -match 'aarch64' } | Select-Object -First 1
if (-not $image) { throw "No Ubuntu 22.04 aarch64 image found for VM.Standard.A1.Flex" }

Write-Host "==> Subnet..."
$subnets = Invoke-Oci network subnet list --compartment-id $TENANCY --vcn-id $VCN_ID @AUTH --output json | ConvertFrom-Json
$subnet = $subnets.data | Where-Object { $_.'display-name' -eq 'veridianwire-subnet' } | Select-Object -First 1
if (-not $subnet) {
    $slJson = Oci-JsonArray $SL_ID "subnet-sls.json"
    $subnet = (Invoke-Oci network subnet create --compartment-id $TENANCY --vcn-id $VCN_ID --cidr-block "10.0.1.0/24" --display-name "veridianwire-subnet" --availability-domain $ad --route-table-id $RT_ID --security-list-ids "file://$slJson" --prohibit-public-ip-on-vnic false @AUTH --output json | ConvertFrom-Json).data
}

Write-Host "==> Launch VM..."
$meta = Oci-JsonObject @{ ssh_authorized_keys = $SSH_PUB } "metadata.json"
$shape = Oci-JsonObject @{ ocpus = 1; memoryInGBs = 6 } "shape.json"
$launch = $null
for ($attempt = 1; $attempt -le 3; $attempt++) {
    try {
        Write-Host "Launch attempt $attempt/3..."
        $launch = Invoke-Oci compute instance launch `
          --compartment-id $TENANCY `
          --availability-domain $ad `
          --display-name "veridianwire-pipeline" `
          --shape "VM.Standard.A1.Flex" `
          --shape-config "file://$shape" `
          --image-id $image.id `
          --subnet-id $subnet.id `
          --assign-public-ip true `
          --metadata "file://$meta" `
          @AUTH --output json | ConvertFrom-Json
        break
    } catch {
        Write-Host $_.Exception.Message
        if ($attempt -eq 3) { throw }
        Write-Host "Retrying in 30s..."
        Start-Sleep -Seconds 30
    }
}

$INSTANCE_ID = $launch.data.id
Write-Host "Instance: $INSTANCE_ID - waiting RUNNING..."
for ($i = 0; $i -lt 36; $i++) {
    Start-Sleep -Seconds 10
    $st = Invoke-Oci compute instance get --instance-id $INSTANCE_ID @AUTH --query 'data."lifecycle-state"' --raw-output
    if ($st -eq "RUNNING") { break }
}
Start-Sleep -Seconds 15
$vnics = Invoke-Oci compute vnic-attachment list --compartment-id $TENANCY --instance-id $INSTANCE_ID @AUTH --output json | ConvertFrom-Json
$vnic = Invoke-Oci network vnic get --vnic-id $vnics.data[0].'vnic-id' @AUTH --output json | ConvertFrom-Json
$pubIp = $vnic.data.'public-ip'
Write-Host "PUBLIC_IP=$pubIp"
