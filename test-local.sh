#!/bin/bash
# Local Testing Script for Movie Sentiment Analyzer
# Usage: ./test-local.sh

echo "🧪 Testing Movie Sentiment Analyzer locally..."

# Test 1: Python Dependencies
echo ""
echo "📦 Testing Python dependencies..."
if python -m pip install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Test 2: Run Tests
echo ""
echo "🧪 Running tests..."
if python -m pytest tests/ -v; then
    echo "✅ Tests passed"
else
    echo "❌ Tests failed"
    exit 1
fi

# Test 3: Linting
echo ""
echo "🔍 Running linting..."
if python -m flake8 backend tests --count --select=E9,F63,F7,F82 --show-source --statistics; then
    echo "✅ Linting passed"
else
    echo "❌ Linting failed"
    exit 1
fi

# Test 4: Docker Build
echo ""
echo "🐳 Testing Docker build..."
if docker build -t movie-sentiment-analyzer:test .; then
    echo "✅ Docker build successful"
else
    echo "❌ Docker build failed"
    exit 1
fi

# Test 5: Run Application
echo ""
echo "🚀 Testing application startup..."
if python -c "import uvicorn; uvicorn.run('backend.app:app', host='0.0.0.0', port=8000)" &
then
    APP_PID=$!
    sleep 5
    
    if curl -f http://localhost:8000/api/health; then
        echo "✅ Application started successfully"
    else
        echo "❌ Application health check failed"
    fi
    
    kill $APP_PID
else
    echo "❌ Application startup failed"
fi

echo ""
echo "🎉 All local tests completed!"
echo ""
echo "📋 Next steps:"
echo "1. Push to GitHub to test CI/CD pipeline"
echo "2. Check Actions tab in your repository"
echo "3. Verify both CI and Deploy workflows pass"
