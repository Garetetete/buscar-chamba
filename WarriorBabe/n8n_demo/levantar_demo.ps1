# Levanta la demo de n8n desde cero en un PC nuevo (requiere Docker Desktop abierto).
# Uso, desde esta carpeta:   powershell -ExecutionPolicy Bypass -File .\levantar_demo.ps1
param(
    [string]$Name = "n8n-wb",
    [int]$Port = 5678
)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$volume = "${Name}_data"

function Wait-N8n {
    Write-Host "Esperando a que n8n arranque..."
    for ($i = 0; $i -lt 60; $i++) {
        try {
            Invoke-WebRequest -UseBasicParsing "http://localhost:$Port/healthz" -TimeoutSec 2 | Out-Null
            Start-Sleep -Seconds 3
            return
        } catch { Start-Sleep -Seconds 2 }
    }
    throw "n8n no respondio en 2 minutos. Revisa: docker logs $Name"
}

function Invoke-N8n([string]$cmd) {
    for ($i = 1; $i -le 5; $i++) {
        docker exec $Name sh -c $cmd
        if ($LASTEXITCODE -eq 0) { return }
        Write-Host "  reintentando ($i)..."
        Start-Sleep -Seconds 4
    }
    throw "Fallo: $cmd"
}

docker version --format "{{.Server.Version}}" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Docker no esta corriendo. Abre Docker Desktop y vuelve a intentar." }

if (docker ps -a --format "{{.Names}}" | Where-Object { $_ -eq $Name }) {
    Write-Host "El contenedor $Name ya existe: lo enciendo."
    docker start $Name | Out-Null
    Wait-N8n
} else {
    docker run -d --name $Name -p "${Port}:5678" -v "${volume}:/home/node/.n8n" `
        -e GENERIC_TIMEZONE=America/Bogota -e TZ=America/Bogota `
        docker.n8n.io/n8nio/n8n:2.46.6 | Out-Null
    Wait-N8n

    docker cp credential_webhook_token.json "${Name}:/home/node/cred.json"
    docker cp 1_mock_systems.json "${Name}:/home/node/1.json"
    docker cp 2_solarwinds_to_servicedesk.json "${Name}:/home/node/2.json"
    Invoke-N8n "n8n import:credentials --input=/home/node/cred.json"
    Invoke-N8n "n8n import:workflow --input=/home/node/1.json"
    Invoke-N8n "n8n import:workflow --input=/home/node/2.json"
    Invoke-N8n "n8n publish:workflow --id=wbMockSystems001"
    Invoke-N8n "n8n publish:workflow --id=wbSolarwindsFlow"
    docker restart $Name | Out-Null
    Wait-N8n
}

# n8n responde a /healthz antes de registrar los webhooks; en un PC lento eso tarda.
# Se reintenta el reset hasta que los flujos esten cargados (maximo 3 minutos).
Write-Host "Esperando a que carguen los flujos..."
$ready = $false
for ($i = 0; $i -lt 90; $i++) {
    try {
        Invoke-RestMethod -Method Post -Uri "http://localhost:$Port/webhook/mock/reset" -TimeoutSec 5 | Out-Null
        $ready = $true
        break
    } catch { Start-Sleep -Seconds 2 }
}
if (-not $ready) {
    throw "Los flujos no cargaron. Abre http://localhost:$Port y revisa que los dos flujos esten publicados (Published), o mira: docker logs $Name"
}
Write-Host ""
Write-Host "Listo. Abre http://localhost:$Port (la primera vez pide crear una cuenta local)."
Write-Host "Datos de la demo limpios: la primera alerta crea ARD-1001."
