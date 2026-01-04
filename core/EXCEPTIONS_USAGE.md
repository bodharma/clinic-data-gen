# Exception Handling Usage Guide

## Quick Start

### 1. Register handlers in your FastAPI app

```python
from fastapi import FastAPI
from core.middleware.error_handler import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
```

### 2. Use custom exceptions in your endpoints

```python
from core.exceptions import (
    InvalidGeneratorConfigError,
    DataGenerationFailedError,
    InvalidInputError,
    FileOperationError,
    S3UploadError,
)

@app.post("/generate/members")
async def generate_members(count: int):
    # Validate input
    if count < 1:
        raise InvalidGeneratorConfigError(
            "member count must be positive",
            details={"count": count, "min_required": 1}
        )

    # Generate data
    try:
        members = MemberRoster().generate(count)
    except Exception as e:
        raise DataGenerationFailedError(
            "failed to generate member data",
            details={"error": str(e), "requested_count": count}
        )

    # Save to file
    try:
        filename = save_to_csv(members)
    except OSError as e:
        raise FileOperationError(
            "failed to save CSV file",
            details={"error": str(e), "path": filepath}
        )

    return {"filename": filename, "count": len(members)}
```

## Exception Hierarchy

```
AppException (base)
├── GenerationError (500)
│   ├── InvalidGeneratorConfigError (400)
│   └── DataGenerationFailedError (500)
├── ValidationError (422)
│   └── InvalidInputError (422)
└── StorageError (500)
    ├── FileOperationError (500)
    └── S3UploadError (500)
```

## Error Response Format

All exceptions return consistent JSON:

```json
{
  "error": "InvalidGeneratorConfigError",
  "message": "member count must be positive",
  "details": {
    "count": -1,
    "min_required": 1
  },
  "path": "/generate/members",
  "method": "POST"
}
```

## When to Use Which Exception

### InvalidGeneratorConfigError (400)
User provided invalid configuration to a generator
- Negative counts
- Invalid format options
- Missing required fields

### DataGenerationFailedError (500)
Data generation process failed during execution
- Template file not found
- CSV parsing errors
- Data processing failures

### InvalidInputError (422)
Input doesn't meet business rules
- Unsupported format combinations
- Invalid enum values
- Incompatible field combinations

### FileOperationError (500)
Local file operations failed
- Permission denied
- Directory creation failed
- File write errors

### S3UploadError (500)
S3 upload operations failed
- Missing AWS credentials
- Network errors
- Permission issues

## Example: Replacing HTTPException

### Before (using HTTPException)
```python
if not Path(filename).exists():
    raise HTTPException(
        status_code=404,
        detail=f"File with path: {filename} not found"
    )
```

### After (using custom exceptions)
```python
if not Path(filename).exists():
    raise FileOperationError(
        "generated file not found",
        details={"path": filename, "expected": True}
    )
```

## Benefits

1. **Separation of Concerns**: Business logic doesn't know about HTTP
2. **Consistent Format**: All errors follow same JSON structure
3. **Better Logging**: Automatic logging with full context
4. **Type Safety**: Can catch specific exception types
5. **Rich Context**: Details dict carries structured error data
