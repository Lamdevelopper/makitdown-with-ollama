$ErrorActionPreference = "Stop"

$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
  $pythonCmd = "py"
  $pythonArgs = @("-3")
} else {
  $pythonCmd = "python"
  $pythonArgs = @()
}

& $pythonCmd @pythonArgs -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if ($LASTEXITCODE -ne 0) {
  throw "Se requiere Python 3.10 o superior."
}

& $pythonCmd @pythonArgs -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

try {
  Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method Get -TimeoutSec 2 | Out-Null
  Write-Host "Ollama responde en http://127.0.0.1:11434"
} catch {
  Write-Host "Aviso: Ollama no responde. La app funcionara sin IA hasta que abras Ollama."
}

Write-Host "Listo. Ejecuta .\run.ps1"
