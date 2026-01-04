# Core Configuration Module

Type-safe, validated configuration management using Pydantic Settings v2.

## Quick Start

```python
from core.config import AppConfig
from core import constants

# Load configuration (reads from .env file and environment variables)
config = AppConfig()

# Access settings
print(config.storage.data_dir)  # Path('/tmp/data')
print(config.api.port)           # 8000
print(config.environment)        # 'development'

# Use constants
print(constants.SUPPORTED_FORMATS)  # ['csv', 'json', 'edi', 'jsonlike']
```

## Configuration Structure

### AppConfig
Main application configuration with nested settings.

**Fields:**
- `environment`: Application environment (development/staging/production)
- `debug`: Enable debug mode
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `storage`: StorageConfig instance
- `aws`: AWSConfig instance
- `api`: APIConfig instance

**Helper properties:**
- `is_development`: Returns True if environment is 'development'
- `is_production`: Returns True if environment is 'production'

### StorageConfig
File storage configuration.

**Fields:**
- `data_dir`: Base directory for generated files (default: `/tmp/data`)
- `s3_bucket`: S3 bucket name for uploads (optional)
- `s3_region`: AWS S3 region (default: `us-east-1`)

**Environment prefix:** `STORAGE_`

### AWSConfig
AWS credentials configuration.

**Fields:**
- `access_key_id`: AWS access key ID (optional)
- `secret_access_key`: AWS secret access key (optional)
- `session_token`: AWS session token for temporary credentials (optional)

**Environment prefix:** `AWS_`

### APIConfig
API server configuration.

**Fields:**
- `host`: Host address to bind (default: `0.0.0.0`)
- `port`: Port to bind (default: `8000`)
- `version`: API version (default: `v3`)
- `base_url`: Base URL for API calls (default: `https://localhost:8000`)
- `cors_origins`: Allowed CORS origins (default: `["*"]`)
- `cors_allow_credentials`: Allow credentials in CORS (default: `True`)
- `cors_allow_methods`: Allowed HTTP methods (default: `["*"]`)
- `cors_allow_headers`: Allowed headers (default: `["*"]`)

**Environment prefix:** `API_`

## Environment Variables

### Simple Variables
```bash
ENVIRONMENT=production
DEBUG=true
LOG_LEVEL=WARNING
```

### Nested Variables (using double underscore)
```bash
STORAGE__DATA_DIR=/custom/path
STORAGE__S3_BUCKET=my-bucket
STORAGE__S3_REGION=eu-west-1

API_HOST=0.0.0.0
API_PORT=9000
API_VERSION=v3
```

### Using .env File
1. Copy `.env.example` to `.env`
2. Update values as needed
3. Configuration will automatically load from `.env`

```bash
cp .env.example .env
# Edit .env with your values
```

## Constants

Application-wide constants are defined in `constants.py`:

**API Metadata:**
- `API_TITLE`: "Clinical Data Generator"
- `API_VERSION`: "1.0.0"
- `API_V1_PREFIX`: "/api/v1"

**File Formats:**
- `SUPPORTED_FORMATS`: ["csv", "json", "edi", "jsonlike"]
- `DEFAULT_FORMAT`: "csv"

**Limits:**
- `MAX_MEMBERS_PER_REQUEST`: 10000
- `DEFAULT_MEMBERS_COUNT`: 1

**See `constants.py` for complete list.**

## Validation

Run the validation script to verify configuration:

```bash
python validate_config.py

# With environment overrides
ENVIRONMENT=production python validate_config.py
STORAGE__DATA_DIR=/custom/path python validate_config.py
```

## Type Safety

All configuration values have full type hints and runtime validation:

```python
config = AppConfig()

# Type-safe access with IDE autocomplete
config.storage.data_dir  # Path
config.api.port          # int
config.environment       # Literal["development", "staging", "production"]
config.storage.s3_bucket # str | None

# Runtime validation
config = AppConfig(api={"port": "invalid"})  # Raises ValidationError
```

## Production Example

```bash
# .env file for production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

STORAGE_DATA_DIR=/var/lib/clinical-data-generator
STORAGE__S3_BUCKET=prod-clinical-data-bucket
STORAGE__S3_REGION=us-west-2

AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

API_HOST=0.0.0.0
API_PORT=8000
API_BASE_URL=https://api.example.com
```

## Next Steps

This configuration will be integrated into:
1. FastAPI app initialization (CORS, metadata)
2. Storage path management
3. S3 upload functionality
4. Logging configuration
5. API connectors

See Phase 1 plan for integration roadmap.
