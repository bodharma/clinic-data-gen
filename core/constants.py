"""Application-wide constants."""

# API metadata
API_TITLE = "Clinical Data Generator"
API_DESCRIPTION = "Generate synthetic clinical data for testing and development"
API_VERSION = "1.0.0"
API_V1_PREFIX = "/api/v1"

# File formats
SUPPORTED_FORMATS = ["csv", "json", "edi", "jsonlike"]
DEFAULT_FORMAT = "csv"

# Limits and defaults
MAX_MEMBERS_PER_REQUEST = 10000
DEFAULT_MEMBERS_COUNT = 1
DEFAULT_SEGMENTS_COUNT = 1

# Multiprocessing
DEFAULT_PROCESS_COUNT = 8

# Vaccine types
SUPPORTED_VACCINE_TYPES = [
    "Pfizer",
    "Moderna",
    "Janssen",
    "AstraZeneca",
    "Novavax",
]

# Test types
SUPPORTED_TEST_TYPES = [
    "rt_pcr_oral",
    "rt_pcr_oral_logix_smart",
    "rt_pcr_nasal",
    "covid_ag",
    "rt_pcr_saliva",
]

# Load types for RT data
RT_LOAD_TYPES = ["F", "I", "D"]  # Full, Incremental, Delta

# Media types
MEDIA_TYPE_CSV = "text/csv"
MEDIA_TYPE_JSON = "application/json"
MEDIA_TYPE_EDI = "text/plain"
MEDIA_TYPE_JSONLIKE = "application/octet-stream"

# Relationship types
SUBSCRIBER_RELATIONSHIPS = ["parent", "spouse", "child", "self"]

# Occupation types
OCCUPATION_TYPES = [
    "faculty_employee",
    "student",
    "employee_or_volunteer",
]

# Gender codes
GENDER_CODES = ["M", "F"]
GENDER_FULL = ["Male", "Female"]

# Ethnicities
ETHNICITY_TYPES = ["Asian", "Black", "White", "Hispanic"]

# Default S3 settings
DEFAULT_S3_BUCKET = "dev-de-phi-backup"
