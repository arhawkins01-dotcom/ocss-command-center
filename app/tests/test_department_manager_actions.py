import sys
import os

# Ensure app package is importable when tests run in CI or locally
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import importlib.util
import os
import sys
import streamlit as st

# Ensure the app source directory is importable (so report_utils and others resolve)
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Load helpers module directly to avoid package import issues during pytest collection
_helpers_path = os.path.join(app_dir, 'helpers.py')
spec = importlib.util.spec_from_file_location("app_helpers", _helpers_path)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
assign_caseloads_bulk = helpers.assign_caseloads_bulk
normalize_caseload_number = helpers.normalize_caseload_number
import streamlit as st


def test_department_manager_bulk_reassign():
    # Prepare minimal session state for department and units
    st.session_state.clear()
    st.session_state['users'] = [
        {'name': 'Alice', 'department': 'DeptA'},
        {'name': 'Bob', 'department': 'DeptA'},
    ]
    st.session_state['units'] = {
        'Unit1': {
            'supervisor': 'Alice',
            'support_officers': ['Bob'],
            'team_leads': [],
            'assignments': {'Bob': []},
        }
    }
    st.session_state['reports_by_caseload'] = {}
    # Set caller role to Department Manager to satisfy server-side guard
    st.session_state['current_role'] = 'Department Manager'

    successes, failures = assign_caseloads_bulk('Bob', ['1001', '1002'])

    assert len(successes) == 2, f"Expected 2 successes, got {len(successes)}"
    assert len(failures) == 0, f"Expected 0 failures, got {len(failures)}"
    n1 = normalize_caseload_number('1001')
    n2 = normalize_caseload_number('1002')
    assert n1 in st.session_state['units']['Unit1']['assignments']['Bob']
    assert n2 in st.session_state['units']['Unit1']['assignments']['Bob']
