from app import roles


def test_role_has_support_officer_processing():
    # Team Lead should map to Support Officer and have process_caseload capability
    assert roles.role_has('Team Lead', 'process_caseload') is True
    # Director should not have process_caseload
    assert roles.role_has('Director', 'process_caseload') is False


def test_role_has_view_kpi():
    assert roles.role_has('Director', 'view_kpi') is True
    assert roles.role_has('Program Officer', 'view_kpi') is True
    assert roles.role_has('Support Officer', 'view_kpi') is False
