#!/usr/bin/env python3
"""Validate configuration setup."""

from core.config import AppConfig
from core import constants


def main():
    """Validate configuration can be loaded and used."""
    print("=" * 70)
    print("Clinical Data Generator - Configuration Validation")
    print("=" * 70)

    # Load configuration
    config = AppConfig()

    print("\nApplication Settings:")
    print(f"  Environment: {config.environment}")
    print(f"  Debug mode: {config.debug}")
    print(f"  Log level: {config.log_level}")
    print(f"  Is development: {config.is_development}")
    print(f"  Is production: {config.is_production}")

    print("\nStorage Settings:")
    print(f"  Data directory: {config.storage.data_dir}")
    print(f"  S3 bucket: {config.storage.s3_bucket or 'Not configured'}")
    print(f"  S3 region: {config.storage.s3_region}")

    print("\nAWS Settings:")
    aws_configured = all([
        config.aws.access_key_id,
        config.aws.secret_access_key,
    ])
    print(f"  AWS configured: {'Yes' if aws_configured else 'No'}")
    if config.aws.access_key_id:
        print(f"  Access Key ID: {config.aws.access_key_id[:8]}...")

    print("\nAPI Settings:")
    print(f"  Host: {config.api.host}")
    print(f"  Port: {config.api.port}")
    print(f"  Version: {config.api.version}")
    print(f"  Base URL: {config.api.base_url}")
    print(f"  CORS origins: {config.api.cors_origins}")

    print("\nConstants:")
    print(f"  API title: {constants.API_TITLE}")
    print(f"  API version: {constants.API_VERSION}")
    print(f"  Supported formats: {', '.join(constants.SUPPORTED_FORMATS)}")
    print(f"  Default format: {constants.DEFAULT_FORMAT}")
    print(f"  Max members per request: {constants.MAX_MEMBERS_PER_REQUEST}")

    print("\n" + "=" * 70)
    print("Configuration validation successful!")
    print("=" * 70)

    # Test environment variable override
    print("\nTip: Override settings using environment variables:")
    print("  ENVIRONMENT=production python validate_config.py")
    print("  STORAGE__DATA_DIR=/custom/path python validate_config.py")
    print("  API_PORT=9000 python validate_config.py")


if __name__ == "__main__":
    main()
