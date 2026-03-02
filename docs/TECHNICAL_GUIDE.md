# OCSS Command Center — Technical Guide

Version: 1.2.0
Last Updated: 2026-03-02

---

## Executive Summary

OCSS Command Center is a role-based Streamlit application for establishment report ingestion, row-level workflow processing, KPI monitoring, and operational ticketing.

Key capabilities:
- Role-based dashboards (Director, Program Officer, Supervisor, Support Officer, IT Administrator)
- Report ingestion with metadata, duplicate detection, preview, and export
- Support Officer row-level processing with completion validation
- Help Ticket Center with auto-routing/auto-assignment and KPI views
- Best-effort on-disk persistence for organizational configuration and tickets

---

## Key Paths (Repository)

- App entry point: `app/app.py`
- Core report logic: `app/report_utils.py`
- App state (best-effort persisted): `data/state/ocss_app_state.json`
- In-app Knowledge Base folder: `data/knowledge_base/`
  - User Manual (target): `data/knowledge_base/user_guide.md`
  - Technical Guide (target): `data/knowledge_base/technical_guide.md`

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
