# OCSS Command Center - Windows Launcher
# This script starts the OCSS Command Center application and opens it in your browser

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OCSS Command Center - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script's directory and navigate to app folder
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AppDir = Join-Path (Split-Path -Parent (Split-Path -Parent $ScriptDir)) "app"

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Navigate to app directory
Set-Location $AppDir
Write-Host "✓ App directory: $AppDir" -ForegroundColor Green

# Check if dependencies are installed
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$pipList = pip list 2>&1 | Out-String
if ($pipList -notmatch "streamlit") {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✓ Dependencies already installed" -ForegroundColor Green
}

# Start the application
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting OCSS Command Center..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The application will open in your browser at:" -ForegroundColor Green
Write-Host "  http://localhost:8501" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

# Launch Streamlit
streamlit run app.py --server.headless=false
