# OCSS Command Center — Technical Guide

Version: 1.3.1
Last Updated: 2026-03-09

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

Recent implementation updates (2026-03-09):
- Support Officer processing UI now includes report-type visual badges, dynamic required-field guidance, narration templates, and per-row completion indicators to reduce completion errors before submission.

---

## Architecture & Data Flow (Enterprise View)

This section combines the platform architecture and enterprise workflow flow into a single review-ready reference for technical guide, slides, and IT review packets.

### Diagram 1: OCSS Command Center Enterprise System Architecture

```text
┌──────────────────────────────────────────────────────────────────┐
│ OCSS USERS / CLIENT LAYER                                        │
│                                                                  │
│ Director | Deputy Director | Program Officers | Supervisors     │
│ Team Leads | Support Officers | Administrative Specialists      │
│                                                                  │
│ Access via Modern Web Browser (Chrome / Edge / Firefox)          │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                │ HTTPS
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ REVERSE PROXY / AUTH LAYER                                       │
│                                                                  │
│ County Gateway / NGINX                                           │
│                                                                  │
│ • SSL/TLS Encryption                                             │
│ • Single Sign-On Authentication                                  │
│ • Security Filtering                                             │
│                                                                  │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ OCSS COMMAND CENTER APPLICATION                                  │
│                                                                  │
│ Python + Streamlit Web Application                               │
│                                                                  │
│ Core Components                                                  │
│                                                                  │
│ • Role-Based Access Control                                      │
│ • Report Ingestion Engine                                        │
│ • Caseload Management Engine                                     │
│ • KPI & Performance Dashboards                                   │
│ • QA & Compliance Metrics                                        │
│ • Help Ticket Center                                             │
│ • Knowledge Base                                                 │
│                                                                  │
│ Runtime Services                                                 │
│                                                                  │
│ • Session State Management                                       │
│ • Data Validation                                                │
│ • Escalation Alert Logic                                         │
│ • Due-Date Clock Processing                                      │
│                                                                  │
└───────────────────────────┬───────────────┬──────────────────────┘
                            │               │
                            │               │
                            ▼               ▼
        ┌──────────────────────┐ ┌─────────────────────────┐
        │ REPORT PROCESSING    │ │ APPLICATION STATE       │
        │                      │ │                         │
        │ Pandas Data Engine   │ │ Persistent Storage      │
        │                      │ │                         │
        │ • Excel Parsing      │ │ • Organizational Config │
        │ • CSV Imports        │ │ • User Assignments      │
        │ • Row Processing     │ │ • Help Tickets          │
        │ • KPI Aggregation    │ │ • Alert Acknowledges    │
        │                      │ │                         │
        └──────────────┬───────┘ └──────────────┬──────────┘
                       │                        │
                       ▼                        ▼
           ┌──────────────────────┐ ┌──────────────────────┐
           │ FILE STORAGE         │ │ EXPORT SERVICES      │
           │                      │ │                      │
           │ Uploaded Reports     │ │ Excel Exports        │
           │ CSV Imports          │ │ Word Leadership Pack  │
           │ Processing Logs      │ │ CSV Downloads        │
           │                      │ │                      │
           └──────────────┬───────┘ └──────────────┬───────┘
                          │                        │
                          ▼                        ▼
┌──────────────────────────────────────────────────────────────────┐
│ EXISTING OCSS SYSTEM ECOSYSTEM                                   │
│                                                                  │
│ • SETS Child Support System                                      │
│ • Hyland OnBase                                                  │
│ • ODJFS Operational Reports (56RA / P-S / Locate)                │
│                                                                  │
│ The Command Center enhances operational workflow visibility      │
│ and leadership oversight while official case records remain      │
│ within the authorized systems of record.                         │
└──────────────────────────────────────────────────────────────────┘
```

### Diagram 2: OCSS Command Center Enterprise Data Flow

```text
┌──────────────────────────────────────────────────────────────────────┐
│ SOURCE REPORT / INPUT LAYER                                          │
│ ODJFS / OCSS Operational Reports                                     │
│ • 56RA Report • P-S Report • Locate Report • Approved Excel / CSV    │
└───────────────────────────────┬──────────────────────────────────────┘
                                │ Upload / Import
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ PROGRAM OFFICER INGESTION WORKFLOW                                   │
│ Upload & Processing Module                                            │
│ • File selection • Report type • Period metadata                     │
│ • Duplicate/content-hash check • Ingestion registry • Warnings       │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ REPORT NORMALIZATION ENGINE                                           │
│ Python / Pandas Processing                                            │
│ • Parse Excel/CSV • Normalize columns • Schema map                   │
│ • Assign report IDs • Compute due clocks/escalation windows          │
│ • Route report to assigned caseload                                  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
               ┌────────────────┼────────────────┐
               │                │                │
               ▼                ▼                ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────────┐
│ CASELOAD ASSIGNMENT │ │ ALERTS ENGINE   │ │ INGESTION AUDIT LAYER   │
│ • Unit/worker route │ │ • Due soon      │ │ • Upload timestamp      │
│ • Queue ownership   │ │ • Overdue       │ │ • Source file name      │
│ • Team lead visibility││ • Escalations  │ │ • Content hash/ID       │
└───────────┬─────────┘ └────────┬────────┘ └────────────┬────────────┘
            │                    │                       │
            └──────────────┬─────┴───────────────┬───────┘
                           │                     │
                           ▼                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ SUPPORT OFFICER / TEAM LEAD PROCESSING                               │
│ Assigned Reports Workflow                                             │
│ • Caseload queue • Row-by-row processing • Required-field guidance   │
│ • Report-type badges • Narration templates • Progress indicators     │
│ • Save to session state • Submit completed work                      │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ VALIDATION & QUALITY CONTROL                                          │
│ • Block incomplete submission                                          │
│ • Identify pending/in-progress rows                                   │
│ • Trigger QA sampling for eligible completed rows                     │
│ • Route to supervisory QA review                                      │
│ • Feed QA/compliance metrics to leadership dashboards                 │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
               ┌────────────────┼────────────────┐
               │                │                │
               ▼                ▼                ▼
┌─────────────────────┐ ┌──────────────────┐ ┌────────────────────────┐
│ LEADERSHIP METRICS  │ │ EXPORT SERVICES  │ │ SUPPORT TICKET CENTER  │
│ • KPI dashboards    │ │ • Excel exports  │ │ • Issue intake         │
│ • Team performance  │ │ • Word packets   │ │ • Auto-routing         │
│ • Caseload status   │ │ • CSV downloads  │ │ • Assignment tracking  │
│ • Throughput + QA   │ │                  │ │ • Ticket KPIs          │
└───────────┬─────────┘ └────────┬─────────┘ └────────────┬───────────┘
            │                    │                        │
            └──────────────┬─────┴──────────────┬─────────┘
                           │                    │
                           ▼                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│ LIMITED PERSISTENCE / SYSTEM STATE                                   │
│ Persisted: org config, caseload assignment settings, tickets, alerts │
│ Session-only: active report work, row state, temporary workflow data │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ OFFICIAL OCSS / STATE SYSTEMS OF RECORD                              │
│ SETS Child Support System, Hyland OnBase, ODJFS/OCSS structures      │
│ Command Center supports governance workflow and visibility only.      │
└──────────────────────────────────────────────────────────────────────┘
```

Figure: OCSS Command Center Enterprise Data Flow
This diagram illustrates how operational reports are ingested, normalized, routed, processed, validated, and surfaced through leadership dashboards while maintaining the Command Center's role as a companion workflow governance platform rather than an official system of record.

### Plain-Language Narrative for IT Review

1. Source report intake begins with Program Officer uploads of approved operational report files (56RA, P-S, Locate, approved Excel/CSV).
2. Ingestion control identifies report type, applies period metadata, checks duplicates/content hash, creates ingestion records, and surfaces warnings.
3. Normalization standardizes column/schema structure, assigns report IDs, computes due clocks/escalation timing, and routes work to caseload ownership.
4. Support Officers and Team Leads process assigned report rows with report-type guidance, templates, and row-level progress controls.
5. Validation blocks incomplete completion attempts and triggers QA sampling/review for eligible completed rows.
6. Leadership and operations outputs feed KPI dashboards, QA/compliance views, export services, and support ticket analytics.
7. Persistence remains intentionally bounded: limited administrative state is saved, while authoritative case records stay in agency systems of record.

### Authoritative Data Boundary

The OCSS Command Center enhances workflow coordination, processing visibility, and operational oversight. Official child support case records and authoritative case actions remain governed by existing authorized agency systems, including SETS and OnBase.

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

## Support Officer QA UI Enhancements (Technical Notes)

Support Officer row-level processing received usability and validation-focused UI enhancements.

Primary implementation points:
- Helper module: `app/support_officer_ui_helpers.py`
- Integration surface: `app/app.py` (Support Officer processing flow)

Implemented UI components:
- Report-type badge renderer for LOCATE, P-S, 56RA, and Case Closure workflows.
- Dynamic required-fields panel that reflects report-specific and conditional requirements.
- Quick-copy narration templates scoped by report type.
- Per-row completion indicator showing readiness and missing-field context.

Behavioral intent:
- Move completion guidance into the active row workflow instead of static instructions.
- Reduce invalid completion attempts by exposing missing requirements before save/submit.
- Improve consistency of narration and case notes by providing context templates.

Operational coupling with QA system:
- When a caseload is submitted as complete, QA sampling is auto-triggered for eligible completed rows.
- Supervisor review occurs in `🎯 QA Review`; executive rollups appear in `🎯 QA & Compliance`.

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
