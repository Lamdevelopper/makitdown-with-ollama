$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
  Write-Host "No encontre .venv. Ejecutando setup.ps1..."
  & .\setup.ps1
}

Start-Process "http://127.0.0.1:8000"
& .\.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
