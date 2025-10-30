Param(
    [string]$EnvFile=".env.local"
)

Write-Host "[run_local_backend] Using env file: $EnvFile"
if (Test-Path $EnvFile) {
    $content = Get-Content $EnvFile
    foreach ($line in $content) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($line.Trim().StartsWith("#")) { continue }
        if (-not ($line -match '=')) { continue }
        $pair = $line.Split("=",2)
        $name = $pair[0].Trim(); $value = $pair[1].Trim()
        if (-not [string]::IsNullOrWhiteSpace($name)) {
            Set-Item -Path Env:$name -Value $value
        }
    }
}

if (-not $env:LOCAL_MODE) { Set-Item Env:LOCAL_MODE "true" }
if (-not $env:DISABLE_KAFKA) { Set-Item Env:DISABLE_KAFKA "true" }
if (-not $env:DISABLE_MINIO) { Set-Item Env:DISABLE_MINIO "true" }
if (-not $env:DISABLE_EMBEDDING) { Set-Item Env:DISABLE_EMBEDDING "true" }

Write-Host "[run_local_backend] Starting FastAPI (sqlite local mode) ..."
if ($env:LOCAL_MODE -and (Test-Path 'backend/requirements-local.txt')) {
    Write-Host "[run_local_backend] Installing local requirements (no Postgres/minio/kafka drivers)" -ForegroundColor Cyan
    pip install -r backend/requirements-local.txt | Write-Host
} else {
    Write-Host "[run_local_backend] Installing full requirements" -ForegroundColor Cyan
    pip install -r backend/requirements.txt | Write-Host
}
python -c "import uvicorn; from backend.app.main import app; uvicorn.run(app, host='0.0.0.0', port=8000)"