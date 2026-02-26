import pandas as pd
from app.app import _filter_alerts_for_viewer


def make_row(report_id, caseload, unit, assigned_to, days_since, days_overdue=0, acks=None):
    acks = acks or {}
    row = {
        'Report ID': report_id,
        'Caseload': caseload,
        'Unit': unit,
        'Assigned To': assigned_to,
        'Unassigned': assigned_to == '',
        'Days Since Upload': days_since,
        'Days Overdue': days_overdue,
        'worker_ack': bool(acks.get('worker_ack')),
        'supervisor_ack': bool(acks.get('supervisor_ack')),
        'program_officer_ack': bool(acks.get('program_officer_ack')),
        'department_manager_ack': bool(acks.get('department_manager_ack')),
        'director_ack': bool(acks.get('director_ack')),
    }
    return row


def test_unassigned_visible_to_director():
    # Unassigned should be visible to Director regardless of days-since filter
    rows = [
        make_row('R1', '181000', 'UnitA', '', days_since=0),
    ]
    df = pd.DataFrame(rows)

    filtered = _filter_alerts_for_viewer(df, viewer_role='Director', viewer_name='', scope_unit=None, viewer_unit_role='')
    assert not filtered.empty
    assert 'R1' in filtered['Report ID'].astype(str).tolist()


def test_support_officer_sees_assigned_recent_items_only():
    # Support Officer should only see assigned recent items (1-3 days window)
    rows = [
        make_row('R1', '181000', 'UnitA', 'Alice', days_since=2),
        make_row('R2', '181001', 'UnitB', '', days_since=0),
    ]
    df = pd.DataFrame(rows)

    filtered = _filter_alerts_for_viewer(df, viewer_role='Support Officer', viewer_name='Alice', scope_unit=None, viewer_unit_role='')
    ids = filtered['Report ID'].astype(str).tolist()
    assert 'R1' in ids
    assert 'R2' not in ids


def test_director_department_manager_scope():
    # Director acting as Department Manager should see 1-10 day items for department scope
    rows = [
        make_row('R10', '181000', 'UnitA', 'Bob', days_since=5, acks={}),
    ]
    df = pd.DataFrame(rows)
    filtered = _filter_alerts_for_viewer(df, viewer_role='Director', viewer_name='Director User', scope_unit=None, viewer_unit_role='Department Manager')
    assert not filtered.empty
    assert 'R10' in filtered['Report ID'].astype(str).tolist()
