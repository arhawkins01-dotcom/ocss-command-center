from app import roles
from app import roles


def test_map_to_view_role_matches_role_view_map():
    # Each expanded role should map to the same canonical role as ROLE_VIEW_MAP or itself
    for role in roles.EXPANDED_CORE_APP_ROLES:
        mapped = roles.map_to_view_role(role)
        expected = roles.ROLE_VIEW_MAP.get(role, role)
        assert mapped == expected, f"Role {role} maps to {mapped}, expected {expected}"


def test_validate_org_structure_returns_list():
    # Minimal fake data to ensure validation runs and returns a list of issues (possibly empty)
    fake_units = {
        'Unit A': {
            'supervisor': '',
            'team_leads': [],
            'support_officers': [],
            'assignments': {}
        }
    }
    fake_users = [
        {'name': 'Alice', 'role': 'Director', 'department': 'Executive'},
        {'name': 'Bob', 'role': 'Deputy Director', 'department': 'Executive'}
    ]
    issues = roles.validate_org_structure(fake_units, fake_users)
    assert isinstance(issues, list)


def test_validate_org_structure_reports_missing_supervisor():
    units = {
        'Unit A': {'supervisor': '', 'team_leads': [], 'support_officers': []}
    }
    users = []
    issues = roles.validate_org_structure(units, users)
    assert any("has no supervisor assigned" in msg for msg in issues)