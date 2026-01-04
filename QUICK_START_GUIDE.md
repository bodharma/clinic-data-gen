# Clinical Data Generator - Quick Start Implementation Guide

This guide helps you begin modernizing the repository immediately with high-impact, manageable tasks.

---

## Phase 1: Immediate Fixes (Day 1 - 2-3 hours)

### Step 1: Fix Broken Tests (30 minutes)

**Fix import errors**:

```bash
# Current issue: tests can't import modules
# Solution: Add src/ directory to Python path

# Create pytest.ini or update pyproject.toml
```

**File: pyproject.toml**
```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

**Fix typo in test_app.py (line 44)**:
```python
# Before:
@LOaky(max_runs=max_runs)

# After:
@flaky(max_runs=max_runs)
```

**Run tests to verify**:
```bash
pytest tests/ -v
```

---

### Step 2: Update Dependencies (30 minutes)

**Create new requirements.txt**:
```txt
# Core Dependencies
fastapi>=0.115.0,<0.116.0
uvicorn[standard]>=0.34.0,<0.35.0
pydantic>=2.10.0,<3.0.0
httpx>=0.28.0,<0.29.0

# Data Generation
mimesis>=18.0.0,<19.0.0
Faker>=30.8.0,<31.0.0
numpy>=2.0.0,<3.0.0
pandas>=2.2.0,<3.0.0

# Protobuf (CRITICAL: Update from 3.15.3)
protobuf>=5.29.0,<6.0.0

# Storage & Database
boto3>=1.35.0
pymongo>=4.10.0
aiofiles>=24.1.0

# Utilities
loguru>=0.7.0
python-dotenv>=1.0.0
python-multipart>=0.0.20

# HTTP Requests
requests>=2.32.0
```

**Create requirements-dev.txt**:
```txt
# Testing
pytest>=8.3.0
pytest-asyncio>=0.24.0
pytest-cov>=6.0.0
pytest-xdist>=3.6.0
pytest-mock>=3.14.0
flaky>=3.8.0

# Code Quality
black>=24.10.0
ruff>=0.8.0
mypy>=1.13.0
bandit>=1.8.0
safety>=3.2.0
pre-commit>=4.0.0

# Type Stubs
types-requests>=2.32.0
```

**Install updated dependencies**:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

### Step 3: Create .env.example (15 minutes)

**File: .env.example**
```bash
# Application
APP_NAME="Clinical Data Generator"
APP_VERSION="2.0.0"
ENVIRONMENT="development"
DEBUG=true
LOG_LEVEL="DEBUG"

# API Configuration
API_HOST="0.0.0.0"
API_PORT=8000
API_PREFIX="/api/v1"
CORS_ORIGINS='["http://localhost:3000"]'

# Storage
STORAGE_TYPE="local"  # local | s3 | memory
LOCAL_STORAGE_PATH="/tmp/clinical-data-gen"
S3_BUCKET_NAME=""
S3_REGION="us-east-1"

# AWS Credentials (if using S3)
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""

# Database (Optional)
MONGODB_URL=""

# Security
SECRET_KEY="dev-secret-key-change-in-production"
ALLOWED_HOSTS='["*"]'

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Generation Limits
MAX_RECORDS_PER_REQUEST=10000
GENERATION_TIMEOUT_SECONDS=300
```

**Create actual .env file**:
```bash
cp .env.example .env
# Edit .env with your local values
```

**Update .gitignore to exclude .env**:
```bash
echo ".env" >> .gitignore
```

---

### Step 4: Update Pre-commit Configuration (15 minutes)

**File: .pre-commit-config.yaml**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic>=2.0]
        args: [--ignore-missing-imports]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks:
      - id: bandit
        args: [-ll, -r, .]
        exclude: tests/
```

**Install pre-commit hooks**:
```bash
pre-commit install
pre-commit run --all-files  # Test on all files
```

---

### Step 5: Create Makefile (30 minutes)

**File: Makefile**
```makefile
.PHONY: help install dev-install test lint format clean run docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make dev-install  - Install dev dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code"
	@echo "  make clean        - Remove generated files"
	@echo "  make run          - Run development server"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

dev-install: install
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-fast:
	pytest tests/ -v -x

lint:
	ruff check .
	mypy .
	bandit -r . -ll

format:
	ruff format .
	ruff check --fix .

clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

run:
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t clinical-data-generator:latest .

docker-run:
	docker run -p 8000:8000 --env-file .env clinical-data-generator:latest
```

**Test Makefile**:
```bash
make help
make dev-install
make test-fast
```

---

## Phase 2: Basic Structure (Day 2-3 - 4-6 hours)

### Step 1: Create src/ Package Structure (1 hour)

```bash
# Create directory structure
mkdir -p src/clinical_data_generator/{api,core,generators,formats,services,utils}
mkdir -p src/clinical_data_generator/api/routes
mkdir -p tests/{unit,integration,fixtures}

# Create __init__.py files
touch src/__init__.py
touch src/clinical_data_generator/__init__.py
touch src/clinical_data_generator/api/__init__.py
touch src/clinical_data_generator/api/routes/__init__.py
touch src/clinical_data_generator/core/__init__.py
touch src/clinical_data_generator/generators/__init__.py
touch src/clinical_data_generator/formats/__init__.py
touch src/clinical_data_generator/services/__init__.py
touch src/clinical_data_generator/utils/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

---

### Step 2: Create Configuration Module (1 hour)

**File: src/clinical_data_generator/config.py**
```python
"""Application configuration using pydantic-settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Application
    app_name: str = "Clinical Data Generator"
    app_version: str = "2.0.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Storage
    storage_type: Literal["local", "s3", "memory"] = "local"
    local_storage_path: str = "/tmp/clinical-data-gen"
    s3_bucket_name: Optional[str] = None
    s3_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    # Database
    mongodb_url: Optional[str] = None

    # Security
    secret_key: str = "dev-secret-key"
    allowed_hosts: list[str] = ["*"]

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    # Generation
    max_records_per_request: int = 10000
    generation_timeout_seconds: int = 300

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

---

### Step 3: Create Health Check Endpoint (30 minutes)

**File: src/clinical_data_generator/api/routes/health.py**
```python
"""Health check endpoints."""
from fastapi import APIRouter, status
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Basic health check endpoint for monitoring"
)
async def health_check() -> HealthResponse:
    """Check if API is alive."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="2.0.0"
    )


@router.get(
    "/health/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness check",
    description="Check if API is ready to handle requests"
)
async def readiness_check():
    """Kubernetes readiness probe."""
    return {"status": "ready"}


@router.get(
    "/health/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness check",
    description="Check if API is alive"
)
async def liveness_check():
    """Kubernetes liveness probe."""
    return {"status": "alive"}
```

---

### Step 4: Update Main Application (1 hour)

**File: src/clinical_data_generator/main.py**
```python
"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import get_settings
from .api.routes import health

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise-grade synthetic healthcare data generation",
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    health.router,
    prefix=settings.api_prefix
)

# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint redirect to docs."""
    return JSONResponse({
        "message": "Clinical Data Generator API",
        "version": settings.app_version,
        "docs": f"{settings.api_prefix}/docs"
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
```

**Test the new application**:
```bash
# Run from root directory
python -m src.clinical_data_generator.main

# Or add to Makefile:
run-new:
	python -m src.clinical_data_generator.main

# Test endpoints:
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/docs
```

---

### Step 5: Create Basic Test for New Structure (30 minutes)

**File: tests/integration/test_health.py**
```python
"""Integration tests for health endpoints."""
import pytest
from httpx import AsyncClient
from src.clinical_data_generator.main import app


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Test health check endpoints."""

    @pytest.fixture
    async def client(self):
        """HTTP client fixture."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac

    async def test_health_check(self, client):
        """Test basic health check."""
        response = await client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data

    async def test_readiness_check(self, client):
        """Test readiness probe."""
        response = await client.get("/api/v1/health/ready")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    async def test_liveness_check(self, client):
        """Test liveness probe."""
        response = await client.get("/api/v1/health/live")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
```

**Run tests**:
```bash
pytest tests/integration/test_health.py -v
```

---

## Phase 3: Improve Dockerfile (Day 3 - 1 hour)

### Multi-stage Dockerfile

**File: Dockerfile**
```dockerfile
# Stage 1: Base
FROM python:3.12-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies
FROM base as dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Application
FROM base as application

# Copy installed dependencies from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ /app/src/
COPY templates/ /app/templates/
COPY data/ /app/data/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/health')"

# Run application
CMD ["uvicorn", "src.clinical_data_generator.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Test Docker build**:
```bash
make docker-build
make docker-run

# Verify health:
curl http://localhost:8000/api/v1/health
```

---

## Phase 4: Create GitHub Actions CI (Day 4 - 1 hour)

**File: .github/workflows/ci.yml**
```yaml
name: CI

on:
  push:
    branches: [ master, main, develop ]
  pull_request:
    branches: [ master, main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Lint with ruff
      run: |
        ruff check .

    - name: Type check with mypy
      run: |
        mypy src/ --ignore-missing-imports

    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=src --cov-report=xml --cov-report=term

    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false

  security:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Run Bandit security scan
      run: |
        pip install bandit
        bandit -r src/ -f json -o bandit-report.json

    - name: Run Safety check
      run: |
        pip install safety
        safety check --json || true

  docker:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Build Docker image
      run: |
        docker build -t clinical-data-generator:test .

    - name: Test Docker image
      run: |
        docker run -d -p 8000:8000 --name test-container clinical-data-generator:test
        sleep 10
        curl -f http://localhost:8000/api/v1/health || exit 1
        docker stop test-container
```

---

## Verification Checklist

After completing these steps, verify:

- [ ] Tests run successfully: `make test`
- [ ] Linting passes: `make lint`
- [ ] Code formatted: `make format`
- [ ] Application runs: `make run`
- [ ] Docker builds: `make docker-build`
- [ ] Docker runs: `make docker-run`
- [ ] Health endpoint works: `curl http://localhost:8000/api/v1/health`
- [ ] API docs accessible: http://localhost:8000/api/v1/docs
- [ ] Pre-commit hooks work: `git commit` (test with small change)
- [ ] CI pipeline runs (after pushing to GitHub)

---

## Next Steps

Once you've completed this quick start:

1. **Migrate Existing Code**: Start moving code from root into src/ structure
2. **Add Type Hints**: Begin adding type annotations to existing functions
3. **Write Tests**: Add unit tests for generators
4. **Refactor Generators**: Extract base class and implement strategy pattern
5. **Update Documentation**: Write comprehensive README

Refer to TECHNICAL_MODERNIZATION_PLAN.md for the complete roadmap.

---

## Common Issues & Solutions

### Issue: ModuleNotFoundError when importing from src/
**Solution**: Ensure pythonpath is set in pyproject.toml or install package in development mode:
```bash
pip install -e .
```

### Issue: Tests still failing after fixes
**Solution**: Clear pytest cache:
```bash
make clean
pytest --cache-clear
```

### Issue: Docker build fails
**Solution**: Check Docker is running and you're in project root:
```bash
docker info
pwd  # Should show .../clinical-data-generator
```

### Issue: Pre-commit hooks too slow
**Solution**: Run on changed files only:
```bash
git add .
pre-commit run
```

---

## Time Estimates Summary

- **Phase 1** (Immediate Fixes): 2-3 hours
- **Phase 2** (Basic Structure): 4-6 hours
- **Phase 3** (Dockerfile): 1 hour
- **Phase 4** (CI Pipeline): 1 hour

**Total**: 8-11 hours for foundational improvements

These changes will make your repository significantly more professional and set the foundation for deeper refactoring.
