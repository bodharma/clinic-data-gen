"""Custom exception hierarchy for clinical data generator.

Provides domain-specific exceptions that separate business logic errors
from HTTP concerns. All exceptions inherit from a base AppException
that carries a message and optional details dict.
"""


class AppException(Exception):
    """Base exception for all application errors.

    All custom exceptions should inherit from this to provide
    consistent error handling throughout the app.

    Args:
        message: Human-readable error message
        details: Optional dict with additional context (error codes, field names, etc.)

    Example:
        raise AppException(
            "failed to process request",
            details={"field": "member_id", "value": "invalid"}
        )
    """

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class GenerationError(AppException):
    """Raised when data generation fails.

    This covers any failure in the data generation process,
    including member rosters, EDI documents, vaccine data, etc.
    """
    pass


class InvalidGeneratorConfigError(GenerationError):
    """Invalid configuration passed to a generator.

    Raised when generator receives invalid parameters like
    negative counts, unsupported formats, or missing required fields.

    Example:
        raise InvalidGeneratorConfigError(
            "invalid member count",
            details={"members_count": -1, "min_required": 1}
        )
    """
    pass


class DataGenerationFailedError(GenerationError):
    """Data generation operation failed during execution.

    Raised when the generation process starts but fails midway,
    such as template loading errors or data processing failures.

    Example:
        raise DataGenerationFailedError(
            "failed to load insurance template",
            details={"template": "insurance_master.csv", "error": str(e)}
        )
    """
    pass


class ValidationError(AppException):
    """Raised when input validation fails.

    This is for validating user input before processing,
    distinct from Pydantic's validation which handles request parsing.
    """
    pass


class InvalidInputError(ValidationError):
    """User provided invalid input data.

    Raised when input fails business rule validation
    (e.g., incompatible field combinations, invalid enum values).

    Example:
        raise InvalidInputError(
            "unsupported file format combination",
            details={
                "download_format": "csv",
                "s3_format": "xml",
                "supported_combinations": ["csv->json", "csv->jsonlike"]
            }
        )
    """
    pass


class StorageError(AppException):
    """Raised when file or cloud storage operations fail.

    Covers both local filesystem and S3 operations.
    """
    pass


class FileOperationError(StorageError):
    """Local file operation failed.

    Raised when file creation, reading, or writing fails.

    Example:
        raise FileOperationError(
            "failed to create output directory",
            details={"path": "/tmp/data", "error": str(e)}
        )
    """
    pass


class S3UploadError(StorageError):
    """S3 upload operation failed.

    Raised when S3 uploads fail due to credentials, network,
    or permission issues.

    Example:
        raise S3UploadError(
            "failed to upload to S3",
            details={
                "bucket": "dev-de-phi-backup",
                "key": "data.csv",
                "error": "missing AWS credentials"
            }
        )
    """
    pass
