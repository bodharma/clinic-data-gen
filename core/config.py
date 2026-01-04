"""Configuration management using Pydantic Settings v2."""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageConfig(BaseSettings):
    """File storage configuration."""

    model_config = SettingsConfigDict(env_prefix="STORAGE_")

    data_dir: Path = Field(
        default=Path("/tmp/data"),
        description="Base directory for generated data files",
    )
    s3_bucket: str | None = Field(
        default=None,
        description="S3 bucket name for uploads (optional)",
    )
    s3_region: str = Field(
        default="us-east-1",
        description="AWS S3 region",
    )


class AWSConfig(BaseSettings):
    """AWS credentials configuration."""

    model_config = SettingsConfigDict(env_prefix="AWS_")

    access_key_id: str | None = Field(
        default=None,
        description="AWS access key ID",
    )
    secret_access_key: str | None = Field(
        default=None,
        description="AWS secret access key",
    )
    session_token: str | None = Field(
        default=None,
        description="AWS session token (for temporary credentials)",
    )


class APIConfig(BaseSettings):
    """API server configuration."""

    model_config = SettingsConfigDict(env_prefix="API_")

    host: str = Field(
        default="0.0.0.0",
        description="Host address to bind the API server",
    )
    port: int = Field(
        default=8000,
        description="Port to bind the API server",
    )
    version: str = Field(
        default="v3",
        description="API version",
    )
    base_url: str = Field(
        default="https://localhost:8000",
        description="Base URL for API calls (used in connectors)",
    )
    cors_origins: list[str] = Field(
        default=["*"],
        description="Allowed CORS origins",
    )
    cors_allow_credentials: bool = Field(
        default=True,
        description="Allow credentials in CORS requests",
    )
    cors_allow_methods: list[str] = Field(
        default=["*"],
        description="Allowed HTTP methods for CORS",
    )
    cors_allow_headers: list[str] = Field(
        default=["*"],
        description="Allowed headers for CORS",
    )


class AppConfig(BaseSettings):
    """Main application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Application environment",
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    # Nested configurations
    storage: StorageConfig = Field(default_factory=StorageConfig)
    aws: AWSConfig = Field(default_factory=AWSConfig)
    api: APIConfig = Field(default_factory=APIConfig)

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"
