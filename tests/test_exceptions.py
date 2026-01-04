"""Tests for custom exception classes.

Validates that all custom exceptions:
- Can be raised and caught properly
- Carry message and details correctly
- Maintain proper inheritance hierarchy
- Work with isinstance checks
"""

import pytest

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


class TestAppException:
    """Test the base AppException class."""

    def test_app_exception_with_message(self):
        """Should create exception with message and empty details."""
        exc = AppException("test error")
        assert exc.message == "test error"
        assert exc.details == {}
        assert str(exc) == "test error"

    def test_app_exception_with_details(self):
        """Should create exception with message and details dict."""
        exc = AppException("test error", details={"key": "value", "count": 42})
        assert exc.message == "test error"
        assert exc.details == {"key": "value", "count": 42}

    def test_app_exception_can_be_raised(self):
        """Should be raisable and catchable."""
        with pytest.raises(AppException) as exc_info:
            raise AppException("something went wrong")

        assert exc_info.value.message == "something went wrong"

    def test_app_exception_inherits_from_exception(self):
        """Should inherit from built-in Exception."""
        exc = AppException("test")
        assert isinstance(exc, Exception)


class TestGenerationError:
    """Test GenerationError and its subclasses."""

    def test_generation_error_inheritance(self):
        """Should inherit from AppException."""
        exc = GenerationError("generation failed")
        assert isinstance(exc, GenerationError)
        assert isinstance(exc, AppException)
        assert isinstance(exc, Exception)

    def test_generation_error_with_details(self):
        """Should carry details about the failure."""
        exc = GenerationError(
            "failed to generate members",
            details={"requested": 100, "generated": 50}
        )
        assert exc.message == "failed to generate members"
        assert exc.details["requested"] == 100
        assert exc.details["generated"] == 50

    def test_invalid_generator_config_error_inheritance(self):
        """Should inherit from GenerationError."""
        exc = InvalidGeneratorConfigError("bad config")
        assert isinstance(exc, InvalidGeneratorConfigError)
        assert isinstance(exc, GenerationError)
        assert isinstance(exc, AppException)
        assert isinstance(exc, Exception)

    def test_invalid_generator_config_error_with_details(self):
        """Should provide details about invalid configuration."""
        exc = InvalidGeneratorConfigError(
            "invalid member count",
            details={"members_count": -1, "min_required": 1}
        )
        assert exc.message == "invalid member count"
        assert exc.details["members_count"] == -1
        assert exc.details["min_required"] == 1

    def test_data_generation_failed_error_inheritance(self):
        """Should inherit from GenerationError."""
        exc = DataGenerationFailedError("processing failed")
        assert isinstance(exc, DataGenerationFailedError)
        assert isinstance(exc, GenerationError)
        assert isinstance(exc, AppException)

    def test_data_generation_failed_error_with_details(self):
        """Should provide details about the failure."""
        exc = DataGenerationFailedError(
            "template not found",
            details={"template": "insurance.csv", "path": "/templates/"}
        )
        assert exc.message == "template not found"
        assert exc.details["template"] == "insurance.csv"


class TestValidationError:
    """Test ValidationError and its subclasses."""

    def test_validation_error_inheritance(self):
        """Should inherit from AppException."""
        exc = ValidationError("validation failed")
        assert isinstance(exc, ValidationError)
        assert isinstance(exc, AppException)
        assert isinstance(exc, Exception)

    def test_validation_error_with_details(self):
        """Should carry validation failure details."""
        exc = ValidationError(
            "invalid field",
            details={"field": "email", "value": "not-an-email"}
        )
        assert exc.message == "invalid field"
        assert exc.details["field"] == "email"

    def test_invalid_input_error_inheritance(self):
        """Should inherit from ValidationError."""
        exc = InvalidInputError("bad input")
        assert isinstance(exc, InvalidInputError)
        assert isinstance(exc, ValidationError)
        assert isinstance(exc, AppException)

    def test_invalid_input_error_with_details(self):
        """Should provide details about invalid input."""
        exc = InvalidInputError(
            "unsupported format combination",
            details={
                "download_format": "csv",
                "s3_format": "xml",
                "supported": ["csv->json", "csv->jsonlike"]
            }
        )
        assert exc.message == "unsupported format combination"
        assert exc.details["download_format"] == "csv"
        assert exc.details["s3_format"] == "xml"
        assert "supported" in exc.details


class TestStorageError:
    """Test StorageError and its subclasses."""

    def test_storage_error_inheritance(self):
        """Should inherit from AppException."""
        exc = StorageError("storage failed")
        assert isinstance(exc, StorageError)
        assert isinstance(exc, AppException)
        assert isinstance(exc, Exception)

    def test_storage_error_with_details(self):
        """Should carry storage operation details."""
        exc = StorageError(
            "failed to access storage",
            details={"operation": "write", "path": "/tmp/data"}
        )
        assert exc.message == "failed to access storage"
        assert exc.details["operation"] == "write"

    def test_file_operation_error_inheritance(self):
        """Should inherit from StorageError."""
        exc = FileOperationError("file error")
        assert isinstance(exc, FileOperationError)
        assert isinstance(exc, StorageError)
        assert isinstance(exc, AppException)

    def test_file_operation_error_with_details(self):
        """Should provide details about file operation failure."""
        exc = FileOperationError(
            "failed to create directory",
            details={"path": "/tmp/data", "error": "permission denied"}
        )
        assert exc.message == "failed to create directory"
        assert exc.details["path"] == "/tmp/data"
        assert exc.details["error"] == "permission denied"

    def test_s3_upload_error_inheritance(self):
        """Should inherit from StorageError."""
        exc = S3UploadError("s3 upload failed")
        assert isinstance(exc, S3UploadError)
        assert isinstance(exc, StorageError)
        assert isinstance(exc, AppException)

    def test_s3_upload_error_with_details(self):
        """Should provide details about S3 upload failure."""
        exc = S3UploadError(
            "upload failed",
            details={
                "bucket": "dev-de-phi-backup",
                "key": "data.csv",
                "error": "invalid credentials"
            }
        )
        assert exc.message == "upload failed"
        assert exc.details["bucket"] == "dev-de-phi-backup"
        assert exc.details["key"] == "data.csv"


class TestExceptionCatching:
    """Test that exceptions can be caught at different levels."""

    def test_catch_specific_exception(self):
        """Should be able to catch specific exception type."""
        with pytest.raises(InvalidInputError):
            raise InvalidInputError("bad input")

    def test_catch_parent_exception(self):
        """Should be able to catch using parent exception type."""
        with pytest.raises(ValidationError):
            raise InvalidInputError("bad input")

    def test_catch_grandparent_exception(self):
        """Should be able to catch using grandparent exception type."""
        with pytest.raises(AppException):
            raise InvalidInputError("bad input")

    def test_catch_base_exception(self):
        """Should be able to catch using base Exception type."""
        with pytest.raises(Exception):
            raise InvalidInputError("bad input")

    def test_catch_and_inspect_details(self):
        """Should be able to inspect exception details after catching."""
        try:
            raise S3UploadError(
                "upload failed",
                details={"bucket": "test-bucket", "retry_count": 3}
            )
        except StorageError as e:
            assert e.message == "upload failed"
            assert e.details["bucket"] == "test-bucket"
            assert e.details["retry_count"] == 3
