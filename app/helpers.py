import pandas as pd
import streamlit as st
from datetime import datetime

try:
    from .report_utils import normalize_caseload_number as _normalize_caseload_number
except Exception:
    from report_utils import normalize_caseload_number as _normalize_caseload_number

try:
    from .roles import role_has
except Exception:
    try:
        from roles import role_has
    except Exception:
        def role_has(role, cap):
            return True


def normalize_caseload_number(raw_value: str) -> str:
    return _normalize_caseload_number(raw_value)


def assign_caseloads_bulk(worker_name: str, caseload_numbers: list):
    """Assign multiple caseloads to a single worker using session state.

    This implementation is intentionally self-contained so tests can import
    it without triggering the Streamlit UI in `app/app.py`.
    """
    successes = []
    failures = []

    caller_role = st.session_state.get('current_role')
    if caller_role and not role_has(caller_role, 'reassign'):
        for c in caseload_numbers:
            failures.append((c, 'Permission denied'))
        return successes, failures

    st.session_state.setdefault('units', {})
    st.session_state.setdefault('reports_by_caseload', {})

    for raw in (caseload_numbers or []):
        n = normalize_caseload_number(raw)
        if not n:
            failures.append((raw, 'Invalid caseload number'))
            continue

        # find unit for worker
        unit_found = None
        for unit_name, unit in st.session_state.get('units', {}).items():
            unit_workers = set(unit.get('support_officers') or []) | set(unit.get('team_leads') or [])
            # Allow optional specialist lists if present in the unit model.
            unit_workers |= set(unit.get('client_info_specialists') or [])
            unit_workers |= set(unit.get('client_info_team_leads') or [])
            unit_workers |= set(unit.get('case_info_specialists') or [])
            unit_workers |= set(unit.get('case_info_team_leads') or [])
            if worker_name in unit_workers:
                unit_found = unit_name
                break

        if not unit_found:
            # try to infer unit from users list
            for u in st.session_state.get('users', []):
                if str(u.get('name', '')).strip() == str(worker_name).strip():
                    # New schema: prefer explicit unit field. Legacy schema: unit stored in department.
                    unit_found = str(u.get('unit', '')).strip() or str(u.get('department', '')).strip() or None
                    break

        if not unit_found:
            failures.append((raw, f"Worker '{worker_name}' not linked to a unit"))
            continue

        unit = st.session_state['units'].setdefault(unit_found, {})
        unit.setdefault('assignments', {})
        unit.setdefault('support_officers', [])
        unit.setdefault('team_leads', [])

        if worker_name not in unit.get('support_officers') and worker_name not in unit.get('team_leads'):
            unit.setdefault('support_officers', []).append(worker_name)

        unit['assignments'].setdefault(worker_name, [])
        if n not in unit['assignments'][worker_name]:
            unit['assignments'][worker_name].append(n)

        st.session_state['reports_by_caseload'].setdefault(n, [])
        successes.append((raw, f"Assigned {n} to {worker_name}"))

    return successes, failures


def get_kpi_metrics(department: str | None = None) -> dict:
    """Compute KPI metrics from session_state: completion, on-time, data quality, CQI alignments.

    Returns a dict with keys: report_completion_rate, on_time_submissions,
    data_quality_score, cqi_alignments.
    """
    reports = st.session_state.get('reports_by_caseload', {}) or {}
    upload_log = st.session_state.get('upload_audit_log', []) or []

    total_reports = 0
    completed_reports = 0
    rows_canonical = 0
    problem_count = 0
    cqi_alignments = 0

    for caseload, rep_list in reports.items():
        for r in (rep_list or []):
            # Department scoping
            if department:
                if str(r.get('owning_department', '')).strip() != str(department).strip():
                    continue

            total_reports += 1
            status = str(r.get('status', '')).strip().lower()
            if status in ('completed', 'finished', 'submitted', 'submitted for review'):
                completed_reports += 1

            qa = r.get('qa_summary') or {}
            try:
                rows = int(qa.get('rows_canonical', 0))
            except Exception:
                rows = 0
            rows_canonical += rows
            problem_count += sum(int(qa.get(k, 0)) for k in ['missing_case_number', 'invalid_service_due_date', 'invalid_action_taken_date', 'invalid_case_narrated', 'duplicate_rows'] if k in qa)

            if 'cqi' in str(r.get('report_type', '')).lower():
                cqi_alignments += 1

    # On-time submissions
    on_time = 0
    total_audits = 0
    for entry in (upload_log or []):
        # support both datetime and iso strings
        try:
            uploaded = pd.to_datetime(entry.get('uploaded_at'))
            due = pd.to_datetime(entry.get('due_at'))
            total_audits += 1
            if uploaded <= due:
                on_time += 1
        except Exception:
            continue

    report_completion_rate = (completed_reports / total_reports * 100) if total_reports > 0 else 0.0
    on_time_submissions = (on_time / total_audits * 100) if total_audits > 0 else 0.0
    data_quality_score = ((rows_canonical - problem_count) / rows_canonical * 100) if rows_canonical > 0 else 100.0

    return {
        'report_completion_rate': round(report_completion_rate, 1),
        'on_time_submissions': round(on_time_submissions, 1),
        'data_quality_score': round(data_quality_score, 1),
        'cqi_alignments': int(cqi_alignments),
    }
