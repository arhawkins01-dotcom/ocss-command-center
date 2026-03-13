"""
Configuration settings for OCSS Command Center Application
Centralized configuration management for production deployment
"""

import os
from pathlib import Path
from typing import Dict, Any

# Application Settings
APP_NAME = "OCSS Establishment Command Center"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Internal Director Command Center for OCSS Establishment Reporting"

# Server Settings
DEFAULT_PORT = 8501
DEFAULT_HOST = "localhost"

# File Paths (Production deployment on Windows Server)
# These paths should be configured for the production environment
BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTION_BASE_PATH = Path("S:/OCSS/CommandCenter")
PRODUCTION_APP_PATH = PRODUCTION_BASE_PATH / "App"
PRODUCTION_DATA_PATH = PRODUCTION_BASE_PATH / "Data"
PRODUCTION_LOGS_PATH = PRODUCTION_BASE_PATH / "Logs"
PRODUCTION_EXPORTS_PATH = PRODUCTION_BASE_PATH / "Exports"

# Local Development Paths
DEV_DATA_PATH = BASE_DIR.parent / "data"
DEV_LOGS_PATH = BASE_DIR.parent / "logs"
DEV_EXPORTS_PATH = BASE_DIR.parent / "exports"

# Environment Detection
def is_production() -> bool:
    """Check if running in production environment"""
    return os.getenv("OCSS_ENV", "development") == "production"

def get_data_path() -> Path:
    """Get the appropriate data path based on environment"""
    if is_production():
        return PRODUCTION_DATA_PATH
    return DEV_DATA_PATH

def get_logs_path() -> Path:
    """Get the appropriate logs path based on environment"""
    if is_production():
        return PRODUCTION_LOGS_PATH
    return DEV_LOGS_PATH

def get_exports_path() -> Path:
    """Get the appropriate exports path based on environment"""
    if is_production():
        return PRODUCTION_EXPORTS_PATH
    return DEV_EXPORTS_PATH

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    paths = [get_data_path(), get_logs_path(), get_exports_path()]
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)

# File Upload Settings
ALLOWED_UPLOAD_EXTENSIONS = ['.xlsx', '.xls', '.csv']
MAX_UPLOAD_SIZE_MB = 50
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# Report Settings
SUPPORTED_REPORT_TYPES = [
    'Establishment Report',
    'Monthly Summary',
    'CQI Alignment',
    'SAVES Compliance',
    'Quarterly Review'
]

# Organizational Units Configuration
DEFAULT_UNITS = {
    'OCSS North': {
        'supervisor': 'Alex Martinez',
        'team_leads': ['Sarah Johnson'],
        'support_officers': ['Michael Chen', 'Jessica Brown'],
        'assignments': {
            'Sarah Johnson': ['181000'],
            'Michael Chen': ['181001'],
            'Jessica Brown': ['181002']
        }
    },
    'OCSS South': {
        'supervisor': 'Priya Singh',
        'team_leads': ['David Martinez'],
        'support_officers': ['Amanda Wilson'],
        'assignments': {
            'David Martinez': ['181001'],
            'Amanda Wilson': ['181000']
        }
    }
}

# Caseload Configuration
DEFAULT_CASELOADS = {
    '181000': 'Downtown Elementary',
    '181001': 'Midtown Middle School',
    '181002': 'Uptown High School'
}

# Role Configuration
AVAILABLE_ROLES = [
    "Director",
    "Deputy Director",
    "Senior Admin Officer",
    "Department Manager",
    "Team Lead",
    "Program Officer",
    "Supervisor",
    "Support Officer",
    "IT Administrator"
]

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Audit Log Settings
AUDIT_LOG_FILE = "audit_log.jsonl"
ENABLE_AUDIT_LOGGING = True

# Session Settings
SESSION_TIMEOUT_MINUTES = 30
ENABLE_SESSION_STATE_PERSISTENCE = True

# UI Settings
THEME_CONFIG = {
    'primaryColor': '#1f77b4',
    'backgroundColor': '#ffffff',
    'secondaryBackgroundColor': '#f0f2f6',
    'textColor': '#31333F',
    'font': 'sans serif'
}

# Data Validation Rules
VALIDATION_RULES = {
    'required_columns': {
        'establishment_report': ['Case_ID', 'Worker', 'Status', 'Date_Filed'],
        'monthly_summary': ['Month', 'Total_Cases', 'Completed', 'In_Progress']
    },
    'data_types': {
        'Case_ID': 'string',
        'Date_Filed': 'datetime',
        'Total_Cases': 'integer'
    }
}

# Export Settings
EXPORT_FORMATS = ['xlsx', 'csv', 'json']
DEFAULT_EXPORT_FORMAT = 'xlsx'

# KPI Thresholds
KPI_THRESHOLDS = {
    'completion_rate': {
        'excellent': 95.0,
        'good': 85.0,
        'needs_improvement': 75.0
    },
    'on_time_submission': {
        'excellent': 95.0,
        'good': 90.0,
        'needs_improvement': 80.0
    },
    'data_quality': {
        'excellent': 98.0,
        'good': 95.0,
        'needs_improvement': 90.0
    }
}

# System Status Configuration
SYSTEM_COMPONENTS = [
    {'name': 'Application Server', 'type': 'service'},
    {'name': 'File System Access', 'type': 'storage'},
    {'name': 'Report Processing', 'type': 'service'},
    {'name': 'Audit Logging', 'type': 'service'}
]

def get_config() -> Dict[str, Any]:
    """
    Get complete configuration as a dictionary
    
    Returns:
        Dictionary containing all configuration settings
    """
    return {
        'app': {
            'name': APP_NAME,
            'version': APP_VERSION,
            'description': APP_DESCRIPTION
        },
        'server': {
            'host': DEFAULT_HOST,
            'port': DEFAULT_PORT
        },
        'paths': {
            'data': str(get_data_path()),
            'logs': str(get_logs_path()),
            'exports': str(get_exports_path())
        },
        'upload': {
            'allowed_extensions': ALLOWED_UPLOAD_EXTENSIONS,
            'max_size_mb': MAX_UPLOAD_SIZE_MB
        },
        'roles': AVAILABLE_ROLES,
        'units': DEFAULT_UNITS,
        'caseloads': DEFAULT_CASELOADS
    }

if __name__ == "__main__":
    # Test configuration
    ensure_directories()
    config = get_config()
    print("OCSS Command Center Configuration")
    print("=" * 50)
    for key, value in config.items():
        print(f"{key}: {value}")
