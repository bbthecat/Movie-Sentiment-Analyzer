# Local Testing Script for Movie Sentiment Analyzer
# Usage: .\test-local.ps1

Write-Host "🧪 Testing Movie Sentiment Analyzer locally..." -ForegroundColor Green

# Test 1: Python Dependencies
Write-Host "`n📦 Testing Python dependencies..." -ForegroundColor Yellow
try {
    py -m pip install -r requirements.txt
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Test 2: Run Tests
Write-Host "`n🧪 Running tests..." -ForegroundColor Yellow
try {
    py -m pytest tests/ -v
    Write-Host "✅ Tests passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Tests failed" -ForegroundColor Red
    exit 1
}

# Test 3: Linting
Write-Host "`n🔍 Running linting..." -ForegroundColor Yellow
try {
    py -m flake8 backend tests --count --select=E9,F63,F7,F82 --show-source --statistics
    Write-Host "✅ Linting passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Linting failed" -ForegroundColor Red
    exit 1
}

# Test 4: Docker Build
Write-Host "`n🐳 Testing Docker build..." -ForegroundColor Yellow
try {
    docker build -t movie-sentiment-analyzer:test .
    Write-Host "✅ Docker build successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    exit 1
}

# Test 5: Run Application
Write-Host "`n🚀 Testing application startup..." -ForegroundColor Yellow
try {
    # Start the app in background
    $job = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        py -c "import uvicorn; uvicorn.run('backend.app:app', host='0.0.0.0', port=8000)"
    }
    
    # Wait a bit for startup
    Start-Sleep -Seconds 5
    
    # Test health endpoint
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Application started successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Application health check failed" -ForegroundColor Red
    }
    
    # Stop the job
    Stop-Job $job
    Remove-Job $job
} catch {
    Write-Host "❌ Application startup failed" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 All local tests completed!" -ForegroundColor Green
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Push to GitHub to test CI/CD pipeline" -ForegroundColor White
Write-Host "2. Check Actions tab in your repository" -ForegroundColor White
Write-Host "3. Verify both CI and Deploy workflows pass" -ForegroundColor White
