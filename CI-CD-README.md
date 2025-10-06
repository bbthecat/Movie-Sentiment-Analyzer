# CI/CD Setup for Movie Sentiment Analyzer

This document describes the Continuous Integration and Continuous Deployment (CI/CD) setup for the Movie Sentiment Analyzer project.

## 🚀 Overview

The CI/CD pipeline includes:
- **Continuous Integration (CI)**: Automated testing, linting, and security scanning
- **Continuous Deployment (CD)**: Automated deployment to staging and production environments
- **Security Scanning**: Dependency and code vulnerability scanning
- **Multi-environment Support**: Staging and production configurations

## 📁 File Structure

```
.github/
├── workflows/
│   ├── ci.yml              # Continuous Integration workflow
│   ├── cd.yml              # Continuous Deployment workflow
│   └── security.yml        # Security scanning workflow
├── docker-compose.staging.yml    # Staging environment
├── docker-compose.production.yml # Production environment
├── nginx/
│   ├── staging.conf        # Nginx config for staging
│   └── production.conf     # Nginx config for production
├── scripts/
│   ├── deploy.sh          # Linux/Mac deployment script
│   ├── deploy.ps1         # Windows deployment script
│   └── ci_simulate.sh     # Local CI simulation
├── env.staging.example     # Staging environment template
└── env.production.example  # Production environment template
```

## 🔧 Workflows

### 1. Continuous Integration (CI)

**Trigger**: Push to `main`/`develop` branches, Pull Requests

**Features**:
- Multi-Python version testing (3.11, 3.12)
- Code linting with flake8
- Unit testing with pytest and coverage
- Security scanning with safety and bandit
- Docker image building and caching

### 2. Continuous Deployment (CD)

**Trigger**: 
- Push to `main` branch → Deploy to staging
- Git tags (`v*`) → Deploy to production
- Manual workflow dispatch

**Features**:
- Multi-environment deployment
- Docker image building and pushing to GitHub Container Registry
- Automated releases for production deployments
- Environment-specific configurations

### 3. Security Scanning

**Trigger**: Push to `main`/`develop`, Pull Requests, Weekly schedule

**Features**:
- Dependency vulnerability scanning (safety, pip-audit)
- Code security analysis (bandit, semgrep)
- Docker image vulnerability scanning (Trivy)
- SARIF report upload to GitHub Security tab

## 🛠️ Setup Instructions

### 1. GitHub Repository Setup

1. **Enable GitHub Actions**: Go to your repository → Settings → Actions → General
2. **Set up Environments**: 
   - Go to Settings → Environments
   - Create `staging` and `production` environments
   - Add required secrets for each environment

### 2. Required Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

#### Repository Secrets (for all environments):
- `OMDB_API_KEY`: Your OMDb API key
- `TMDB_API_KEY`: Your TMDb API key
- `TRAKT_CLIENT_ID`: Your Trakt client ID (optional)

#### Environment-specific Secrets:
- `DOCKER_REGISTRY_TOKEN`: GitHub token for container registry access
- `DEPLOYMENT_HOST`: Target server for deployment
- `SSH_PRIVATE_KEY`: SSH key for server access
- `SSL_CERT`: SSL certificate for production
- `SSL_KEY`: SSL private key for production

### 3. Local Development Setup

1. **Copy environment file**:
   ```bash
   cp env.staging.example .env
   ```

2. **Edit `.env`** with your API keys:
   ```bash
   OMDB_API_KEY=your_actual_api_key
   TMDB_API_KEY=your_actual_api_key
   ```

3. **Run local CI simulation**:
   ```bash
   ./scripts/ci_simulate.sh
   ```

### 4. Deployment

#### Using GitHub Actions (Recommended)
- Push to `main` branch for staging deployment
- Create a git tag for production deployment:
  ```bash
  git tag v1.0.0
  git push origin v1.0.0
  ```

#### Manual Deployment

**Linux/Mac**:
```bash
./scripts/deploy.sh staging
./scripts/deploy.sh production
```

**Windows**:
```powershell
.\scripts\deploy.ps1 staging
.\scripts\deploy.ps1 production
```

## 🔍 Monitoring and Debugging

### 1. GitHub Actions Logs
- Go to your repository → Actions tab
- Click on any workflow run to view detailed logs

### 2. Application Health Check
```bash
curl http://localhost:8000/api/health
```

### 3. Container Logs
```bash
docker-compose -f docker-compose.staging.yml logs -f
docker-compose -f docker-compose.production.yml logs -f
```

### 4. Security Reports
- Go to your repository → Security tab
- View vulnerability alerts and code scanning results

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check Python version compatibility
   - Verify all dependencies are in `requirements.txt`
   - Review flake8 linting errors

2. **Deployment Failures**:
   - Verify environment variables are set correctly
   - Check Docker daemon is running
   - Ensure ports 8000, 80, 443 are available

3. **Security Scan Failures**:
   - Review vulnerability reports
   - Update dependencies with known vulnerabilities
   - Fix code security issues flagged by bandit

### Getting Help

1. Check GitHub Actions logs for detailed error messages
2. Review container logs for runtime issues
3. Verify environment configuration files
4. Test locally using the CI simulation script

## 📊 Metrics and Reporting

The CI/CD pipeline provides:
- **Test Coverage**: Code coverage reports via pytest-cov
- **Security Metrics**: Vulnerability counts and severity levels
- **Build Performance**: Build times and success rates
- **Deployment Status**: Environment health and availability

## 🔄 Maintenance

### Regular Tasks
1. **Weekly**: Review security scan results
2. **Monthly**: Update dependencies and base images
3. **Quarterly**: Review and update CI/CD configurations

### Updates
- Keep GitHub Actions workflows updated
- Monitor for new security tools and best practices
- Update Docker base images regularly
- Review and optimize build performance

## 📝 Best Practices

1. **Branch Protection**: Enable branch protection rules for `main`
2. **Code Reviews**: Require pull request reviews
3. **Environment Parity**: Keep staging and production configs similar
4. **Secrets Management**: Never commit secrets to version control
5. **Monitoring**: Set up alerts for deployment failures
6. **Backup**: Regular backup of production data and configurations
