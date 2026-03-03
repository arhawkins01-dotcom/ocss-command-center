# OCSS Command Center — Technical Guide

Version: 1.3.0
Last Updated: 2026-03-03

---

## Executive Summary

OCSS Command Center is a role-based Streamlit application for establishment report ingestion, row-level workflow processing, KPI monitoring, and operational ticketing.

Key capabilities:
- Role-based dashboards (Director, Deputy Director, Department Manager, Senior Administrative Officer, Program Officer, Supervisor, Support Officer, IT Administrator)
- Report ingestion with metadata, duplicate detection, preview, and export
- Support Officer row-level processing with completion validation
- Help Ticket Center with auto-routing/auto-assignment and KPI views
- Best-effort on-disk persistence for organizational configuration and tickets

Recent implementation updates (2026-03-03):
- Sidebar role selection moved to two-stage grouped selection (`Role Group` + role dropdown) with last-selected-role defaulting.
- Administrative specialist roles now run a non-caseload processing workflow (report intake + tickets + knowledge base) while still reusing support-processing components where applicable.
- Program Officer legacy dashboard retained with agency-wide KPI filtering by Department, Unit, and Support Staff (Support Officer + Team Lead), with scope synchronization across KPI, Caseload Management, and Performance Analytics tabs.
- Support Officer/Team Lead authenticated sessions are identity-locked to the signed-in worker, and KPI/Throughput tracker tables are filtered to that worker only.

---

## Key Paths (Repository)

- App entry point: `app/app.py`
- Core report logic: `app/report_utils.py`
- App state (best-effort persisted): `data/state/ocss_app_state.json`
- In-app Knowledge Base folder: `data/knowledge_base/`
  - User Manual (target): `data/knowledge_base/user_guide.md`
  - Technical Guide (target): `data/knowledge_base/technical_guide.md`

---

## Role & View Resolution Notes

- Expanded role names are defined in `app/roles.py` (`EXPANDED_CORE_APP_ROLES`).
- View capability mapping is resolved by `map_to_view_role()` and `ROLE_VIEW_MAP`.
- Current UX grouping for unauthenticated role selection is implemented in `app/app.py`:
  - Leadership
  - Management
  - Program & CQI
  - Administrative
  - Support
  - IT

Administrative specialist roles are intentionally distinct from Support Officer role semantics:
- They do not receive Support Officer assigned-caseload management screens.
- They use administrative intake/ticket flows.

Support worker visibility controls:
- In authenticated mode, the Support Officer identity selector is disabled and replaced by signed-in identity lock.
- In no-auth/demo mode, the selector remains available for simulation and testing.
- `Support Officer KPI Tracker` and `Support Officer Throughput` are filtered to the active support worker context.

---

## Program Officer KPI Filter Implementation

Program Officer KPI scope controls are implemented in `app/app.py` and persisted in `st.session_state` keys:
- `po_kpi_department_filter`
- `po_kpi_unit_filter`
- `po_kpi_support_staff_filter`

Scope behavior:
- KPI metrics are computed over filtered assignment/report sets (not only viewer department).
- Monthly submission trends and support-staff snapshot are filtered by the same scope.
- Program Officer `Caseload Management` and `Performance Analytics` tabs read the same filter keys for consistent cross-tab views.
- `Reset all Program Officer filters` restores full agency scope defaults.

---

## Knowledge Base Seeding (How It Works)

The app seeds Knowledge Base documents into `data/knowledge_base/` when needed.

- User Manual seed source: `docs/USER_MANUAL.md`
- Technical Guide seed source: `data/knowledge_base/technical_guide.md`
- Seed manifest: `data/knowledge_base/.seed_manifest.json`

Behavior summary:
- If a KB document is missing, it is copied from its seed source.
- If a KB document has been edited using the in-app Knowledge Base Admin, it is not overwritten.

---

## Persistence Model

The application uses a mixed persistence approach:

- Persisted (best-effort):
  - Organizational configuration (users/units)
  - Alert acknowledgements
  - Help tickets and ticket activity log
- Session-based (not persisted):
  - Uploaded report content and in-progress row edits

Persisted state is stored as JSON at `data/state/ocss_app_state.json`.

---

## Help Ticket Center Workflow (Technical Notes)

Tickets support a status lifecycle:
- `Open` → `Assigned` → `In Progress` → `Waiting on Submitter` → `Resolved`/`Closed`

Implementation notes:
- Ticket activity is appended to an on-disk log (best-effort persistence).
- Auto-assignment occurs when one or more IT Administrators exist in User Management.
- `Resolved` and `Closed` require a resolution text in the UI.

---

## Running Locally

Install dependencies:

```bash
pip install -r app/requirements.txt
```

Run Streamlit:

```bash
streamlit run app/app.py --server.enableCORS false --server.enableXsrfProtection false
```

---

## Deployment Notes

- Streamlit Cloud uses `app/app.py` as the main file path.
- For internal hosting, ensure the `data/` directory is writable if persistence is required.
- Authentication mode is controlled via `OCSS_AUTH_MODE` (see `app/auth.py`).

---

## Testing

Run unit tests:

```bash
pytest -q
```

---

End of Technical Guide
