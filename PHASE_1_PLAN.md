# Phase 1: Core Architecture - Implementation Plan

yo, this is the detailed plan for leveling up the architecture. we're moving from "everything in one file" to "actually maintainable code".

---

## Current State

**What we're working with:**
- 460-line `app.py` with all routes/logic mixed together
- 15+ generator modules (ranging from 125 to 1003 lines each)
- Direct instantiation everywhere - no DI, no service layer
- Inconsistent error handling (mix of HTTPException and random errors)
- No centralized config management
- Basic FastAPI setup with no middleware
- 45/56 tests passing (mostly endpoint tests)

**Code smells:**
- Fat controllers (routes doing business logic)
- Tight coupling (generators instantiated in routes)
- Hardcoded values (`/tmp/data/`, URLs, etc.)
- Repeated patterns (`create_storage_dir()`, file existence checks)
- No separation between HTTP concerns and business logic

---

## Implementation by Component

### 1. Config Management 🔥
**Priority: DO THIS FIRST** - everything else depends on it

**Agent:** `backend-developer`

**What we're building:**
- `/core/config.py` - Pydantic Settings v2 classes
- `/.env.example` - documented config template
- `/core/constants.py` - app-wide constants

**What gets configured:**
- Storage paths (replace hardcoded `/tmp/data/`)
- API settings (CORS, rate limits, etc.)
- S3 settings (bucket names, regions)
- External API URLs (currently hardcoded)
- Log levels and formats

**Structure:**
```
core/
├── __init__.py
├── config.py          # Settings classes
└── constants.py       # App-wide constants
```

**Example pattern:**
```python
from pydantic_settings import BaseSettings

class StorageConfig(BaseSettings):
    data_dir: Path = Path("/tmp/data")
    s3_bucket: str | None = None

    class Config:
        env_prefix = "STORAGE_"

class AppConfig(BaseSettings):
    storage: StorageConfig = StorageConfig()
    debug: bool = False

    class Config:
        env_file = ".env"
```

---

### 2. Error Handling & Custom Exceptions
**Priority: DO SECOND** - needed before service layer

**Agent:** `python-pro`

**What we're building:**
- `/core/exceptions.py` - custom exception hierarchy
- `/core/middleware/error_handler.py` - FastAPI exception handlers

**Exception hierarchy:**
```
AppException (base)
├── GenerationError
│   ├── InvalidGeneratorConfigError
│   └── DataGenerationFailedError
├── ValidationError
│   └── InvalidInputError
└── StorageError
    ├── FileNotFoundError
    └── S3UploadError
```

**Structure:**
```
core/
├── exceptions.py
└── middleware/
    ├── __init__.py
    └── error_handler.py
```

**Pattern:**
```python
class AppException(Exception):
    """base exception for the app"""
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}

class GenerationError(AppException):
    """something went wrong generating data"""
    pass

# In middleware:
@app.exception_handler(GenerationError)
async def generation_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": exc.message, "details": exc.details}
    )
```

---

### 3. Logging Setup
**Priority: DO THIRD** - needed for observability during refactor

**Agent:** `backend-developer`

**What we're building:**
- `/core/logging.py` - structured logging setup
- `/core/middleware/logging_middleware.py` - request/response logging

**What gets logged:**
- Request/response (with timing)
- Generator operations (which generator, how many records)
- File operations (paths, sizes)
- S3 operations (bucket, key, success/failure)
- Errors (with full context)

**Structure:**
```
core/
├── logging.py
└── middleware/
    └── logging_middleware.py
```

**Tech stack:**
- `structlog` for structured logging
- JSON formatter for production
- Human-readable for dev

**Pattern:**
```python
import structlog

logger = structlog.get_logger()

# In service:
logger.info("generating_members", count=100, format="csv")

# Output:
# {"event": "generating_members", "count": 100, "format": "csv", "timestamp": "..."}
```

---

### 4. Service Layer Pattern
**Priority: DO FOURTH** - the big refactor

**Agents:** `backend-developer` (primary) + `python-pro` (patterns review)

**What we're building:**
```
services/
├── __init__.py
├── base.py                    # Base service class
├── generation/
│   ├── __init__.py
│   ├── member_service.py      # MemberRoster logic
│   ├── edi_service.py         # EDI generation logic
│   ├── testing_service.py     # TestingData logic
│   ├── vaccine_service.py     # Vaccine data logic
│   └── rt_service.py          # RT data services
├── storage/
│   ├── __init__.py
│   ├── file_service.py        # Local file operations
│   └── s3_service.py          # S3 operations
└── conversion/
    ├── __init__.py
    └── format_service.py      # CSV/JSON/EDI conversions
```

**Service responsibilities:**
- `MemberService`: wraps MemberRoster, handles generation logic
- `EDIService`: EDI document creation/writing
- `StorageService`: file system and S3 operations
- `ConversionService`: format transformations
- `TestingDataService`: testing data generation
- `VaccineService`: vaccine data generation
- `RTService`: RT eligibility/claim/benefit data

**Pattern:**
```python
class GenerationService:
    def __init__(self, storage_service: StorageService, config: AppConfig):
        self.storage = storage_service
        self.config = config

    async def generate_members(self, count: int) -> Path:
        # business logic here
        # returns file path, no HTTP concerns
        pass
```

**Files to refactor:**
- Extract logic from `app.py` routes
- Keep generators as-is (they're fine as data generators)
- Routes become thin controllers

---

### 5. Dependency Injection Container
**Priority: DO FIFTH** - after services exist

**Agent:** `backend-developer`

**What we're building:**
- `/core/dependencies.py` - service factory functions
- `/core/container.py` - optional DI container

**DI approach:**
```python
# dependencies.py
def get_config() -> AppConfig:
    return AppConfig()  # Singleton

def get_storage_service(config: AppConfig = Depends(get_config)) -> StorageService:
    return StorageService(config)

def get_member_service(
    storage: StorageService = Depends(get_storage_service),
    config: AppConfig = Depends(get_config)
) -> MemberService:
    return MemberService(storage, config)

# In routes:
@app.get("/members/csv")
async def get_members(
    service: MemberService = Depends(get_member_service)
):
    return await service.generate_csv(...)
```

**Structure:**
```
core/
├── dependencies.py    # Dependency providers
└── container.py       # Optional DI container
```

---

### 6. Route Refactoring
**Priority: DO LAST** - after everything else is ready

**Agent:** `backend-developer`

**What we're building:**
```
api/
├── __init__.py
├── routes/
│   ├── __init__.py
│   ├── health.py          # Health check endpoint
│   ├── members.py         # Member routes
│   ├── edi.py             # EDI routes
│   ├── testing.py         # Testing data routes
│   ├── vaccines.py        # Vaccine routes
│   └── realtime.py        # RT eligibility/claim routes
└── models/
    ├── __init__.py
    ├── requests.py        # Pydantic request models
    └── responses.py       # Pydantic response models
```

**Refactor `app.py`:**
- Remove all route handlers (move to route modules)
- Keep only app creation, middleware setup, route registration
- Add startup/shutdown events
- Clean up imports

**Route pattern:**
```python
# api/routes/members.py
router = APIRouter(prefix="/members", tags=["members"])

@router.get("/csv")
async def get_members_csv(
    members_num: int = Query(1, gt=0),
    service: MemberService = Depends(get_member_service)
) -> FileResponse:
    try:
        filepath = await service.generate_members_csv(members_num)
        return FileResponse(filepath, media_type="text/csv")
    except GenerationError as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Implementation Order

### Foundation (do these first)
1. Config management (`backend-developer`)
2. Error handling (`python-pro`)
3. Logging setup (`backend-developer`)
4. Review foundation (`architecture-reviewer`)

### Services (the big refactor)
5. Create service layer structure (`backend-developer`)
6. Implement storage services (`backend-developer`)
7. Implement generation services (member, EDI) (`backend-developer`)
8. Review service patterns (`architecture-reviewer` + `python-pro`)

### Integration (wire it all up)
9. Implement remaining services (testing, vaccine, RT) (`backend-developer`)
10. Setup DI container (`backend-developer`)
11. Review DI patterns (`python-pro`)

### Routes & Testing (finish strong)
12. Refactor routes to use services (`backend-developer`)
13. Update tests for new structure (`backend-developer`)
14. Final code review (`code-reviewer`)
15. Architecture validation (`architecture-reviewer`)

---

## Key Architectural Decisions

### 1. DI Approach: FastAPI Depends vs Custom Container
**Decision:** Use FastAPI `Depends()` pattern

**Why:**
- Native to FastAPI, well-documented
- No additional dependencies
- Request-scoped injection out of the box
- Testing is straightforward (override dependencies)

**When to reconsider:** If we need complex lifecycle management

---

### 2. Config Management: Pydantic Settings vs python-decouple
**Decision:** Pydantic Settings v2

**Why:**
- Already using Pydantic for request validation
- Type safety and validation built-in
- Nice IDE autocomplete
- Consistent with FastAPI ecosystem

---

### 3. Logging: structlog vs loguru vs stdlib
**Decision:** structlog

**Why:**
- Structured logging is portfolio-worthy
- JSON output for production
- Thread-safe for async
- Performance is good enough

**Alternative:** Keep it simple with loguru if structlog is overkill

---

### 4. Service Layer Granularity
**Decision:** One service per domain (MemberService, EDIService, etc.)

**Why:**
- Matches current generator organization
- Clear boundaries
- Easy to test
- Not over-engineered

**Avoid:** Micro-services, complex service hierarchies, service orchestrators

---

### 5. Error Handling Strategy
**Decision:** Domain exceptions + middleware translation

**Why:**
- Services throw domain exceptions (GenerationError)
- Middleware translates to HTTP responses
- Clear separation between business and HTTP layer
- Easy to test business logic without HTTP concerns

---

## Files That Will Be Created

```
clinical-data-generator/
├── core/
│   ├── __init__.py
│   ├── config.py              # NEW - Pydantic settings
│   ├── constants.py           # NEW - App constants
│   ├── exceptions.py          # NEW - Custom exceptions
│   ├── logging.py             # NEW - Logging setup
│   ├── dependencies.py        # NEW - DI providers
│   ├── container.py           # NEW - Optional DI container
│   └── middleware/
│       ├── __init__.py
│       ├── error_handler.py   # NEW - Error middleware
│       └── logging_middleware.py  # NEW - Request logging
├── services/
│   ├── __init__.py
│   ├── base.py                # NEW - Base service
│   ├── generation/
│   │   ├── __init__.py
│   │   ├── member_service.py  # NEW
│   │   ├── edi_service.py     # NEW
│   │   ├── testing_service.py # NEW
│   │   ├── vaccine_service.py # NEW
│   │   └── rt_service.py      # NEW
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── file_service.py    # NEW
│   │   └── s3_service.py      # NEW
│   └── conversion/
│       ├── __init__.py
│       └── format_service.py  # NEW
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py          # NEW
│   │   ├── members.py         # NEW - from app.py
│   │   ├── edi.py             # NEW - from app.py
│   │   ├── testing.py         # NEW - from app.py
│   │   ├── vaccines.py        # NEW - from app.py
│   │   └── realtime.py        # NEW - from app.py
│   └── models/
│       ├── __init__.py
│       ├── requests.py        # NEW - move from app.py
│       └── responses.py       # NEW
├── .env.example               # NEW
└── app.py                     # REFACTOR - just app setup
```

---

## Files That Will Be Refactored

```
clinical-data-generator/
├── app.py                                  # MAJOR REFACTOR - extract routes
├── generate_raw_data.py                    # MINOR - add error handling
├── generate_edi.py                         # MINOR - add error handling
├── generate_testing_data.py                # MINOR - add error handling
├── generate_vaccine_data.py                # MINOR - add error handling
├── generate_rt_*.py                        # MINOR - add error handling
└── tests/test_app.py                       # UPDATE - use DI for testing
```

---

## Testing Strategy

**What needs testing:**
- Config validation (required fields, type checking)
- Service layer logic (mock dependencies)
- Error handling (exception mapping)
- DI container (dependency resolution)
- Routes (integration tests with overridden dependencies)

**Test structure:**
```
tests/
├── unit/
│   ├── test_config.py
│   ├── test_exceptions.py
│   ├── services/
│   │   ├── test_member_service.py
│   │   ├── test_storage_service.py
│   │   └── ...
├── integration/
│   ├── test_routes_members.py
│   ├── test_routes_edi.py
│   └── ...
└── conftest.py                  # Fixtures for DI override
```

---

## Success Metrics

**Phase 1 is done when:**
- ✅ All config is in Pydantic Settings (no hardcoded values)
- ✅ Custom exception hierarchy exists and is used everywhere
- ✅ Structured logging is working (JSON output)
- ✅ Service layer exists for all major operations
- ✅ DI container provides all dependencies
- ✅ Routes are thin controllers (< 20 lines each)
- ✅ All 45+ tests still pass (or more)
- ✅ New tests for services exist
- ✅ No breaking changes to API contracts

---

## Agent Assignment Summary

| Component | Primary Agent | Reviewer | Why |
|-----------|--------------|----------|-----|
| Config Management | `backend-developer` | `architecture-reviewer` | Pydantic Settings expertise |
| Error Handling | `python-pro` | `code-reviewer` | Pythonic exception patterns |
| Logging | `backend-developer` | `architecture-reviewer` | Async/middleware knowledge |
| Service Layer | `backend-developer` | `architecture-reviewer`, `python-pro` | Complex FastAPI refactor |
| DI Container | `backend-developer` | `python-pro` | FastAPI Depends pattern |
| Routes | `backend-developer` | `code-reviewer` | FastAPI routes |
| Final Review | `architecture-reviewer` | - | Overall design validation |

---

**Last Updated:** 2026-01-04
**Status:** Ready to start

---

*let's build something clean*
