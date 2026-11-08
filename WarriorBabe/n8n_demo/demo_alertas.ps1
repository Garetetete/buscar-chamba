# Manda las 3 alertas de la demo y muestra el resultado de cada una.
# Uso, desde esta carpeta:   powershell -ExecutionPolicy Bypass -File .\demo_alertas.ps1
# Opciones:  -Pausa      espera Enter antes de cada alerta (para ir explicando en el video)
#            -SinReset   no borra los tickets anteriores
param(
    [switch]$Pausa,
    [switch]$SinReset,
    [int]$Port = 5678
)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$base = "http://localhost:$Port/webhook"
$h = @{ 'X-Webhook-Token' = 'demo-token-123' }

function Send-Alert([string]$titulo, [string]$archivo) {
    if ($Pausa) { Read-Host "`n[Enter] $titulo" | Out-Null } else { Write-Host "`n$titulo" }
    try {
        $r = Invoke-RestMethod -Method Post -Uri "$base/solarwinds-alert" -Headers $h `
            -ContentType 'application/json' -InFile $archivo
    } catch {
        throw "No respondio el webhook. Corre primero .\levantar_demo.ps1  ($($_.Exception.Message))"
    }
    $r | Format-List | Out-String | ForEach-Object { Write-Host $_.Trim() -ForegroundColor Green }
    Start-Sleep -Seconds 1
}

if (-not $SinReset) {
    Invoke-RestMethod -Method Post -Uri "$base/mock/reset" | Out-Null
    Write-Host "Datos limpios: los tickets empiezan en ARD-1001."
}

Send-Alert "1. Alerta de CPU nueva -> crea el ticket" "alerta_cpu.json"
Send-Alert "2. La misma alerta otra vez -> actualiza el mismo ticket, sin duplicar" "alerta_cpu.json"
Send-Alert "3. Alerta informativa -> se ignora" "alerta_info.json"

Write-Host "`nListo. En n8n: flujo principal -> pestana Executions, ahi estan las 3 ejecuciones."
