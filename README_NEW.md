# Clinical Data Generator

> Enterprise-grade synthetic healthcare data generation for testing, development, and compliance

[![CI Status](https://github.com/yourusername/clinical-data-generator/workflows/CI/badge.svg)](https://github.com/yourusername/clinical-data-generator/actions)
[![Coverage](https://codecov.io/gh/yourusername/clinical-data-generator/branch/master/graph/badge.svg)](https://codecov.io/gh/yourusername/clinical-data-generator)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Overview

Clinical Data Generator is a high-performance Python application that generates synthetic, HIPAA-compliant healthcare data for testing healthcare systems, insurance claims processing, and clinical workflows. It supports multiple industry-standard formats including EDI X12, FHIR, and custom healthcare schemas.

### Key Features

- **Multiple Data Formats**: Generate EDI X12 837/834, FHIR R4 resources, CSV, JSON, and Protocol Buffers
- **Healthcare Standards**: Compliant with HIPAA, HL7 FHIR v4, and EDI X12 standards
- **RESTful API**: FastAPI-based API with automatic OpenAPI documentation
- **High Performance**: Async I/O and multiprocessing for generating large datasets
- **Flexible Output**: Local file system, AWS S3, or in-memory storage
- **Production Ready**: Type-safe, fully tested, containerized, and monitored

### Use Cases

- Testing healthcare payment systems and adjudication engines
- Developing insurance claim processing workflows
- Creating realistic patient demographics for EHR testing
- Generating vaccine registry data for public health systems
- Validating FHIR API implementations
- Training machine learning models with synthetic health data

---

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- AWS account (optional, for S3 storage)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/clinical-data-generator.git
cd clinical-data-generator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
# Edit .env with your configuration

# Run the application
uvicorn src.clinical_data_generator.main:app --reload
```

Access the API documentation at: http://localhost:8000/api/v1/docs

### Docker Quick Start

```bash
# Build image
docker build -t clinical-data-generator .

# Run container
docker run -p 8000:8000 --env-file .env clinical-data-generator

# Or use Docker Compose
docker-compose up
```

---

## Usage Examples

### Generate Member Demographics CSV

**HTTP Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/members/csv?members_num=100" \
  -H "accept: text/csv" \
  --output members.csv
```

**Python Client**:
```python
import httpx

response = httpx.get(
    "http://localhost:8000/api/v1/members/csv",
    params={"members_num": 100}
)

with open("members.csv", "wb") as f:
    f.write(response.content)
```

### Generate EDI X12 837 Claims

**HTTP Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/edi/claims" \
  -H "Content-Type: application/json" \
  -d '{
    "claim_count": 5,
    "segments": 2,
    "optional_fields": true,
    "claim_data": {
      "diagnosis_code": "Z01.411",
      "service_code": "99213"
    }
  }' \
  --output claims.edi
```

### Generate FHIR Diagnostic Reports

**HTTP Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/fhir/diagnostic-reports" \
  -H "Content-Type: application/json" \
  -d '{
    "record_count": 10,
    "output_format": "json"
  }'
```

### Generate Vaccine Encounters

**HTTP Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/vaccines" \
  -H "Content-Type: application/json" \
  -d '{
    "entries": 50,
    "vaccine_type": "Pfizer",
    "dose_number": 1
  }'
```

---

## API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check endpoint |
| `/api/v1/members/csv` | GET | Generate member demographics CSV |
| `/api/v1/members/edi` | GET | Generate EDI 834 enrollment |
| `/api/v1/edi/claims` | POST | Generate EDI 837 claims |
| `/api/v1/fhir/diagnostic-reports` | POST | Generate FHIR diagnostic reports |
| `/api/v1/vaccines` | POST | Generate vaccine encounter data |
| `/api/v1/eligibility` | POST | Generate eligibility data |

### Request Parameters

**Common Parameters**:
- `record_count`: Number of records to generate (1-10000)
- `output_format`: Output format (csv, json, edi, fhir)
- `include_metadata`: Include generation metadata (boolean)

**Example Request Body**:
```json
{
  "record_count": 100,
  "output_format": "csv",
  "include_metadata": true,
  "member_filters": {
    "age_range": [18, 65],
    "ethnicity_filter": ["Asian", "White"],
    "include_address": true
  }
}
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "download_url": "/downloads/members-20250104.csv",
    "record_count": 100,
    "format": "csv",
    "file_size_bytes": 15360,
    "generated_at": "2025-01-04T12:00:00Z"
  },
  "meta": {
    "version": "2.0.0",
    "request_id": "req-abc123"
  }
}
```

---

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│  Client/User    │
└────────┬────────┘
         │ HTTP/REST
┌────────┴────────────────────────────┐
│       FastAPI Gateway               │
│  ┌──────────────────────────────┐  │
│  │ Routes │ Validation │ Auth   │  │
│  └──────────────────────────────┘  │
└────────┬────────────────────────────┘
         │
┌────────┴────────────────────────────┐
│      Service Layer                  │
│  ┌────────────┐  ┌──────────────┐  │
│  │ Generation │  │  Validation  │  │
│  │  Service   │  │   Service    │  │
│  └────────────┘  └──────────────┘  │
└────────┬────────────────────────────┘
         │
┌────────┴────────────────────────────┐
│    Business Logic Layer             │
│  ┌──────────┐  ┌──────────┐        │
│  │ Member   │  │  Claim   │  ...   │
│  │Generator │  │Generator │        │
│  └──────────┘  └──────────┘        │
└────────┬────────────────────────────┘
         │
┌────────┴────────────────────────────┐
│    Format Conversion Layer          │
│  ┌─────┐  ┌─────┐  ┌──────┐        │
│  │ EDI │  │ CSV │  │ FHIR │  ...   │
│  └─────┘  └─────┘  └──────┘        │
└─────────────────────────────────────┘
```

### Technology Stack

- **Framework**: FastAPI 0.115+ (async Python web framework)
- **Validation**: Pydantic v2 (data validation using Python type hints)
- **Data Generation**: Mimesis 18+, Faker 30+ (synthetic data libraries)
- **Storage**: Local filesystem, AWS S3, in-memory
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Code Quality**: Ruff (linting), Black (formatting), Mypy (type checking)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus metrics, structured logging

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Development

### Development Setup

```bash
# Install development dependencies
make dev-install

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run application in development mode
make run
```

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_generators.py -v

# Run integration tests only
pytest tests/integration/ -v

# Run with parallel execution
pytest tests/ -n auto
```

### Code Quality

This project enforces high code quality standards:

```bash
# Type checking
mypy src/

# Linting
ruff check .

# Security scanning
bandit -r src/

# Dependency vulnerability check
safety check
```

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit:

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Configuration

### Environment Variables

Configuration is managed through environment variables. See [`.env.example`](.env.example) for all available options.

**Key Configuration**:

```bash
# Application
ENVIRONMENT=development  # development | staging | production
DEBUG=true
LOG_LEVEL=DEBUG

# API
API_PORT=8000
CORS_ORIGINS='["http://localhost:3000"]'

# Storage
STORAGE_TYPE=local  # local | s3 | memory
S3_BUCKET_NAME=my-bucket
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret

# Generation Limits
MAX_RECORDS_PER_REQUEST=10000
GENERATION_TIMEOUT_SECONDS=300
```

### Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Default**: 100 requests per minute per IP
- **Configuration**: Set via `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW`
- **Custom limits**: Can be set per endpoint

---

## Deployment

### Docker Deployment

**Build and run**:
```bash
docker build -t clinical-data-generator:latest .
docker run -d -p 8000:8000 --env-file .env clinical-data-generator:latest
```

**Docker Compose**:
```bash
docker-compose up -d
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f deployment/kubernetes/

# Check deployment status
kubectl get pods -l app=clinical-data-generator

# View logs
kubectl logs -l app=clinical-data-generator
```

### AWS ECS/Fargate

See [deployment/aws/README.md](deployment/aws/README.md) for AWS deployment instructions.

### Health Checks

The application provides health check endpoints for monitoring:

- `/health`: Basic health check
- `/health/ready`: Readiness probe (all dependencies available)
- `/health/live`: Liveness probe (application is running)

---

## Data Formats

### Supported Formats

#### 1. EDI X12

**Supported Transaction Sets**:
- **834**: Benefit Enrollment and Maintenance
- **837**: Health Care Claim (Professional, Institutional, Dental)
- **270/271**: Eligibility Inquiry and Response
- **835**: Health Care Claim Payment/Advice

**Example Usage**:
```python
from src.clinical_data_generator.generators import ClaimGenerator
from src.clinical_data_generator.formats import EDIAdapter

generator = ClaimGenerator()
claims = generator.generate(count=10)

edi_adapter = EDIAdapter()
edi_document = edi_adapter.convert(claims)
```

#### 2. FHIR R4

**Supported Resources**:
- Patient
- Observation
- DiagnosticReport
- Immunization
- Condition
- MedicationRequest

**Example**:
```json
{
  "resourceType": "DiagnosticReport",
  "id": "example-123",
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "58410-2",
      "display": "Complete blood count"
    }]
  },
  "subject": {
    "reference": "Patient/example-456"
  }
}
```

#### 3. CSV

Standard CSV format with headers, suitable for data analysis and import into databases.

#### 4. JSON

Structured JSON format compatible with most modern APIs and databases.

#### 5. Protocol Buffers

Binary format for high-performance data serialization.

---

## Performance

### Benchmarks

Generation performance on standard hardware (Apple M1, 16GB RAM):

| Record Count | Format | Time | Throughput |
|-------------|--------|------|------------|
| 1,000 | CSV | 0.5s | 2,000/s |
| 1,000 | JSON | 0.6s | 1,667/s |
| 1,000 | EDI | 1.2s | 833/s |
| 10,000 | CSV | 4.5s | 2,222/s |
| 10,000 | JSON | 5.2s | 1,923/s |

### Optimization Tips

1. **Use async endpoints** for I/O-bound operations
2. **Enable multiprocessing** for CPU-intensive generation (>1000 records)
3. **Use S3 storage** for large datasets to avoid local disk I/O
4. **Batch requests** when generating multiple datasets
5. **Cache configuration** objects to avoid repeated instantiation

---

## Security

### Security Measures

- **Input Validation**: All inputs validated using Pydantic schemas
- **Rate Limiting**: Prevents API abuse
- **CORS**: Configurable CORS policies
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, etc.
- **Dependency Scanning**: Automated vulnerability checks via GitHub Actions
- **Container Security**: Non-root user, minimal base image

### HIPAA Compliance

All generated data is **synthetic and not real patient data**. The application:

- Does NOT store or process real PHI
- Generates data using randomization algorithms
- Should NOT be used with real patient identifiers
- Is suitable for testing and development environments only

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `make test`
5. Run linting: `make lint`
6. Commit changes: `git commit -m "Add my feature"`
7. Push to branch: `git push origin feature/my-feature`
8. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Add type hints to all functions
- Write docstrings for all public APIs
- Maintain test coverage above 85%
- Update documentation for new features

---

## Roadmap

### Version 2.1 (Q2 2025)
- [ ] GraphQL API support
- [ ] Real-time data streaming
- [ ] Enhanced FHIR resource support
- [ ] Data validation against official schemas

### Version 2.5 (Q3 2025)
- [ ] Web UI for data generation
- [ ] Scheduled generation jobs
- [ ] Data quality metrics dashboard
- [ ] Export to additional formats (Parquet, Avro)

### Version 3.0 (Q4 2025)
- [ ] Machine learning-based data generation
- [ ] Multi-tenant support
- [ ] Advanced data relationship modeling
- [ ] Integration with healthcare data standards APIs

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
```bash
# Solution: Install package in development mode
pip install -e .
```

**Issue**: Tests failing with import errors
```bash
# Solution: Ensure pytest can find modules
export PYTHONPATH="${PYTHONPATH}:${PWD}"
pytest tests/
```

**Issue**: Docker container unhealthy
```bash
# Solution: Check logs
docker logs <container-id>

# Verify health endpoint
docker exec <container-id> curl http://localhost:8000/api/v1/health
```

**Issue**: Rate limit errors in development
```bash
# Solution: Disable rate limiting
# In .env file:
RATE_LIMIT_ENABLED=false
```

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Mimesis** and **Faker** libraries for synthetic data generation
- **FastAPI** framework for the excellent async API capabilities
- Healthcare standards organizations (HL7, X12, NCPDP) for format specifications
- Open source contributors and testers

---

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/clinical-data-generator/issues)
- **Documentation**: [Full Documentation](https://clinical-data-generator.readthedocs.io)
- **Email**: your.email@example.com
- **Twitter**: [@yourhandle](https://twitter.com/yourhandle)

---

## Citation

If you use this project in your research or development, please cite:

```bibtex
@software{clinical_data_generator,
  title = {Clinical Data Generator: Enterprise Healthcare Data Synthesis},
  author = {Your Name},
  year = {2025},
  url = {https://github.com/yourusername/clinical-data-generator}
}
```

---

**Built with ❤️ for the healthcare technology community**
