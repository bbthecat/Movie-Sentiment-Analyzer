# Troubleshooting Guide

## GitHub Actions Errors

### 1. CI Workflow Errors

**Problem**: `flake8: command not found`
**Solution**: 
- ✅ Fixed: Added `pip install flake8 pytest` to CI workflow
- ✅ Fixed: Updated requirements.txt to be more flexible

**Problem**: `pytest: command not found`
**Solution**:
- ✅ Fixed: Added pytest installation to CI workflow

**Problem**: `ModuleNotFoundError: No module named 'httpx'`
**Solution**:
- ✅ Fixed: Added httpx to requirements.txt and CI workflow
- ✅ Fixed: Added PYTHONPATH=. to pytest command

**Problem**: `ModuleNotFoundError: No module named 'backend'`
**Solution**:
- ✅ Fixed: Added PYTHONPATH=. to pytest command in CI workflow

### 2. Deploy Workflow Errors

**Problem**: Permission denied when pushing to GitHub Container Registry
**Solution**:
- ✅ Fixed: Added proper permissions to deploy workflow:
  ```yaml
  permissions:
    contents: read
    packages: write
  ```

**Problem**: Docker build fails
**Solution**:
- ✅ Fixed: Updated Dockerfile with proper system dependencies
- ✅ Fixed: Created .dockerignore to reduce build context
- ✅ Fixed: Updated requirements.txt with flexible versions

### 3. Local Development Issues

**Problem**: Import errors in Windows
**Solution**:
```bash
# Install dependencies
py -m pip install -r requirements.txt

# Run tests
py -m pytest tests/ -v

# Run linting
py -m flake8 backend tests
```

**Problem**: Docker build fails locally
**Solution**:
```bash
# Build with verbose output
docker build -t movie-sentiment-analyzer:test . --progress=plain

# Check if Docker is running
docker --version
```

### 4. Common Fixes Applied

1. **Requirements.txt**: Made version constraints more flexible
2. **Dockerfile**: Added build-essential and curl
3. **CI Workflow**: Added missing dependencies installation
4. **Deploy Workflow**: Added proper permissions
5. **Dockerignore**: Reduced build context size

### 5. Testing the Fixes

**Local Testing**:
```bash
# Test Python dependencies
py -m pip install -r requirements.txt
py -m pytest tests/ -v

# Test Docker build
docker build -t movie-sentiment-analyzer:test .
```

**GitHub Actions Testing**:
1. Push changes to main branch
2. Check Actions tab in GitHub repository
3. Verify both CI and Deploy workflows pass

### 6. If Issues Persist

1. **Check GitHub Actions logs** for specific error messages
2. **Verify repository secrets** are set correctly
3. **Check branch protection rules** if using protected branches
4. **Ensure Docker is enabled** in repository settings

### 7. Success Indicators

✅ **CI Workflow**: Tests pass, linting passes, Docker builds
✅ **Deploy Workflow**: Image pushed to GitHub Container Registry
✅ **Local Development**: All commands work without errors
