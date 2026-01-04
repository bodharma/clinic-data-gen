"""Tests for configuration management."""

import os
from pathlib import Path

import pytest

from core.config import AppConfig, APIConfig, AWSConfig, StorageConfig
from core import constants


class TestStorageConfig:
    """Test StorageConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = StorageConfig()
        assert config.data_dir == Path("/tmp/data")
        assert config.s3_bucket is None
        assert config.s3_region == "us-east-1"

    def test_env_override(self, monkeypatch):
        """Test environment variable override."""
        monkeypatch.setenv("STORAGE_DATA_DIR", "/custom/path")
        monkeypatch.setenv("STORAGE_S3_BUCKET", "test-bucket")
        monkeypatch.setenv("STORAGE_S3_REGION", "eu-west-1")

        config = StorageConfig()
        assert config.data_dir == Path("/custom/path")
        assert config.s3_bucket == "test-bucket"
        assert config.s3_region == "eu-west-1"


class TestAWSConfig:
    """Test AWSConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = AWSConfig()
        assert config.access_key_id is None
        assert config.secret_access_key is None
        assert config.session_token is None

    def test_env_override(self, monkeypatch):
        """Test environment variable override."""
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test-key")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test-secret")
        monkeypatch.setenv("AWS_SESSION_TOKEN", "test-token")

        config = AWSConfig()
        assert config.access_key_id == "test-key"
        assert config.secret_access_key == "test-secret"
        assert config.session_token == "test-token"


class TestAPIConfig:
    """Test APIConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = APIConfig()
        assert config.host == "0.0.0.0"
        assert config.port == 8000
        assert config.version == "v3"
        assert config.base_url == "https://localhost:8000"
        assert config.cors_origins == ["*"]
        assert config.cors_allow_credentials is True

    def test_env_override(self, monkeypatch):
        """Test environment variable override."""
        monkeypatch.setenv("API_HOST", "127.0.0.1")
        monkeypatch.setenv("API_PORT", "9000")
        monkeypatch.setenv("API_VERSION", "v4")

        config = APIConfig()
        assert config.host == "127.0.0.1"
        assert config.port == 9000
        assert config.version == "v4"


class TestAppConfig:
    """Test AppConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = AppConfig()
        assert config.environment == "development"
        assert config.debug is False
        assert config.log_level == "INFO"
        assert isinstance(config.storage, StorageConfig)
        assert isinstance(config.aws, AWSConfig)
        assert isinstance(config.api, APIConfig)

    def test_is_development_property(self):
        """Test is_development property."""
        config = AppConfig(environment="development")
        assert config.is_development is True
        assert config.is_production is False

    def test_is_production_property(self):
        """Test is_production property."""
        config = AppConfig(environment="production")
        assert config.is_production is True
        assert config.is_development is False

    def test_nested_env_override(self, monkeypatch):
        """Test nested configuration override with double underscore."""
        monkeypatch.setenv("STORAGE__DATA_DIR", "/nested/path")
        monkeypatch.setenv("STORAGE__S3_BUCKET", "nested-bucket")
        monkeypatch.setenv("API__PORT", "7000")

        config = AppConfig()
        assert config.storage.data_dir == Path("/nested/path")
        assert config.storage.s3_bucket == "nested-bucket"
        assert config.api.port == 7000

    def test_environment_validation(self):
        """Test environment field validation."""
        # Valid environments
        for env in ["development", "staging", "production"]:
            config = AppConfig(environment=env)
            assert config.environment == env

        # Invalid environment should raise validation error
        with pytest.raises(Exception):  # Pydantic ValidationError
            AppConfig(environment="invalid")


class TestConstants:
    """Test application constants."""

    def test_api_constants(self):
        """Test API-related constants."""
        assert constants.API_TITLE == "Clinical Data Generator"
        assert constants.API_VERSION == "1.0.0"
        assert constants.API_V1_PREFIX == "/api/v1"

    def test_format_constants(self):
        """Test file format constants."""
        assert constants.SUPPORTED_FORMATS == ["csv", "json", "edi", "jsonlike"]
        assert constants.DEFAULT_FORMAT == "csv"

    def test_limit_constants(self):
        """Test limit constants."""
        assert constants.MAX_MEMBERS_PER_REQUEST == 10000
        assert constants.DEFAULT_MEMBERS_COUNT == 1

    def test_media_type_constants(self):
        """Test media type constants."""
        assert constants.MEDIA_TYPE_CSV == "text/csv"
        assert constants.MEDIA_TYPE_JSON == "application/json"
        assert constants.MEDIA_TYPE_EDI == "text/plain"
        assert constants.MEDIA_TYPE_JSONLIKE == "application/octet-stream"
