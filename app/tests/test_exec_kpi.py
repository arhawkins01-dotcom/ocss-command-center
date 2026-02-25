import importlib.util
import os
import sys
import streamlit as st
from datetime import datetime, timedelta

# Ensure the app source directory is importable (so report_utils and others resolve)
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Load helpers module directly to avoid package import issues during pytest collection
_helpers_path = os.path.join(app_dir, 'helpers.py')
spec = importlib.util.spec_from_file_location("app_helpers", _helpers_path)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
get_kpi_metrics = helpers.get_kpi_metrics


def test_get_kpi_metrics_basic():
    st.session_state.clear()
    # Two caseloads: one completed, one pending
    st.session_state['reports_by_caseload'] = {
        '181000': [
            {
                'report_id': 'RPT-181000-001',
                'status': 'Completed',
                'qa_summary': {'rows_canonical': 10, 'missing_case_number': 0, 'invalid_service_due_date': 0, 'invalid_action_taken_date': 0, 'invalid_case_narrated': 0, 'duplicate_rows': 0},
                'report_type': 'General',
                'owning_department': 'Establishment'
            }
        ],
        '181001': [
            {
                'report_id': 'RPT-181001-001',
                'status': 'Ready for Processing',
                'qa_summary': {'rows_canonical': 5, 'missing_case_number': 1, 'invalid_service_due_date': 0, 'invalid_action_taken_date': 0, 'invalid_case_narrated': 0, 'duplicate_rows': 0},
                'report_type': 'CQI Alignment',
                'owning_department': 'Establishment'
            }
        ]
    }

    now = datetime.now()
    st.session_state['upload_audit_log'] = [
        {'report_id': 'RPT-181000-001', 'uploaded_at': (now - timedelta(days=1)).isoformat(), 'due_at': now.isoformat(), 'owning_department': 'Establishment'},
        {'report_id': 'RPT-181001-001', 'uploaded_at': (now + timedelta(days=2)).isoformat(), 'due_at': (now + timedelta(days=1)).isoformat(), 'owning_department': 'Establishment'},
    ]

    kpis = get_kpi_metrics(department=None)
    assert kpis['report_completion_rate'] == 50.0
    assert kpis['cqi_alignments'] == 1
    # on-time: one of two with due_at is on-time -> 50.0
    assert kpis['on_time_submissions'] == 50.0
    # data quality: (15 total rows, 1 problem) -> (14/15)*100 = 93.3...
    assert round(kpis['data_quality_score'], 1) == 93.3
