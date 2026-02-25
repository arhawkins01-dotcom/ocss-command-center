"""Package initializer for the app module.

Expose common submodules so tests and imports using `from app import ...`
work reliably whether the package is imported as a package or when modules
are loaded in different import contexts.
"""
__all__ = [
    'roles',
    'report_utils',
    'database',
    'config',
    'auth',
    'helpers',
]

# Try to import submodules into the package namespace for convenience.
try:
    from . import roles, report_utils, database, auth, config, helpers  # type: ignore
except Exception:
    # Best-effort import; tests can import submodules directly if needed.
    pass

# Re-export common helper symbols for convenience (best-effort).
try:
    from .helpers import assign_caseloads_bulk, normalize_caseload_number, get_kpi_metrics  # type: ignore
    __all__.extend(['assign_caseloads_bulk', 'normalize_caseload_number', 'get_kpi_metrics'])
except Exception:
    pass
