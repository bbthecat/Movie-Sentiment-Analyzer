# Deployment script for Movie Sentiment Analyzer
# Usage: .\scripts\deploy.ps1 [staging|production]

param(
    [Parameter(Position=0)]
    [ValidateSet("staging", "production")]
    [string]$Environment = "staging"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

Write-Host "🚀 Deploying Movie Sentiment Analyzer to $Environment environment..." -ForegroundColor Green

# Check if required files exist
$EnvFile = Join-Path $ProjectDir ".env"
if (-not (Test-Path $EnvFile)) {
    Write-Host "❌ Error: .env file not found. Please create it from env.$Environment.example" -ForegroundColor Red
    exit 1
}

# Load environment variables
Get-Content $EnvFile | ForEach-Object {
    if ($_ -match "^([^#][^=]+)=(.*)$") {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
    }
}

# Check if required environment variables are set
$RequiredVars = @("OMDB_API_KEY", "TMDB_API_KEY")
foreach ($Var in $RequiredVars) {
    if (-not [Environment]::GetEnvironmentVariable($Var, "Process")) {
        Write-Host "❌ Error: $Var is not set in .env file" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Environment variables validated" -ForegroundColor Green

# Create necessary directories
$Directories = @(
    "data\movies",
    "data\reviews", 
    "data\analysis",
    "data\samples",
    "logs",
    "ssl"
)

foreach ($Dir in $Directories) {
    $FullPath = Join-Path $ProjectDir $Dir
    if (-not (Test-Path $FullPath)) {
        New-Item -ItemType Directory -Path $FullPath -Force | Out-Null
    }
}

Write-Host "✅ Directories created" -ForegroundColor Green

# Pull latest images
Write-Host "📥 Pulling latest Docker images..." -ForegroundColor Yellow
$ComposeFile = Join-Path $ProjectDir "docker-compose.$Environment.yml"
docker-compose -f $ComposeFile pull

# Stop existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose -f $ComposeFile down

# Start new containers
Write-Host "🚀 Starting new containers..." -ForegroundColor Yellow
docker-compose -f $ComposeFile up -d

# Wait for health check
Write-Host "⏳ Waiting for application to be healthy..." -ForegroundColor Yellow
$Timeout = 60
$Counter = 0
$Healthy = $false

while ($Counter -lt $Timeout -and -not $Healthy) {
    try {
        $Response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -TimeoutSec 2 -ErrorAction Stop
        if ($Response.StatusCode -eq 200) {
            $Healthy = $true
            Write-Host "✅ Application is healthy!" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "Waiting for application... ($Counter/$Timeout)" -ForegroundColor Yellow
        Start-Sleep -Seconds 2
        $Counter += 2
    }
}

if (-not $Healthy) {
    Write-Host "❌ Error: Application failed to become healthy within $Timeout seconds" -ForegroundColor Red
    docker-compose -f $ComposeFile logs
    exit 1
}

# Show deployment status
Write-Host "📊 Deployment Status:" -ForegroundColor Cyan
docker-compose -f $ComposeFile ps

Write-Host "🎉 Deployment to $Environment completed successfully!" -ForegroundColor Green
Write-Host "🌐 Application is available at: http://localhost:8000" -ForegroundColor Cyan
