# Movie Sentiment Analyzer - Development Makefile

.PHONY: help install test lint security build deploy-staging deploy-production clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install         - Install dependencies"
	@echo "  test           - Run tests"
	@echo "  lint           - Run linting"
	@echo "  security       - Run security checks"
	@echo "  ci             - Run full CI pipeline locally"
	@echo "  build          - Build Docker image"
	@echo "  deploy-staging - Deploy to staging"
	@echo "  deploy-prod    - Deploy to production"
	@echo "  clean          - Clean up containers and images"

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	pytest -v --cov=backend --cov-report=html --cov-report=term

# Run linting
lint:
	flake8 backend tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 backend tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run security checks
security:
	safety check
	bandit -r backend/
	pip-audit

# Run full CI pipeline locally
ci:
	@echo "Running CI pipeline..."
	@$(MAKE) install
	@$(MAKE) lint
	@$(MAKE) test
	@$(MAKE) security
	@echo "CI pipeline completed successfully!"

# Build Docker image
build:
	docker build -t movie-sentiment-analyzer:latest .

# Deploy to staging
deploy-staging:
	@if [ -f .env ]; then \
		docker-compose -f docker-compose.staging.yml up -d; \
	else \
		echo "Error: .env file not found. Please create it from env.staging.example"; \
		exit 1; \
	fi

# Deploy to production
deploy-prod:
	@if [ -f .env ]; then \
		docker-compose -f docker-compose.production.yml up -d; \
	else \
		echo "Error: .env file not found. Please create it from env.production.example"; \
		exit 1; \
	fi

# Clean up
clean:
	docker-compose -f docker-compose.staging.yml down
	docker-compose -f docker-compose.production.yml down
	docker system prune -f
	docker image prune -f

# Development helpers
dev:
	uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

logs-staging:
	docker-compose -f docker-compose.staging.yml logs -f

logs-prod:
	docker-compose -f docker-compose.production.yml logs -f

# Health check
health:
	curl -f http://localhost:8000/api/health || echo "Application is not running"
