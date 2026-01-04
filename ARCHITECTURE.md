# Clinical Data Generator - Architecture Overview

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Web UI     │  │  API Client  │  │   CLI Tool   │         │
│  │  (Future)    │  │   (cURL)     │  │   (Future)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────┴────────────────────────────────────┐
│                      API Gateway Layer                          │
│                        (FastAPI)                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Rate Limiting │ CORS │ Auth │ Security Headers │ Logging│  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Members    │  │     EDI      │  │    FHIR      │        │
│  │   Routes     │  │   Routes     │  │   Routes     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                      Service Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Generation  │  │  Validation  │  │   Storage    │        │
│  │   Service    │  │   Service    │  │   Service    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                   Domain/Business Logic Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Member     │  │    Claim     │  │   Vaccine    │        │
│  │  Generator   │  │  Generator   │  │  Generator   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Eligibility  │  │     RT       │  │     FHIR     │        │
│  │  Generator   │  │  Generators  │  │  Generator   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    Format Conversion Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │     EDI      │  │     CSV      │  │     JSON     │        │
│  │   Adapter    │  │  Formatter   │  │  Formatter   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐                           │
│  │   Protobuf   │  │    FHIR      │                           │
│  │   Adapter    │  │  Formatter   │                           │
│  └──────────────┘  └──────────────┘                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    Data Access Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  File System │  │      S3      │  │   MongoDB    │        │
│  │   Storage    │  │   Storage    │  │  (Optional)  │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Descriptions

### 1. API Gateway Layer (FastAPI)

**Responsibilities**:
- HTTP request handling
- Request validation
- Response formatting
- Middleware execution (CORS, rate limiting, security headers)
- API documentation (Swagger/OpenAPI)
- Authentication/authorization

**Key Components**:
- `main.py`: Application entry point
- `routes/`: Endpoint definitions organized by domain
- `middleware.py`: Cross-cutting concerns
- `dependencies.py`: Dependency injection setup

**Technology Stack**:
- FastAPI 0.115+
- Uvicorn (ASGI server)
- Pydantic v2 (validation)

---

### 2. Service Layer

**Responsibilities**:
- Orchestrate business logic
- Coordinate between generators and formatters
- Handle cross-cutting concerns (logging, caching)
- External API integration
- File storage management

**Key Services**:

**GenerationService**:
```python
class GenerationService:
    """Orchestrates data generation workflow"""

    async def generate_and_save(
        self,
        generator_type: str,
        count: int,
        format: str
    ) -> GenerationResult:
        # 1. Create appropriate generator
        # 2. Generate data
        # 3. Validate data
        # 4. Format data
        # 5. Save to storage
        # 6. Return result metadata
```

**ValidationService**:
```python
class ValidationService:
    """Validates generated data against standards"""

    def validate_edi_x12(self, edi_data: str) -> ValidationResult:
        # EDI X12 validation logic

    def validate_fhir(self, fhir_resource: dict) -> ValidationResult:
        # FHIR resource validation
```

**StorageService**:
```python
class StorageService:
    """Abstract storage operations"""

    async def save(self, data: bytes, filename: str) -> str:
        # Delegates to appropriate storage backend
```

---

### 3. Domain/Business Logic Layer

**Responsibilities**:
- Core data generation logic
- Business rule enforcement
- Domain model definitions
- Data relationship management

**Generator Pattern**:
```python
class BaseGenerator(ABC):
    """All generators inherit from this base"""

    @abstractmethod
    def generate_single(self) -> T:
        """Generate one record"""

    def generate(self, count: int) -> List[T]:
        """Generate multiple records"""

    @abstractmethod
    def validate(self, record: T) -> bool:
        """Validate generated record"""
```

**Generator Types**:

| Generator | Purpose | Output Schema |
|-----------|---------|---------------|
| MemberGenerator | Patient/member demographics | MemberSchema |
| ClaimGenerator | Insurance claims | ClaimSchema |
| EligibilityGenerator | Benefit eligibility | EligibilitySchema |
| VaccineGenerator | Vaccine encounters | VaccineSchema |
| RTClaimGenerator | Real-time claim data | RTClaimSchema |
| FHIRGenerator | FHIR resources | FHIR ResourceType |

**Data Relationships**:
```
Member (1) ──< (N) Claims
Member (1) ──< (N) Vaccine Encounters
Member (N) ──> (1) Plan
Member (N) ──> (1) Sponsor
Claim (N) ──> (1) Provider
Claim (1) ──< (N) Claim Lines
```

---

### 4. Format Conversion Layer

**Responsibilities**:
- Convert domain objects to specific formats
- Format-specific validation
- Template processing (for EDI)
- Schema compliance

**Adapter Pattern Implementation**:
```python
class FormatAdapter(ABC):
    """Base adapter for all format conversions"""

    @abstractmethod
    def convert(self, data: List[Dict]) -> bytes:
        """Convert data to target format"""

    @abstractmethod
    def get_content_type(self) -> str:
        """Return MIME type for format"""
```

**Format Adapters**:

| Adapter | Input | Output | Use Case |
|---------|-------|--------|----------|
| EDIAdapter | Member/Claim data | EDI X12 837/834 | Insurance transactions |
| CSVAdapter | Any domain object | CSV file | Data analysis |
| JSONAdapter | Any domain object | JSON | API integration |
| ProtobufAdapter | Domain objects | Binary protobuf | High-performance APIs |
| FHIRAdapter | Clinical data | FHIR JSON/XML | Healthcare interop |

---

### 5. Data Access Layer

**Responsibilities**:
- Abstract storage mechanisms
- File I/O operations
- Cloud storage integration
- Database operations (if applicable)

**Storage Strategy Pattern**:
```python
class StorageBackend(ABC):
    @abstractmethod
    async def save(self, data: bytes, path: str) -> str:
        """Save data, return accessible URL/path"""

    @abstractmethod
    async def load(self, path: str) -> bytes:
        """Load data from storage"""

    @abstractmethod
    async def delete(self, path: str) -> bool:
        """Delete data from storage"""
```

**Storage Implementations**:
- **LocalFileStorage**: Development/testing
- **S3Storage**: Production cloud storage
- **MemoryStorage**: Testing/benchmarking

---

## Data Flow Examples

### Example 1: Generate Member CSV

```
1. HTTP Request
   POST /api/v1/members/generate
   {
     "record_count": 100,
     "output_format": "csv",
     "include_address": true
   }

2. API Layer (FastAPI)
   - Validate request (Pydantic)
   - Extract parameters
   - Call GenerationService

3. Service Layer
   - Create MemberGenerator(config)
   - Generate 100 member records
   - Validate each record
   - Pass to CSVAdapter

4. Format Layer
   - Convert List[MemberSchema] to CSV bytes
   - Add headers

5. Storage Layer
   - Save CSV to /tmp/members-{uuid}.csv
   - Return file path

6. API Layer
   - Return FileResponse with CSV
   - Set content-type: text/csv
   - Add download headers

7. HTTP Response
   Status: 200 OK
   Content-Type: text/csv
   Content-Disposition: attachment; filename="members.csv"
   [CSV data]
```

---

### Example 2: Generate EDI X12 837 Claim

```
1. HTTP Request
   POST /api/v1/edi/claims
   {
     "claim_count": 5,
     "segments": 2,
     "optional_fields": true
   }

2. API Layer
   - Validate EDI request
   - Call GenerationService

3. Service Layer
   - Create ClaimGenerator
   - Generate 5 claims with line items
   - Create MemberGenerator for subscribers
   - Combine data for EDI context

4. Format Layer (EDIAdapter)
   - Load EDI templates (ISA, GS, ST, etc.)
   - Populate templates with claim data
   - Build EDI segments
   - Add control numbers
   - Assemble complete EDI document

5. Validation Layer
   - Validate EDI structure
   - Check segment counts
   - Verify control numbers

6. Storage Layer
   - Save EDI to storage
   - Return path

7. API Response
   - Return EDI file or content
   - Content-Type: text/plain
```

---

## Design Patterns Applied

### 1. Strategy Pattern
- **Use Case**: Interchangeable generators
- **Implementation**: BaseGenerator with concrete implementations
- **Benefit**: Easy to add new data types

### 2. Adapter Pattern
- **Use Case**: Format conversions
- **Implementation**: FormatAdapter with format-specific adapters
- **Benefit**: Isolated format logic

### 3. Factory Pattern
- **Use Case**: Generator creation
- **Implementation**: GeneratorFactory
- **Benefit**: Centralized instantiation logic

### 4. Repository Pattern
- **Use Case**: Data persistence abstraction
- **Implementation**: StorageRepository
- **Benefit**: Storage backend flexibility

### 5. Dependency Injection
- **Use Case**: Service composition
- **Implementation**: FastAPI Depends()
- **Benefit**: Testability, loose coupling

---

## Configuration Architecture

### Environment-Based Configuration

```
.env (development)
├── Development settings
├── Local storage paths
└── Debug mode enabled

.env.staging
├── Staging settings
├── S3 storage
└── Debug mode disabled

.env.production
├── Production settings
├── S3 storage with CDN
├── Rate limiting strict
└── Monitoring enabled
```

### Configuration Hierarchy

```python
1. Environment Variables (.env file)
   ↓
2. Settings Class (config.py)
   ↓
3. Dependency Injection (FastAPI)
   ↓
4. Service/Component Configuration
```

---

## Scalability Considerations

### Horizontal Scalability
- Stateless API design
- No session storage in application
- File storage via S3 (shared across instances)
- Rate limiting via Redis (shared state)

### Vertical Scalability
- Async I/O for file operations
- Multiprocessing for CPU-intensive generation
- Configurable worker pool size
- Memory-efficient streaming for large datasets

### Performance Optimization
- Generator result caching
- Template preloading
- Connection pooling (S3, MongoDB)
- Lazy loading of large data files

---

## Security Architecture

### Defense in Depth

```
Layer 1: Network (Cloud provider security groups, WAF)
Layer 2: API Gateway (Rate limiting, CORS, auth)
Layer 3: Application (Input validation, sanitization)
Layer 4: Business Logic (Data validation, business rules)
Layer 5: Data Access (Parameterized queries, encryption)
Layer 6: Storage (Encrypted at rest, access controls)
```

### Security Measures

1. **Input Validation**: Pydantic schemas with strict validation
2. **Output Encoding**: Proper content-type headers, sanitization
3. **Rate Limiting**: Prevent abuse
4. **Authentication**: API key or OAuth (optional)
5. **Audit Logging**: Track all generation requests
6. **Dependency Scanning**: Automated vulnerability checks
7. **Secrets Management**: Environment variables, never in code

---

## Monitoring & Observability

### Logging Strategy

```python
# Structured logging with loguru
logger.info(
    "Member generation completed",
    extra={
        "request_id": request_id,
        "record_count": 100,
        "duration_ms": 1234,
        "format": "csv"
    }
)
```

### Metrics to Track

- Request count by endpoint
- Generation time by record count
- Error rate by type
- File storage usage
- API response times (p50, p95, p99)

### Health Checks

- `/health`: Basic liveness check
- `/health/ready`: Readiness check (dependencies available)
- `/health/live`: Kubernetes liveness probe

---

## Testing Strategy Architecture

### Test Pyramid

```
        ┌─────────────┐
       │   E2E Tests  │  (5%)
      └───────────────┘
     ┌─────────────────┐
    │ Integration Tests│ (25%)
   └───────────────────┘
  ┌─────────────────────┐
 │    Unit Tests        │ (70%)
└───────────────────────┘
```

### Test Organization

```
tests/
├── unit/              # Fast, isolated tests
│   ├── test_generators.py
│   ├── test_adapters.py
│   └── test_validators.py
├── integration/       # Multi-component tests
│   ├── test_api_endpoints.py
│   └── test_data_flow.py
├── e2e/              # Full workflow tests
│   └── test_generation_workflow.py
└── performance/      # Load/stress tests
    └── test_benchmarks.py
```

---

## Deployment Architecture

### Container Architecture

```
┌─────────────────────────────────────┐
│   Docker Container                  │
│  ┌────────────────────────────┐    │
│  │   FastAPI Application      │    │
│  │   (Uvicorn ASGI Server)    │    │
│  └────────────────────────────┘    │
│                                     │
│  Port: 8000                         │
│  Health: /health                    │
│  Environment: Production            │
└─────────────────────────────────────┘
```

### Deployment Options

**Option 1: AWS ECS/Fargate**
- Serverless containers
- Auto-scaling
- ALB for load balancing

**Option 2: Kubernetes**
- Deployment + Service
- HorizontalPodAutoscaler
- Ingress for routing

**Option 3: Cloud Run (GCP)**
- Fully managed
- Auto-scaling
- Pay-per-use

---

## Future Architecture Enhancements

### Phase 1 (Current)
- Monolithic FastAPI application
- File-based storage
- Synchronous generation

### Phase 2 (Future)
- Async job queue (Celery/RQ)
- Background workers for large generations
- Progress tracking
- Job scheduling

### Phase 3 (Advanced)
- Microservices architecture
- Separate services for each generator type
- Event-driven architecture
- Real-time data streaming

---

## Conclusion

This architecture provides:

1. **Clear Separation of Concerns**: Layered architecture with defined responsibilities
2. **Scalability**: Stateless design, horizontal scaling ready
3. **Maintainability**: Well-organized, testable, documented
4. **Extensibility**: Easy to add new generators, formats, storage backends
5. **Professional Standards**: Industry best practices throughout

The architecture balances simplicity for a portfolio project with professional-grade design patterns that demonstrate senior-level technical skills.
