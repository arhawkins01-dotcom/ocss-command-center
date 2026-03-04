# OCSS Department Structure (agency-level departments -> units).
# This is used as a default template for deployments that want a county-style
# org structure. The application will still function if deployments override
# this via persisted session state.
OCSS_DEPARTMENTS = {
    'Establishment': {
        'description': 'Paternity establishment, new case intake, new child support orders',
        'units': [
            # Operational units (county template)
            'Establishment Unit 15',
            'Establishment Unit 16',
            'Establishment Unit 17',
            'New Order Unit 22',
            # Clerical units
            'Front Desk Unit 8',
            'Genetic Testing Unit 22',
            'Interface Unit 23',
        ]
    },
    'Financial Operations': {
        'description': 'Payment processing, financial reconciliation, order entry',
        'units': ['Financial Operations Unit 1', 'Financial Operations Unit 2', 'Financial Operations Unit 3', 'Financial Operations Unit 4', 'Financial Operations Unit 5']
    },
    'Case Maintenance': {
        'description': 'Ongoing case maintenance and updates',
        'units': [
            'Case Maintenance A-E',
            'Case Maintenance F-K',
            'Case Maintenance L-R',
            'Case Maintenance S-Z',
            'CM Transition',
            'Zero Support',
            'Case Maintenance Arrears',
            'Non IV-D',
        ]
    },
    'Compliance': {
        'description': 'Compliance/enforcement and non-paying cases',
        'units': [
            'Compliance Unit 18203',
            'Compliance Unit 18204',
            'Compliance Unit 18205',
            'Compliance Unit 18206',
            'Compliance Unit 18207',
            'Compliance Unit 18208 (UIFSA)',
            'Compliance Management Caseloads',
        ]
    },
    'Continuous Quality Improvement (CQI)': {
        'description': 'Continuous Quality Improvement and quality review workflows',
        'units': ['CQI Unit 1', 'CQI Unit 2', 'CQI Unit 3', 'CQI Unit 4', 'CQI Unit 5']
    },
}
"""
Configuration settings for OCSS Command Center Application
Centralized configuration management for production deployment
"""

import os
from pathlib import Path
from typing import Dict, Any

# Application Settings
APP_NAME = "OCSS Agency Command Center"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Internal Director Command Center for OCSS Agency Reporting"

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
    'Quarterly Review',
    # Enforcement / case-banked workflows (Case Maintenance + Compliance)
    'Monthly Emancipation',
    'Ohio Deceased',
    'NCP w DOD in SETS',
    'ODRC',
    'Spousal Support Suborder End Date',
    'Locate/No Worker Activity/No Payment',
    'Deceased CP Clean Up',
    'Case Closure/Child Past Emancipation',
    'End of Fiscal Year Project - TBD',
]

# Organizational Units Configuration
# Default units are generated from OCSS_DEPARTMENTS to ensure every department
# has a usable skeleton. Deployments can override via session state persistence.
DEFAULT_UNITS = {}
for _dept, _cfg in (OCSS_DEPARTMENTS or {}).items():
    for _unit_name in (_cfg.get('units') or []):
        unit_type = 'standard'
        lowered = str(_unit_name).lower()
        if 'genetic' in lowered:
            unit_type = 'genetic_testing'
        elif 'interface' in lowered or 'front desk' in lowered:
            unit_type = 'interface'

        DEFAULT_UNITS[str(_unit_name)] = {
            'department': str(_dept),
            'unit_type': unit_type,
            'supervisor': '',
            'team_leads': [],
            'support_officers': [],
            # Optional: list of caseload series prefixes owned by this unit (e.g., ['1811'] for 181100 series)
            'caseload_series_prefixes': [],
            'assignments': {},
        }

# Default caseload-series routing (can be edited in-app).
# We use exact 6-digit caseload numbers as prefixes so routing is deterministic.
_DEFAULT_CASELOAD_SERIES_PREFIXES = {
    # Case Maintenance Division (Dillinger)
    'Case Maintenance A-E': ['182101'],
    'Case Maintenance F-K': ['182102'],
    'CM Transition': ['182150'],
    'Case Maintenance L-R': ['182103'],
    'Zero Support': ['182120'],
    'Case Maintenance S-Z': ['182104'],
    'Case Maintenance Arrears': ['182110'],
    'Non IV-D': ['182140'],

    # Compliance Division (Meznarich)
    'Compliance Unit 18203': [
        '182301', '182302', '182303', '182304', '182305', '182306', '182307', '182308', '182309', '182310', '182311',
        '182320', '182330', '182340', '182350', '182360',
    ],
    'Compliance Unit 18204': [
        '182401', '182402', '182404', '182405', '182406', '182407', '182408', '182409', '182410', '182411',
        '182430', '182440', '182450', '182460',
    ],
    'Compliance Unit 18205': [
        '182501', '182502', '182504', '182505', '182506', '182507', '182508', '182509', '182510', '182511', '182512',
        '182530', '182540', '182550', '182560',
    ],
    'Compliance Unit 18206': [
        '182220', '182221',
        '182601', '182602', '182604', '182605', '182606', '182607', '182608', '182609', '182610', '182611',
        '182630', '182640', '182650', '182660',
    ],
    'Compliance Unit 18207': [
        '182701', '182702', '182704', '182705', '182706', '182707', '182708', '182709', '182710',
        '182730', '182740', '182750', '182760',
    ],
    'Compliance Unit 18208 (UIFSA)': [
        '182801', '182802', '182803', '182804', '182806', '182807', '182808', '182810',
        '182811', '182812', '182813', '182814', '182815',
        '182840', '182860',
    ],
    'Compliance Management Caseloads': ['182197', '182198', '182199', '189999'],
}
for _unit_name, _prefixes in _DEFAULT_CASELOAD_SERIES_PREFIXES.items():
    if _unit_name in DEFAULT_UNITS:
        DEFAULT_UNITS[_unit_name]['caseload_series_prefixes'] = list(_prefixes)

# Establishment unit rosters (caseload assignments) where caseloads are known.
_DEFAULT_UNIT_ROSTERS = {
    'Establishment Unit 15': {
        'supervisor': 'Stacy Slick-Williams',
        'team_leads': ['Anna K. Engler', 'Akilah Rasheed-Tinsley'],
        'support_officers': [
            'Anna K. Engler',
            'Joy G. Ogunmola',
            'Akilah Rasheed-Tinsley',
            'Brittany Baran',
            'Jeffrey A. Swanson',
            'Cyrita J. Johnson',
        ],
        'caseload_numbers': ['181100', '181101', '181103', '181105', '181106', '181107', '181109', '181110', '181112'],
        'assignments': {
            'Stacy Slick-Williams': ['181100'],
            'Anna K. Engler': ['181101'],
            'Joy G. Ogunmola': ['181103'],
            'Akilah Rasheed-Tinsley': ['181105'],
            'Brittany Baran': ['181107'],
            'Jeffrey A. Swanson': ['181109'],
            'Cyrita J. Johnson': ['181112'],
        },
    },
    'Establishment Unit 16': {
        'supervisor': 'Robin L. Patterson',
        'team_leads': ['April Jeter', 'Awilda Martinez'],
        'support_officers': [
            'April Jeter',
            'Karen McRowe',
            'Tamika Joseph-McManus',
            'Awilda Martinez',
            'Richard Fletcher',
            'Natalie Spatafore',
        ],
        'caseload_numbers': ['181200', '181201', '181202', '181204', '181205', '181208', '181209', '181213', '181214'],
        'assignments': {
            'Robin L. Patterson': ['181200'],
            'April Jeter': ['181204'],
            'Karen McRowe': ['181205'],
            'Tamika Joseph-McManus': ['181208'],
            'Awilda Martinez': ['181209'],
            'Richard Fletcher': ['181213'],
            'Natalie Spatafore': ['181214'],
        },
    },
    'Establishment Unit 17': {
        'supervisor': 'Jeanne Sua',
        'team_leads': ['Kristine DeSouza', 'L. Arlene Gonzalez'],
        'support_officers': [
            'Kristine DeSouza',
            'Patricia Bennett',
            'Cecelia Durham',
            'Mayra Berrios',
            'L. Arlene Gonzalez',
            'Hannah Maynard',
        ],
        'caseload_numbers': ['181300', '181301', '181302', '181303', '181304', '181305', '181306', '181307', '181308'],
        'assignments': {
            'Jeanne Sua': ['181300'],
            'Kristine DeSouza': ['181301'],
            'Patricia Bennett': ['181303'],
            'Cecelia Durham': ['181304'],
            'Mayra Berrios': ['181306'],
            'L. Arlene Gonzalez': ['181307'],
            'Hannah Maynard': ['181308'],
        },
    },
    'New Order Unit 22': {
        'supervisor': 'James Brown',
        'team_leads': ['Nadia Ahmetovic'],
        'support_officers': [
            'Nadia Ahmetovic',
            'Latonya Grays-Martin',
            'Michelle Fogler',
            'Tracy Wilson',
            'William Wedmedyk',
        ],
        'caseload_numbers': ['182001', '182002', '182003', '182004', '182005'],
        'assignments': {
            'Nadia Ahmetovic': ['182001'],
            'Latonya Grays-Martin': ['182002'],
            'Michelle Fogler': ['182003'],
            'Tracy Wilson': ['182004'],
            'William Wedmedyk': ['182005'],
        },
    },
    'Front Desk Unit 8': {
        'supervisor': 'James Brown',
        'team_leads': ['Reginald Davis'],
        'support_officers': [
            'Pamela Alexander',
            'Danielle Deberry',
            'Reginald Davis',
            'Aleesha Anderson',
        ],
    },
    'Genetic Testing Unit 22': {
        'supervisor': 'Silas Ungar',
        'team_leads': ['Laurie Tomlinson'],
        'support_officers': [
            'Laurie Tomlinson',
            'Aleia Lawson',
            'Natasha Johnson',
            'Tiffany Johnson',
        ],
    },
    'Interface Unit 23': {
        'supervisor': 'Giselle Torres',
        'team_leads': ['Quiana Harville', 'Enid Williams'],
        'support_officers': [
            'Sierra Carter',
            'Chandara Dodson',
            'Quiana Harville',
            'Avonna Handsome',
            'Taylor Andrews',
            'Enid Williams',
        ],
    },

    # Case Maintenance Division (Dillinger) supervisors
    'Case Maintenance A-E': {'supervisor': 'Monnie Brawley'},
    'Case Maintenance F-K': {'supervisor': 'Monnie Brawley'},
    'CM Transition': {'supervisor': 'Monnie Brawley'},
    'Case Maintenance L-R': {'supervisor': 'Tameika Hill-White'},
    'Zero Support': {'supervisor': 'Tameika Hill-White'},
    'Case Maintenance S-Z': {'supervisor': 'Ligeia Tyree'},
    'Case Maintenance Arrears': {'supervisor': 'Ligeia Tyree'},
    'Non IV-D': {'supervisor': 'Ligeia Tyree'},

    # Compliance Division (Meznarich) supervisors
    'Compliance Unit 18203': {'supervisor': 'Ezra Miklowski'},
    'Compliance Unit 18204': {'supervisor': 'Karen Beeble'},
    'Compliance Unit 18205': {'supervisor': 'Christie Cunningham'},
    'Compliance Unit 18206': {'supervisor': 'Kimberly Mell'},
    'Compliance Unit 18207': {'supervisor': 'Tiffany Mitchell'},
    'Compliance Unit 18208 (UIFSA)': {'supervisor': 'Alison Donze'},
    'Compliance Management Caseloads': {'supervisor': 'Meznarich'},
}

for _unit_name, _preset in _DEFAULT_UNIT_ROSTERS.items():
    if _unit_name not in DEFAULT_UNITS:
        continue

    # Ensure required keys exist.
    DEFAULT_UNITS[_unit_name].setdefault('assignments', {})
    DEFAULT_UNITS[_unit_name].setdefault('team_leads', [])
    DEFAULT_UNITS[_unit_name].setdefault('support_officers', [])
    DEFAULT_UNITS[_unit_name].setdefault('caseload_numbers', [])

    if 'supervisor' in _preset and isinstance(_preset['supervisor'], str):
        DEFAULT_UNITS[_unit_name]['supervisor'] = _preset['supervisor']

    if 'assignments' in _preset and isinstance(_preset['assignments'], dict):
        DEFAULT_UNITS[_unit_name]['assignments'].update(_preset['assignments'])
        # If workers are listed in assignments, treat non-supervisor workers as support officers.
        _preset_supervisor = str(_preset.get('supervisor', '')).strip()
        DEFAULT_UNITS[_unit_name]['support_officers'] = list(
            dict.fromkeys(
                list(DEFAULT_UNITS[_unit_name]['support_officers'])
                + [
                    str(worker).strip()
                    for worker in _preset['assignments'].keys()
                    if str(worker).strip() and str(worker).strip() != _preset_supervisor
                ]
            )
        )

    if 'team_leads' in _preset and isinstance(_preset['team_leads'], list):
        DEFAULT_UNITS[_unit_name]['team_leads'] = list(
            dict.fromkeys([str(n).strip() for n in _preset['team_leads'] if str(n).strip() and str(n).strip().upper() != 'VACANT'])
        )

    if 'support_officers' in _preset and isinstance(_preset['support_officers'], list):
        DEFAULT_UNITS[_unit_name]['support_officers'] = list(
            dict.fromkeys(
                list(DEFAULT_UNITS[_unit_name]['support_officers'])
                + [
                    str(n).strip()
                    for n in _preset['support_officers']
                    if str(n).strip() and str(n).strip().upper() != 'VACANT'
                ]
            )
        )

    if 'caseload_numbers' in _preset and isinstance(_preset['caseload_numbers'], list):
        DEFAULT_UNITS[_unit_name]['caseload_numbers'] = list(
            dict.fromkeys([str(c).strip() for c in _preset['caseload_numbers'] if str(c).strip()])
        )

# Caseload Configuration
DEFAULT_CASELOADS = {
    '181000': 'Downtown Elementary',
    '181001': 'Midtown Middle School',
    '181002': 'Uptown High School'
}

# Role Configuration
AVAILABLE_ROLES = [
    "Director",
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

# Download / export safety: set to 'false' in production env to disable downloads
ALLOW_DOWNLOADS = os.getenv('ALLOW_DOWNLOADS', 'true').lower() == 'true'

# Import sanitization: when true, attempt to redact obvious PII columns during ingestion
SANITIZE_PII_ON_IMPORT = os.getenv('SANITIZE_PII_ON_IMPORT', 'false').lower() == 'true'

# Maximum number of rows to read from uploaded files to avoid very large imports
MAX_IMPORT_ROWS = int(os.getenv('MAX_IMPORT_ROWS', str(200000)))

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
