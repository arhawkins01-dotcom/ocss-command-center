# Make config a Python package
from .settings import (
    APP_NAME,
    APP_VERSION,
    get_config,
    ensure_directories,
    get_data_path,
    get_logs_path,
    get_exports_path,
    is_production
)

__all__ = [
    'APP_NAME',
    'APP_VERSION',
    'get_config',
    'ensure_directories',
    'get_data_path',
    'get_logs_path',
    'get_exports_path',
    'is_production'
]
