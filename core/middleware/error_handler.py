"""FastAPI exception handlers for custom application exceptions.

Maps domain-specific exceptions to appropriate HTTP responses
with consistent error format and proper status codes.
"""

import traceback
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse

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


def _create_error_response(
    request: Request,
    exc: Exception,
    status_code: int,
    error_name: str | None = None,
) -> dict[str, Any]:
    """Create standardized error response dict.

    Args:
        request: FastAPI request object
        exc: The exception that was raised
        status_code: HTTP status code to return
        error_name: Override for the error name (defaults to exception class name)

    Returns:
        Dict with error, message, details, path, and method fields
    """
    error_data = {
        "error": error_name or exc.__class__.__name__,
        "path": str(request.url.path),
        "method": request.method,
    }

    # Add message and details if it's an AppException
    if isinstance(exc, AppException):
        error_data["message"] = exc.message
        error_data["details"] = exc.details
    else:
        error_data["message"] = str(exc)

    return error_data


async def validation_error_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    """Handle validation errors with 422 Unprocessable Entity.

    Validation errors indicate that the user provided input that
    doesn't meet business rules (distinct from request parsing errors).

    Args:
        request: FastAPI request object
        exc: The validation exception that was raised

    Returns:
        JSONResponse with 422 status and error details
    """
    print(f"[ValidationError] {exc.message} | Path: {request.url.path}")
    if exc.details:
        print(f"[ValidationError] Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_create_error_response(request, exc, status.HTTP_422_UNPROCESSABLE_ENTITY),
    )


async def invalid_input_error_handler(
    request: Request, exc: InvalidInputError
) -> JSONResponse:
    """Handle invalid input errors with 422 Unprocessable Entity.

    More specific validation handler for input-specific errors.

    Args:
        request: FastAPI request object
        exc: The invalid input exception that was raised

    Returns:
        JSONResponse with 422 status and error details
    """
    print(f"[InvalidInputError] {exc.message} | Path: {request.url.path}")
    if exc.details:
        print(f"[InvalidInputError] Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_create_error_response(request, exc, status.HTTP_422_UNPROCESSABLE_ENTITY),
    )


async def invalid_generator_config_error_handler(
    request: Request, exc: InvalidGeneratorConfigError
) -> JSONResponse:
    """Handle invalid generator configuration with 400 Bad Request.

    Generator config errors are user errors (bad parameters)
    so we use 400 instead of 500.

    Args:
        request: FastAPI request object
        exc: The invalid config exception that was raised

    Returns:
        JSONResponse with 400 status and error details
    """
    print(f"[InvalidGeneratorConfigError] {exc.message} | Path: {request.url.path}")
    if exc.details:
        print(f"[InvalidGeneratorConfigError] Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=_create_error_response(request, exc, status.HTTP_400_BAD_REQUEST),
    )


async def generation_error_handler(
    request: Request, exc: GenerationError
) -> JSONResponse:
    """Handle data generation errors with 500 Internal Server Error.

    Generation failures are server-side issues (template loading,
    data processing, etc.) so we use 500.

    Args:
        request: FastAPI request object
        exc: The generation exception that was raised

    Returns:
        JSONResponse with 500 status and error details
    """
    print(f"[GenerationError] {exc.message} | Path: {request.url.path}")
    if exc.details:
        print(f"[GenerationError] Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_create_error_response(request, exc, status.HTTP_500_INTERNAL_SERVER_ERROR),
    )


async def storage_error_handler(
    request: Request, exc: StorageError
) -> JSONResponse:
    """Handle storage errors with 500 Internal Server Error.

    Storage failures (file I/O, S3 uploads) are server-side issues.

    Args:
        request: FastAPI request object
        exc: The storage exception that was raised

    Returns:
        JSONResponse with 500 status and error details
    """
    print(f"[StorageError] {exc.message} | Path: {request.url.path}")
    if exc.details:
        print(f"[StorageError] Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_create_error_response(request, exc, status.HTTP_500_INTERNAL_SERVER_ERROR),
    )


async def app_exception_handler(
    request: Request, exc: AppException
) -> JSONResponse:
    """Handle generic app exceptions with 500 Internal Server Error.

    Catch-all handler for any AppException that doesn't have
    a more specific handler.

    Args:
        request: FastAPI request object
        exc: The app exception that was raised

    Returns:
        JSONResponse with 500 status and error details
    """
    print(f"[AppException] {exc.message} | Path: {request.url.path}")
    if exc.details:
        print(f"[AppException] Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_create_error_response(request, exc, status.HTTP_500_INTERNAL_SERVER_ERROR),
    )


async def generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions with 500 Internal Server Error.

    Catch-all for any exception that isn't an AppException.
    Logs the full traceback for debugging but returns a generic
    message to avoid leaking sensitive information.

    Args:
        request: FastAPI request object
        exc: The unexpected exception that was raised

    Returns:
        JSONResponse with 500 status and generic error message
    """
    # Log the full traceback for debugging
    print(f"[UnexpectedException] {exc.__class__.__name__}: {str(exc)}")
    print(f"[UnexpectedException] Path: {request.url.path} | Method: {request.method}")
    print("[UnexpectedException] Traceback:")
    print(traceback.format_exc())

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "an unexpected error occurred",
            "path": str(request.url.path),
            "method": request.method,
        },
    )


def register_exception_handlers(app) -> None:
    """Register all exception handlers with the FastAPI app.

    Call this function during app initialization to set up
    all custom exception handlers.

    Args:
        app: FastAPI application instance

    Example:
        from fastapi import FastAPI
        from core.middleware.error_handler import register_exception_handlers

        app = FastAPI()
        register_exception_handlers(app)
    """
    # Register specific exception handlers first (more specific to less specific)
    app.add_exception_handler(InvalidInputError, invalid_input_error_handler)
    app.add_exception_handler(InvalidGeneratorConfigError, invalid_generator_config_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(DataGenerationFailedError, generation_error_handler)
    app.add_exception_handler(GenerationError, generation_error_handler)
    app.add_exception_handler(FileOperationError, storage_error_handler)
    app.add_exception_handler(S3UploadError, storage_error_handler)
    app.add_exception_handler(StorageError, storage_error_handler)
    app.add_exception_handler(AppException, app_exception_handler)

    # Catch-all for unexpected exceptions (must be last)
    app.add_exception_handler(Exception, generic_exception_handler)
