# PowerShell script to activate Drawlingo conda environment
# This script works even if conda init hasn't been run

Write-Host "Activating Drawlingo environment..." -ForegroundColor Green

# Find conda installation
$CONDA_BASE = "D:\Apps\MiniConda"

# Initialize conda for this session (if not already initialized)
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "Initializing conda for this session..." -ForegroundColor Yellow
    & "$CONDA_BASE\Scripts\conda.exe" shell.powershell hook | Out-String | Invoke-Expression
}

# Activate the environment
conda activate Drawlingo

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate Drawlingo environment!" -ForegroundColor Red
    Write-Host "Please make sure the environment exists: conda env list" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Environment activated successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting Drawlingo..." -ForegroundColor Cyan
python main.py

