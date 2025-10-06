#!/bin/bash
set -euo pipefail

# Deployment script for Movie Sentiment Analyzer
# Usage: ./scripts/deploy.sh [staging|production]

ENVIRONMENT=${1:-staging}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Deploying Movie Sentiment Analyzer to $ENVIRONMENT environment..."

# Check if environment is valid
if [[ "$ENVIRONMENT" != "staging" && "$ENVIRONMENT" != "production" ]]; then
    echo "❌ Error: Environment must be 'staging' or 'production'"
    exit 1
fi

# Check if required files exist
if [[ ! -f "$PROJECT_DIR/.env" ]]; then
    echo "❌ Error: .env file not found. Please create it from env.$ENVIRONMENT.example"
    exit 1
fi

# Load environment variables
source "$PROJECT_DIR/.env"

# Check if required environment variables are set
required_vars=("OMDB_API_KEY" "TMDB_API_KEY")
for var in "${required_vars[@]}"; do
    if [[ -z "${!var:-}" ]]; then
        echo "❌ Error: $var is not set in .env file"
        exit 1
    fi
done

echo "✅ Environment variables validated"

# Create necessary directories
mkdir -p "$PROJECT_DIR/data/movies"
mkdir -p "$PROJECT_DIR/data/reviews"
mkdir -p "$PROJECT_DIR/data/analysis"
mkdir -p "$PROJECT_DIR/data/samples"
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/ssl"

echo "✅ Directories created"

# Pull latest images
echo "📥 Pulling latest Docker images..."
docker-compose -f "$PROJECT_DIR/docker-compose.$ENVIRONMENT.yml" pull

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f "$PROJECT_DIR/docker-compose.$ENVIRONMENT.yml" down

# Start new containers
echo "🚀 Starting new containers..."
docker-compose -f "$PROJECT_DIR/docker-compose.$ENVIRONMENT.yml" up -d

# Wait for health check
echo "⏳ Waiting for application to be healthy..."
timeout=60
counter=0
while [[ $counter -lt $timeout ]]; do
    if curl -f http://localhost:8000/api/health >/dev/null 2>&1; then
        echo "✅ Application is healthy!"
        break
    fi
    echo "Waiting for application... ($counter/$timeout)"
    sleep 2
    counter=$((counter + 2))
done

if [[ $counter -ge $timeout ]]; then
    echo "❌ Error: Application failed to become healthy within $timeout seconds"
    docker-compose -f "$PROJECT_DIR/docker-compose.$ENVIRONMENT.yml" logs
    exit 1
fi

# Show deployment status
echo "📊 Deployment Status:"
docker-compose -f "$PROJECT_DIR/docker-compose.$ENVIRONMENT.yml" ps

echo "🎉 Deployment to $ENVIRONMENT completed successfully!"
echo "🌐 Application is available at: http://localhost:8000"
