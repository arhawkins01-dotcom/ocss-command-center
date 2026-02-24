"""Centralized role definitions and helper utilities.

Keep role lists and mappings in one place so UI and logic stay consistent.
"""
from typing import List

# Full expanded roles including sub-roles
EXPANDED_CORE_APP_ROLES: List[str] = [
    "Director", "Deputy Director", "Department Manager", "Program Officer", "Senior Administrative Officer",
    "Supervisor", "Team Lead", "Support Officer", "IT Administrator"
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
    # Team Leads process caseloads like Support Officers; map to Support Officer view
    "Team Lead": "Support Officer"
}

# Organizational role hierarchy and expected minimum counts for reporting validation.
# Keys are parent roles; values map child-role -> minimum recommended count.
ROLE_HIERARCHY = {
    "Director": {"Deputy Director": 2, "Senior Administrative Officer": 2},
    "Deputy Director": {"Department Manager": 4},
    "Department Manager": {"Supervisor": 5},
    "Supervisor": {"Team Lead": 2, "Support Officer": 5},
}


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
        # Count roles at top levels: Director, Deputy Director, Department Manager, Supervisor
        role_counts: dict = {}
        for u in (users or []):
            r = str((u or {}).get('role', '')).strip()
            if not r:
                continue
            role_counts[r] = role_counts.get(r, 0) + 1

        # Units mapping: supervisors own units; count team leads/support officers per unit
        for unit_name, unit in (units or {}).items():
            # Supervisor
            sup = unit.get('supervisor')
            if not sup:
                issues.append(f"Unit '{unit_name}' has no supervisor assigned.")
            # Team leads and support officers
            tl = unit.get('team_leads', []) or []
            so = unit.get('support_officers', []) or []
            if len(tl) < ROLE_HIERARCHY.get('Supervisor', {}).get('Team Lead', 2):
                issues.append(f"Unit '{unit_name}' has fewer than recommended Team Leads ({len(tl)}).")
            if len(so) < ROLE_HIERARCHY.get('Supervisor', {}).get('Support Officer', 5):
                issues.append(f"Unit '{unit_name}' has fewer than recommended Support Officers ({len(so)}).")

        # High-level recommendations
        for parent, children in ROLE_HIERARCHY.items():
            for child_role, min_count in children.items():
                count = role_counts.get(child_role, 0)
                if count < min_count:
                    issues.append(f"Recommended: at least {min_count} {child_role}(s) under {parent} (found {count}).")
    except Exception as ex:  # pragma: no cover - defensive
        issues.append(f"Org validation failed: {ex}")

    return issues


# Role capabilities: map canonical view-roles to capability flags.
# Use `map_to_view_role()` before checking capabilities to ensure sub-roles inherit.
ROLE_CAPABILITIES = {
    'Director': {'export': True, 'manage_users': True, 'view_kpi': True, 'reassign': True},
    'Program Officer': {'export': True, 'manage_users': True, 'view_kpi': True, 'reassign': True},
    'Supervisor': {'export': True, 'manage_users': True, 'view_kpi': True, 'reassign': True},
    'Support Officer': {'export': False, 'manage_users': False, 'view_kpi': False, 'reassign': False, 'process_caseload': True},
    'IT Administrator': {'export': True, 'manage_users': True, 'view_kpi': False, 'reassign': False, 'view_it_logs': True},
}

# Department Manager: department-scoped leadership capabilities
ROLE_CAPABILITIES['Department Manager'] = {'export': True, 'manage_users': True, 'view_kpi': True, 'reassign': True}

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
