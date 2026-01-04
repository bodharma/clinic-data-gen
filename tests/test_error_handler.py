"""Tests for FastAPI exception handlers.

Validates that custom exception handlers:
- Return correct HTTP status codes
- Provide consistent error response format
- Include request context (path, method)
- Handle all custom exception types
- Catch unexpected exceptions gracefully
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.exceptions import (
    AppException,
    GenerationError,
    InvalidGeneratorConfigError,
    DataGenerationFailedError,
    ValidationError,
    InvalidInputError,
    StorageError,
    FileOperationError,
    S3UploadError,
)
from core.middleware.error_handler import register_exception_handlers


@pytest.fixture
def app():
    """Create FastAPI app with exception handlers registered."""
    app = FastAPI()

    # Register all exception handlers
    register_exception_handlers(app)

    # Test endpoints that raise different exceptions
    @app.get("/test/validation-error")
    async def test_validation_error():
        raise ValidationError(
            "validation failed",
            details={"field": "email", "error": "invalid format"}
        )

    @app.get("/test/invalid-input-error")
    async def test_invalid_input_error():
        raise InvalidInputError(
            "unsupported format",
            details={"format": "xml", "supported": ["csv", "json"]}
        )

    @app.get("/test/invalid-config-error")
    async def test_invalid_config_error():
        raise InvalidGeneratorConfigError(
            "invalid member count",
            details={"count": -1, "min": 1}
        )

    @app.get("/test/generation-error")
    async def test_generation_error():
        raise GenerationError(
            "failed to generate data",
            details={"stage": "template_loading"}
        )

    @app.get("/test/data-generation-failed-error")
    async def test_data_generation_failed_error():
        raise DataGenerationFailedError(
            "template not found",
            details={"template": "insurance.csv"}
        )

    @app.get("/test/storage-error")
    async def test_storage_error():
        raise StorageError(
            "storage operation failed",
            details={"operation": "write"}
        )

    @app.get("/test/file-operation-error")
    async def test_file_operation_error():
        raise FileOperationError(
            "failed to create file",
            details={"path": "/tmp/test.csv"}
        )

    @app.get("/test/s3-upload-error")
    async def test_s3_upload_error():
        raise S3UploadError(
            "upload failed",
            details={"bucket": "test-bucket", "key": "data.csv"}
        )

    @app.get("/test/app-exception")
    async def test_app_exception():
        raise AppException(
            "generic app error",
            details={"code": "ERR_001"}
        )

    @app.get("/test/unexpected-error")
    async def test_unexpected_error():
        raise RuntimeError("something unexpected happened")

    @app.get("/test/zero-division")
    async def test_zero_division():
        return 1 / 0

    return app


@pytest.fixture
def client(app):
    """Create test client for the app.

    Set raise_server_exceptions=False to allow testing error handlers
    instead of re-raising exceptions in tests.
    """
    return TestClient(app, raise_server_exceptions=False)


class TestValidationErrorHandlers:
    """Test validation error handlers return 422."""

    def test_validation_error_returns_422(self, client):
        """ValidationError should return 422 Unprocessable Entity."""
        response = client.get("/test/validation-error")
        assert response.status_code == 422

        data = response.json()
        assert data["error"] == "ValidationError"
        assert data["message"] == "validation failed"
        assert data["details"]["field"] == "email"
        assert data["path"] == "/test/validation-error"
        assert data["method"] == "GET"

    def test_invalid_input_error_returns_422(self, client):
        """InvalidInputError should return 422 Unprocessable Entity."""
        response = client.get("/test/invalid-input-error")
        assert response.status_code == 422

        data = response.json()
        assert data["error"] == "InvalidInputError"
        assert data["message"] == "unsupported format"
        assert data["details"]["format"] == "xml"
        assert data["path"] == "/test/invalid-input-error"
        assert data["method"] == "GET"


class TestGeneratorConfigErrorHandlers:
    """Test invalid generator config returns 400."""

    def test_invalid_config_error_returns_400(self, client):
        """InvalidGeneratorConfigError should return 400 Bad Request."""
        response = client.get("/test/invalid-config-error")
        assert response.status_code == 400

        data = response.json()
        assert data["error"] == "InvalidGeneratorConfigError"
        assert data["message"] == "invalid member count"
        assert data["details"]["count"] == -1
        assert data["details"]["min"] == 1
        assert data["path"] == "/test/invalid-config-error"
        assert data["method"] == "GET"


class TestGenerationErrorHandlers:
    """Test generation errors return 500."""

    def test_generation_error_returns_500(self, client):
        """GenerationError should return 500 Internal Server Error."""
        response = client.get("/test/generation-error")
        assert response.status_code == 500

        data = response.json()
        assert data["error"] == "GenerationError"
        assert data["message"] == "failed to generate data"
        assert data["details"]["stage"] == "template_loading"
        assert data["path"] == "/test/generation-error"
        assert data["method"] == "GET"

    def test_data_generation_failed_error_returns_500(self, client):
        """DataGenerationFailedError should return 500."""
        response = client.get("/test/data-generation-failed-error")
        assert response.status_code == 500

        data = response.json()
        assert data["error"] == "DataGenerationFailedError"
        assert data["message"] == "template not found"
        assert data["details"]["template"] == "insurance.csv"
        assert data["path"] == "/test/data-generation-failed-error"


class TestStorageErrorHandlers:
    """Test storage errors return 500."""

    def test_storage_error_returns_500(self, client):
        """StorageError should return 500 Internal Server Error."""
        response = client.get("/test/storage-error")
        assert response.status_code == 500

        data = response.json()
        assert data["error"] == "StorageError"
        assert data["message"] == "storage operation failed"
        assert data["details"]["operation"] == "write"
        assert data["path"] == "/test/storage-error"
        assert data["method"] == "GET"

    def test_file_operation_error_returns_500(self, client):
        """FileOperationError should return 500."""
        response = client.get("/test/file-operation-error")
        assert response.status_code == 500

        data = response.json()
        assert data["error"] == "FileOperationError"
        assert data["message"] == "failed to create file"
        assert data["details"]["path"] == "/tmp/test.csv"
        assert data["path"] == "/test/file-operation-error"

    def test_s3_upload_error_returns_500(self, client):
        """S3UploadError should return 500."""
        response = client.get("/test/s3-upload-error")
        assert response.status_code == 500

        data = response.json()
        assert data["error"] == "S3UploadError"
        assert data["message"] == "upload failed"
        assert data["details"]["bucket"] == "test-bucket"
        assert data["details"]["key"] == "data.csv"
        assert data["path"] == "/test/s3-upload-error"


class TestGenericErrorHandlers:
    """Test generic and unexpected error handlers."""

    def test_app_exception_returns_500(self, client):
        """Generic AppException should return 500."""
        response = client.get("/test/app-exception")
        assert response.status_code == 500

        data = response.json()
        assert data["error"] == "AppException"
        assert data["message"] == "generic app error"
        assert data["details"]["code"] == "ERR_001"
        assert data["path"] == "/test/app-exception"
        assert data["method"] == "GET"

    def test_unexpected_error_returns_500(self, client):
        """Unexpected exceptions should return 500 with generic message."""
        response = client.get("/test/unexpected-error")
        assert response.status_code == 500

        data = response.json()
        assert data["error"] == "InternalServerError"
        assert data["message"] == "an unexpected error occurred"
        assert data["path"] == "/test/unexpected-error"
        assert data["method"] == "GET"
        # Should not leak exception details
        assert "details" not in data

    def test_zero_division_error_returns_500(self, client):
        """Zero division should be caught and return generic 500."""
        response = client.get("/test/zero-division")
        assert response.status_code == 500

        data = response.json()
        assert data["error"] == "InternalServerError"
        assert data["message"] == "an unexpected error occurred"
        assert data["path"] == "/test/zero-division"


class TestErrorResponseFormat:
    """Test that all error responses follow consistent format."""

    def test_error_response_has_required_fields(self, client):
        """All error responses should have error, message, path, method."""
        response = client.get("/test/validation-error")
        data = response.json()

        assert "error" in data
        assert "message" in data
        assert "path" in data
        assert "method" in data

    def test_error_response_with_details(self, client):
        """AppExceptions should include details if provided."""
        response = client.get("/test/s3-upload-error")
        data = response.json()

        assert "details" in data
        assert isinstance(data["details"], dict)
        assert len(data["details"]) > 0

    def test_unexpected_error_no_details(self, client):
        """Unexpected errors should not include details field."""
        response = client.get("/test/unexpected-error")
        data = response.json()

        # Should not leak implementation details
        assert "details" not in data


class TestRequestContext:
    """Test that request context is included in error responses."""

    def test_path_is_included(self, client):
        """Error response should include request path."""
        response = client.get("/test/validation-error")
        data = response.json()
        assert data["path"] == "/test/validation-error"

    def test_method_is_included(self, client):
        """Error response should include request method."""
        response = client.get("/test/validation-error")
        data = response.json()
        assert data["method"] == "GET"

    def test_different_paths_reflected(self, client):
        """Different endpoints should show different paths."""
        response1 = client.get("/test/validation-error")
        response2 = client.get("/test/generation-error")

        assert response1.json()["path"] != response2.json()["path"]


class TestExceptionHandlerRegistration:
    """Test that exception handlers are properly registered."""

    def test_register_exception_handlers_works(self):
        """Should be able to register handlers on a new app."""
        app = FastAPI()
        register_exception_handlers(app)

        # App should have exception handlers registered
        assert len(app.exception_handlers) > 0

    def test_all_custom_exceptions_handled(self, client):
        """All custom exception types should be handled."""
        test_endpoints = [
            "/test/validation-error",
            "/test/invalid-input-error",
            "/test/invalid-config-error",
            "/test/generation-error",
            "/test/data-generation-failed-error",
            "/test/storage-error",
            "/test/file-operation-error",
            "/test/s3-upload-error",
            "/test/app-exception",
        ]

        for endpoint in test_endpoints:
            response = client.get(endpoint)
            # Should return proper error response, not 500 with stack trace
            assert response.status_code in [400, 422, 500]
            data = response.json()
            assert "error" in data
            assert "message" in data
