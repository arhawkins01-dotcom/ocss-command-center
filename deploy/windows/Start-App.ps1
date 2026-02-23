# OCSS Command Center - Windows Server Deployment Script
# Production deployment for S:\OCSS\CommandCenter\App\

<#
.SYNOPSIS
    Starts the OCSS Command Center Streamlit application on Windows Server

.DESCRIPTION
    This script performs health checks, sets up the environment, and starts
    the Streamlit application in production mode. Designed for internal
    server deployment at S:\OCSS\CommandCenter\

.NOTES
    Version: 1.0.0
    Author: OCSS IT Team
    Requires: Python 3.10+, PowerShell 5.1+
#>

# Script Configuration
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AppRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$AppDir = Join-Path $AppRoot "app"
$LogsDir = Join-Path $AppRoot "logs"
$DataDir = Join-Path $AppRoot "data"
$ExportsDir = Join-Path $AppRoot "exports"

# Colors for output
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorInfo = "Cyan"

# Logging function
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$Timestamp] [$Level] $Message"
    
    # Create logs directory if it doesn't exist
    if (-not (Test-Path $LogsDir)) {
        New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
    }
    
    $LogFile = Join-Path $LogsDir "deployment_$(Get-Date -Format 'yyyyMMdd').log"
    Add-Content -Path $LogFile -Value $LogMessage
    
    # Also output to console with colors
    switch ($Level) {
        "SUCCESS" { Write-Host $Message -ForegroundColor $ColorSuccess }
        "WARNING" { Write-Host $Message -ForegroundColor $ColorWarning }
        "ERROR"   { Write-Host $Message -ForegroundColor $ColorError }
        default   { Write-Host $Message -ForegroundColor $ColorInfo }
    }
}

# Banner
function Show-Banner {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
    Write-Host "   OCSS Establishment Command Center" -ForegroundColor $ColorInfo
    Write-Host "   Production Deployment Script" -ForegroundColor $ColorInfo
    Write-Host "   Version 1.0.0" -ForegroundColor $ColorInfo
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
    Write-Host ""
}

# Check if running as Administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Health Check: Python Installation
function Test-PythonInstallation {
    Write-Log "Checking Python installation..." "INFO"
    
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            
            if ($major -ge 3 -and $minor -ge 10) {
                Write-Log "✓ Python $pythonVersion found" "SUCCESS"
                return $true
            } else {
                Write-Log "✗ Python version $pythonVersion is too old. Requires Python 3.10+" "ERROR"
                return $false
            }
        }
    } catch {
        Write-Log "✗ Python not found in PATH" "ERROR"
        return $false
    }
    
    return $false
}

# Health Check: Required Directories
function Test-RequiredDirectories {
    Write-Log "Checking required directories..." "INFO"
    
    $requiredDirs = @($AppDir, $LogsDir, $DataDir, $ExportsDir)
    $allExist = $true
    
    foreach ($dir in $requiredDirs) {
        if (-not (Test-Path $dir)) {
            Write-Log "Creating directory: $dir" "WARNING"
            try {
                New-Item -ItemType Directory -Path $dir -Force | Out-Null
                Write-Log "✓ Created directory: $dir" "SUCCESS"
            } catch {
                Write-Log "✗ Failed to create directory: $dir" "ERROR"
                $allExist = $false
            }
        } else {
            Write-Log "✓ Directory exists: $dir" "SUCCESS"
        }
    }
    
    return $allExist
}

# Health Check: Required Files
function Test-RequiredFiles {
    Write-Log "Checking required files..." "INFO"
    
    $appPy = Join-Path $AppDir "app.py"
    $requirementsTxt = Join-Path $AppDir "requirements.txt"
    
    $allExist = $true
    
    if (-not (Test-Path $appPy)) {
        Write-Log "✗ app.py not found at: $appPy" "ERROR"
        $allExist = $false
    } else {
        Write-Log "✓ app.py found" "SUCCESS"
    }
    
    if (-not (Test-Path $requirementsTxt)) {
        Write-Log "✗ requirements.txt not found at: $requirementsTxt" "ERROR"
        $allExist = $false
    } else {
        Write-Log "✓ requirements.txt found" "SUCCESS"
    }
    
    return $allExist
}

# Install/Update Dependencies
function Install-Dependencies {
    Write-Log "Installing/Updating Python dependencies..." "INFO"
    
    $requirementsTxt = Join-Path $AppDir "requirements.txt"
    
    try {
        Set-Location $AppDir
        python -m pip install --upgrade pip --quiet
        python -m pip install -r requirements.txt --quiet
        Write-Log "✓ Dependencies installed successfully" "SUCCESS"
        return $true
    } catch {
        Write-Log "✗ Failed to install dependencies: $_" "ERROR"
        return $false
    }
}

# Check if Streamlit is already running
function Test-StreamlitRunning {
    $streamlitProcess = Get-Process -Name "streamlit" -ErrorAction SilentlyContinue
    return $null -ne $streamlitProcess
}

# Stop existing Streamlit instances
function Stop-StreamlitInstances {
    Write-Log "Checking for existing Streamlit instances..." "INFO"
    
    $streamlitProcesses = Get-Process -Name "streamlit" -ErrorAction SilentlyContinue
    
    if ($streamlitProcesses) {
        Write-Log "Found $($streamlitProcesses.Count) Streamlit instance(s) running" "WARNING"
        Write-Log "Stopping existing instances..." "INFO"
        
        foreach ($proc in $streamlitProcesses) {
            try {
                Stop-Process -Id $proc.Id -Force
                Write-Log "✓ Stopped process ID: $($proc.Id)" "SUCCESS"
            } catch {
                Write-Log "✗ Failed to stop process ID: $($proc.Id)" "ERROR"
            }
        }
        
        Start-Sleep -Seconds 2
    } else {
        Write-Log "✓ No existing Streamlit instances found" "SUCCESS"
    }
}

# Start Streamlit Application
function Start-StreamlitApp {
    param(
        [int]$Port = 8501
    )
    
    Write-Log "Starting OCSS Command Center..." "INFO"
    
    $appPy = Join-Path $AppDir "app.py"
    
    # Set environment variable for production
    $env:OCSS_ENV = "production"
    
    try {
        Set-Location $AppDir
        
        Write-Log "Streamlit application starting on port $Port" "INFO"
        Write-Log "Access the application at: http://localhost:$Port" "SUCCESS"
        Write-Log "Press Ctrl+C to stop the application" "INFO"
        Write-Host ""
        
        # Start Streamlit
        streamlit run $appPy --server.port $Port --server.headless true
        
    } catch {
        Write-Log "✗ Failed to start Streamlit: $_" "ERROR"
        return $false
    }
}

# Main execution flow
function Main {
    Show-Banner
    
    Write-Log "Starting deployment checks..." "INFO"
    Write-Host ""
    
    # Check if running as admin (optional, but recommended)
    if (-not (Test-Administrator)) {
        Write-Log "WARNING: Not running as Administrator. Some operations may fail." "WARNING"
    }
    
    # Run health checks
    $pythonOk = Test-PythonInstallation
    $dirsOk = Test-RequiredDirectories
    $filesOk = Test-RequiredFiles
    
    Write-Host ""
    
    if (-not ($pythonOk -and $dirsOk -and $filesOk)) {
        Write-Log "Health checks failed. Please resolve the errors above." "ERROR"
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor $ColorWarning
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
    
    Write-Log "All health checks passed!" "SUCCESS"
    Write-Host ""
    
    # Stop existing instances
    Stop-StreamlitInstances
    Write-Host ""
    
    # Install dependencies
    $depsOk = Install-Dependencies
    
    if (-not $depsOk) {
        Write-Log "Failed to install dependencies. Exiting..." "ERROR"
        exit 1
    }
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor $ColorSuccess
    Write-Host "   Ready to start application!" -ForegroundColor $ColorSuccess
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor $ColorSuccess
    Write-Host ""
    
    # Start the application
    Start-StreamlitApp -Port 8501
}

# Run the script
Main
