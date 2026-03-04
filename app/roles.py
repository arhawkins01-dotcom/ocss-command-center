"""Centralized role definitions and helper utilities.

Keep role lists and mappings in one place so UI and logic stay consistent.
"""
from typing import List, Dict, Any

# Full expanded roles including sub-roles.
# Keep these strings stable: they are used in UI selectboxes, persistence, and tests.
EXPANDED_CORE_APP_ROLES: List[str] = [
    "Director",
    "Deputy Director",
    "Department Manager",
    "Program Officer",
    "Administrative Assistant",
    "Senior Administrative Officer",
    "Supervisor",
    "Team Lead",
    "Support Officer",
    "Client Information Specialist Team Lead",
    "Client Information Specialist",
    "Case Information Specialist Team Lead",
    "Case Information Specialist",
    "IT Administrator",
]

# Canonical core roles used for UI availability and tests
CORE_APP_ROLES: List[str] = [
    "Director", "Program Officer", "Supervisor", "Support Officer", "IT Administrator"
]

# Only these roles are available in the UI by default (can be swapped to expanded)
SUPPORTED_USER_ROLES = CORE_APP_ROLES

# Map sub-roles to main roles for dashboard logic
ROLE_VIEW_MAP = {
    "Deputy Director": "Director",
    "Senior Administrative Officer": "Supervisor",
    # Administrative Assistants mirror Program Officers (report intake + KPI scope)
    "Administrative Assistant": "Program Officer",
    # Team Leads process caseloads like Support Officers; map to Support Officer view
    "Team Lead": "Support Officer",
    # Administrative specialists reuse support-processing workflow components,
    # but retain their own role labels in the UI.
    "Client Information Specialist Team Lead": "Support Officer",
    "Client Information Specialist": "Support Officer",
    "Case Information Specialist Team Lead": "Support Officer",
    "Case Information Specialist": "Support Officer",
}

# Organizational role hierarchy and expected minimum counts for reporting validation.
# Keys are parent roles; values map child-role -> minimum recommended count.
ROLE_HIERARCHY = {
    "Director": {"Deputy Director": 2, "Senior Administrative Officer": 1},
    "Deputy Director": {"Department Manager": 4},
    "Department Manager": {"Program Officer": 1, "Administrative Assistant": 1, "Supervisor": 5},
    "Supervisor": {"Team Lead": 2, "Support Officer": 4},
}


# Recommended department + unit structure (soft validation only).
# These represent typical Cuyahoga-style staffing patterns and are used only
# for warnings in `validate_org_structure`.
DEPARTMENT_EXPECTATIONS: Dict[str, Dict[str, int]] = {
    # Applies to each department (recommended minima)
    "__default__": {
        "Department Manager": 1,
        "Program Officer": 1,
        "Administrative Assistant": 1,
        "Supervisor": 5,
        "units": 5,
    },
    # Establishment contains additional clerical units in many agencies.
    "Establishment": {
        "Department Manager": 1,
        "Program Officer": 1,
        "Administrative Assistant": 1,
        "Supervisor": 5,
        "units": 5,
        # unit-type hints used in `validate_org_structure` when present
        "genetic_testing_unit": 1,
        "interface_unit": 1,
    },
}

UNIT_EXPECTATIONS_BY_TYPE: Dict[str, Dict[str, int]] = {
    # Standard operational unit
    "standard": {
        "Supervisor": 1,
        "Team Lead": 2,
        "Support Officer": 4,
    },
    # Establishment clerical units
    "genetic_testing": {
        "Supervisor": 1,
        "Client Information Specialist Team Lead": 2,
        "Client Information Specialist": 4,
    },
    "interface": {
        "Supervisor": 1,
        "Case Information Specialist Team Lead": 2,
        "Case Information Specialist": 4,
    },
}


def _norm(value: Any) -> str:
    try:
        return str(value or '').strip()
    except Exception:
        return ''


def _user_unit(user: dict) -> str:
    # Backwards-compatibility: older data stored unit name in the `department` field.
    unit = _norm((user or {}).get('unit'))
    if unit:
        return unit
    return _norm((user or {}).get('department'))


def _unit_type_from_unit_record(unit_record: dict, unit_name: str = '') -> str:
    # Allow either explicit unit_type or inference by unit name.
    explicit = _norm((unit_record or {}).get('unit_type')).lower()
    if explicit:
        if 'genetic' in explicit:
            return 'genetic_testing'
        if 'interface' in explicit:
            return 'interface'
        return 'standard'

    name = _norm(unit_name).lower()
    if 'genetic' in name:
        return 'genetic_testing'
    if 'interface' in name:
        return 'interface'
    return 'standard'


def get_children_roles(role: str) -> dict:
    """Return child-role mapping for a given parent role (may be empty)."""
    return ROLE_HIERARCHY.get(role, {})


def get_parent_roles() -> dict:
    """Return a mapping of child role -> parent role(s)."""
    parents: dict = {}
    for parent, children in ROLE_HIERARCHY.items():
        for child in children:
            parents.setdefault(child, []).append(parent)
    return parents


def validate_org_structure(units: dict, users: list) -> list:
    """Validate a simple org structure and return list of human-readable issues.

    - `units` is expected to be the `st.session_state['units']` structure used by the app.
    - `users` is expected to be a list of user dicts (name/role/department).

    This function performs lightweight checks against `ROLE_HIERARCHY` recommended minima.
    It does not enforce policy — it simply discovers potential gaps and returns messages.
    """
    issues: list = []
    try:
        users_list = users or []
        units_map = units or {}

        def _effective_role(u: dict) -> str:
            r = _norm((u or {}).get('role'))
            if r == 'Director':
                sub = _norm((u or {}).get('unit_role'))
                if sub in {'Director', 'Deputy Director', 'Department Manager', 'Senior Administrative Officer'}:
                    return sub
            return r

        # Count roles globally.
        role_counts: dict = {}
        for u in users_list:
            r = _effective_role(u)
            if not r:
                continue
            role_counts[r] = role_counts.get(r, 0) + 1

        # Department-level recommended structure.
        dept_role_counts: Dict[str, Dict[str, int]] = {}
        for u in users_list:
            dept = _norm((u or {}).get('department'))
            if not dept:
                continue
            dept_role_counts.setdefault(dept, {})
            role = _effective_role(u)
            if role:
                dept_role_counts[dept][role] = dept_role_counts[dept].get(role, 0) + 1

        # Map units to departments when present.
        units_by_department: Dict[str, List[str]] = {}
        for unit_name, unit in units_map.items():
            dept = _norm((unit or {}).get('department'))
            if dept:
                units_by_department.setdefault(dept, []).append(unit_name)

        # Unit checks: supervisor + staffing. Prefer user membership (unit field) when available,
        # but fall back to legacy unit dict lists.
        users_by_unit: Dict[str, List[dict]] = {}
        for u in users_list:
            unit_name = _user_unit(u)
            if unit_name:
                users_by_unit.setdefault(unit_name, []).append(u)

        for unit_name, unit in units_map.items():
            unit_kind = _unit_type_from_unit_record(unit, unit_name)
            expectations = UNIT_EXPECTATIONS_BY_TYPE.get(unit_kind, UNIT_EXPECTATIONS_BY_TYPE['standard'])

            # Supervisor presence (either explicit in units map or via users list)
            sup = _norm((unit or {}).get('supervisor'))
            if not sup:
                has_sup_user = any(_norm(u.get('role')) == 'Supervisor' for u in users_by_unit.get(unit_name, []))
                if not has_sup_user:
                    issues.append(f"Unit '{unit_name}' has no supervisor assigned.")

            # Role counts inside unit
            unit_user_roles: Dict[str, int] = {}
            for u in users_by_unit.get(unit_name, []):
                r = _effective_role(u)
                if r:
                    unit_user_roles[r] = unit_user_roles.get(r, 0) + 1

            # Legacy lists (team_leads/support_officers) still count if present.
            legacy_team_leads = list((unit or {}).get('team_leads') or [])
            legacy_support = list((unit or {}).get('support_officers') or [])
            if legacy_team_leads:
                unit_user_roles['Team Lead'] = max(unit_user_roles.get('Team Lead', 0), len(set(legacy_team_leads)))
            if legacy_support:
                unit_user_roles['Support Officer'] = max(unit_user_roles.get('Support Officer', 0), len(set(legacy_support)))

            for role_name, min_count in expectations.items():
                found = int(unit_user_roles.get(role_name, 0) or 0)
                if role_name == 'Supervisor':
                    continue  # handled above
                if found < min_count:
                    issues.append(
                        f"Unit '{unit_name}' ({unit_kind}) has fewer than recommended {role_name}s ({found}; recommended {min_count})."
                    )

        # Department expectations: only check departments that exist in users or units.
        departments_seen = set(dept_role_counts.keys()) | set(units_by_department.keys())
        for dept in sorted(d for d in departments_seen if d):
            expected = dict(DEPARTMENT_EXPECTATIONS.get('__default__', {}))
            expected.update(DEPARTMENT_EXPECTATIONS.get(dept, {}))

            # Unit count under department (if known)
            if 'units' in expected:
                unit_count = len(units_by_department.get(dept, []))
                if unit_count and unit_count < int(expected['units']):
                    issues.append(
                        f"Department '{dept}' has fewer than recommended units ({unit_count}; recommended {expected['units']})."
                    )

            for role_name, min_count in expected.items():
                if role_name in {'units', 'genetic_testing_unit', 'interface_unit'}:
                    continue
                found = int((dept_role_counts.get(dept, {}) or {}).get(role_name, 0) or 0)
                if found < int(min_count):
                    issues.append(
                        f"Department '{dept}' has fewer than recommended {role_name}s ({found}; recommended {min_count})."
                    )

            # Establishment clerical units (only if unit types are present)
            if dept == 'Establishment':
                dept_units = units_by_department.get(dept, [])
                if dept_units:
                    gt_units = 0
                    iface_units = 0
                    for u_name in dept_units:
                        u_kind = _unit_type_from_unit_record(units_map.get(u_name, {}), u_name)
                        if u_kind == 'genetic_testing':
                            gt_units += 1
                        if u_kind == 'interface':
                            iface_units += 1
                    if gt_units < int(expected.get('genetic_testing_unit', 0) or 0):
                        issues.append("Establishment department: recommended at least 1 Genetic Testing unit.")
                    if iface_units < int(expected.get('interface_unit', 0) or 0):
                        issues.append("Establishment department: recommended at least 1 Interface unit.")

        # High-level recommendations (global minima) based on ROLE_HIERARCHY.
        for parent, children in ROLE_HIERARCHY.items():
            for child_role, min_count in children.items():
                count = role_counts.get(child_role, 0)
                if count < min_count:
                    issues.append(
                        f"Recommended: at least {min_count} {child_role}(s) under {parent} (found {count})."
                    )
    except Exception as ex:  # pragma: no cover - defensive
        issues.append(f"Org validation failed: {ex}")

    return issues


# Role capabilities: map canonical view-roles to capability flags.
# Use `map_to_view_role()` before checking capabilities to ensure sub-roles inherit.
ROLE_CAPABILITIES = {
    'Director': {'export': True, 'manage_users': True, 'view_kpi': True, 'reassign': True, 'import_reports': True},
    'Program Officer': {'export': True, 'manage_users': True, 'view_kpi': True, 'reassign': True, 'import_reports': True},
    'Supervisor': {'export': True, 'manage_users': True, 'view_kpi': True, 'reassign': True, 'import_reports': True},
    'Support Officer': {'export': False, 'manage_users': False, 'view_kpi': False, 'reassign': False, 'process_caseload': True},
    'IT Administrator': {'export': True, 'manage_users': True, 'view_kpi': False, 'reassign': False, 'view_it_logs': True, 'import_reports': True},
    # Non-caseload administrative support
    'Administrative Assistant': {'export': False, 'manage_users': False, 'view_kpi': False, 'reassign': False, 'process_caseload': False, 'import_reports': True},
}

# Department Manager: department-scoped leadership capabilities
ROLE_CAPABILITIES['Department Manager'] = {'export': True, 'manage_users': True, 'view_kpi': True, 'reassign': True, 'import_reports': True}

# Knowledge base edit capability — restricted to Program Officer and IT Administrator by default
ROLE_CAPABILITIES['Program Officer']['edit_kb'] = True
ROLE_CAPABILITIES['IT Administrator']['edit_kb'] = True

# Ensure leadership roles have IT-like user and caseload management capabilities
for _role in ("Director", "Deputy Director", "Department Manager", "Program Officer", "Senior Administrative Officer", "Supervisor"):
    ROLE_CAPABILITIES.setdefault(_role, {})
    # Directors should retain a leadership-only view (no direct caseload processing).
    if _role == 'Director':
        ROLE_CAPABILITIES[_role].update({
            'manage_users': True,
            'view_it_logs': True,
        })
    else:
        ROLE_CAPABILITIES[_role].update({
            'manage_users': True,
            'process_caseload': True,
            'view_it_logs': True,
            'import_reports': True,
        })


def role_has(role: str, capability: str) -> bool:
    """Return True if `role` (or its mapped view-role) has `capability`.

    This normalizes the role via `map_to_view_role()` so expanded roles inherit
    the capabilities of their canonical view role.
    """
    if not role or not capability:
        return False
    view_role = map_to_view_role(role)
    caps = ROLE_CAPABILITIES.get(view_role, {})
    return bool(caps.get(capability, False))


def map_to_view_role(role: str) -> str:
    """Return the canonical view-role for a possibly expanded sub-role."""
    if not role:
        return role
    return ROLE_VIEW_MAP.get(role, role)


def get_supported_roles(expanded: bool = False):
    """Return either the canonical or expanded role list."""
    return EXPANDED_CORE_APP_ROLES if expanded else CORE_APP_ROLES


def role_is_leadership(role: str) -> bool:
    return role in {"Director", "Deputy Director", "Senior Administrative Officer"}
