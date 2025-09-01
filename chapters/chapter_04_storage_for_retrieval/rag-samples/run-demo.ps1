# RAG Demo PowerShell Helper Script
# Chapter 4: Storage for Retrieval - AWS AI Engineering Course
#
# This script provides Windows PowerShell equivalents for Makefile targets
# Usage: .\run-demo.ps1 <command>

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "RAG Demo - AWS AI Engineering Course" -ForegroundColor Cyan
    Write-Host "====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Setup and Environment:" -ForegroundColor Green
    Write-Host "  setup           Install dependencies and validate environment"
    Write-Host "  validate        Validate AWS configuration and connectivity"
    Write-Host ""
    Write-Host "Demo Modes:" -ForegroundColor Green
    Write-Host "  demo-local      Run local FAISS RAG demo"
    Write-Host "  demo-kb         Run Bedrock Knowledge Base demo"
    Write-Host "  agent           Run Strands agent wrapper demo"
    Write-Host ""
    Write-Host "Monitoring:" -ForegroundColor Green
    Write-Host "  monitor-setup   Set up comprehensive CloudWatch monitoring"
    Write-Host "  monitor-status  Check monitoring status"
    Write-Host "  monitor-report  Generate performance report"
    Write-Host ""
    Write-Host "Testing and Maintenance:" -ForegroundColor Green
    Write-Host "  test            Run test suite"
    Write-Host "  clean           Clean up local files and indexes"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Magenta
    Write-Host "  .\run-demo.ps1 demo-local    # Run local FAISS demo"
    Write-Host "  .\run-demo.ps1 setup         # Set up environment"
    Write-Host "  .\run-demo.ps1 monitor-setup # Set up monitoring"
}

function Install-Dependencies {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
}

function Initialize-Environment {
    Write-Host "Setting up RAG demo environment..." -ForegroundColor Yellow
    
    # Install dependencies
    Install-Dependencies
    
    # Validate environment
    Write-Host "Validating environment..." -ForegroundColor Yellow
    python -c "import common; common.validate_environment()" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Environment validation successful!" -ForegroundColor Green
    } else {
        Write-Host "Environment validation had issues. Check configuration." -ForegroundColor Yellow
    }
}

function Test-Environment {
    Write-Host "Validating AWS configuration and connectivity..." -ForegroundColor Yellow
    python -c "import common; common.validate_environment()"
}

function Start-LocalDemo {
    Write-Host "Running local FAISS RAG demo..." -ForegroundColor Yellow
    python rag_vector_local.py
}

function Start-KBDemo {
    Write-Host "Running Bedrock Knowledge Base demo..." -ForegroundColor Yellow
    if (-not (Test-Path ".kb.env")) {
        Write-Host "Knowledge Base not set up. You need to create AWS infrastructure first." -ForegroundColor Red
        Write-Host "Tip: Use the Makefile on Linux/WSL or create infrastructure manually." -ForegroundColor Yellow
        return
    }
    python rag_bedrock_kb.py
}

function Start-Agent {
    Write-Host "Running Strands agent wrapper demo..." -ForegroundColor Yellow
    python strands_agent.py
}

function Initialize-Monitoring {
    Write-Host "Setting up comprehensive monitoring..." -ForegroundColor Yellow
    
    # Check if monitoring config exists
    if (-not (Test-Path "monitoring.env")) {
        Write-Host "Creating monitoring configuration..." -ForegroundColor Yellow
        Copy-Item "monitoring.env.example" "monitoring.env"
        Write-Host "Please edit monitoring.env with your configuration" -ForegroundColor Yellow
        Write-Host "Opening monitoring.env for editing..." -ForegroundColor Cyan
        Start-Process notepad.exe "monitoring.env"
        Write-Host "After editing, run: .\run-demo.ps1 monitor-setup" -ForegroundColor Yellow
        return
    }
    
    python bedrock_kb_monitoring.py --setup-monitoring
}

function Get-MonitoringStatus {
    Write-Host "Checking monitoring status..." -ForegroundColor Yellow
    python bedrock_kb_monitoring.py --status
}

function New-MonitoringReport {
    Write-Host "Generating performance report..." -ForegroundColor Yellow
    python bedrock_kb_monitoring.py --performance-report
}

function Invoke-Tests {
    Write-Host "Running test suite..." -ForegroundColor Yellow
    if (Test-Path "test_*.py") {
        python -m pytest test_*.py -v
    } else {
        Write-Host "No test files found." -ForegroundColor Cyan
    }
}

function Clear-Environment {
    Write-Host "Cleaning up local files and indexes..." -ForegroundColor Yellow
    
    # Remove FAISS index files
    if (Test-Path "faiss_index.faiss") {
        Remove-Item "faiss_index.faiss"
        Write-Host "Removed FAISS index" -ForegroundColor Gray
    }
    
    # Remove document cache
    if (Test-Path "document_chunks.json") {
        Remove-Item "document_chunks.json"
        Write-Host "Removed document cache" -ForegroundColor Gray
    }
    
    # Remove Python cache
    if (Test-Path "__pycache__") {
        Remove-Item "__pycache__" -Recurse -Force
        Write-Host "Removed Python cache" -ForegroundColor Gray
    }
    
    Write-Host "Cleanup complete!" -ForegroundColor Green
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "setup" { Initialize-Environment }
    "validate" { Test-Environment }
    "demo-local" { Start-LocalDemo }
    "demo-kb" { Start-KBDemo }
    "agent" { Start-Agent }
    "monitor-setup" { Initialize-Monitoring }
    "monitor-status" { Get-MonitoringStatus }
    "monitor-report" { New-MonitoringReport }
    "test" { Invoke-Tests }
    "clean" { Clear-Environment }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
        exit 1
    }
}
