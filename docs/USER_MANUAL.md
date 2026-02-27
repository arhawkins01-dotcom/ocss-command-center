# OCSS Command Center — User Manual

Version: 1.1.0
Last Updated: 2026-02-27

---

## Change Log
- 2026-02-27 — Consolidated manual, clarified role workflows, standardized UI label `💾 Save Progress` across instructions.

## Table of Contents

1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [Roles & Dashboards](#roles--dashboards)
   - [Director / Deputy Director](#director--deputy-director)
   - [Department Manager / Senior Administrative Officer](#department-manager--senior-administrative-officer)
   - [Program Officer](#program-officer)
   - [Supervisor](#supervisor)
   - [Support Officer / Team Lead](#support-officer--team-lead)
   - [IT Administrator](#it-administrator)
4. [KPIs & Metrics Dashboards](#kpis--metrics-dashboards)
5. [Report Intake & Processing — Step-by-step](#report-intake--processing---step-by-step)
6. [Caseload Management & Assignment Flows](#caseload-management--assignment-flows)
7. [Knowledge Base & Documentation Workflow](#knowledge-base--documentation-workflow)
8. [Operational Notes & Troubleshooting](#operational-notes--troubleshooting)
9. [Screenshots & Training Aids](#screenshots--training-aids)
10. [Appendix: Report Types & Field Rules](#appendix-report-types--field-rules)
11. [Glossary & Contact](#glossary--contact)

---

## System Overview

OCSS Command Center is a lightweight Streamlit-based web application designed to ingest, QA, and route caseload reports across organizational roles. It provides:

- A secure role-based dashboard for daily work
- An ingestion pipeline with duplicate detection and preview
- Row-level (case-line) processing UI for Support Officers
- Caseload assignment and unit management tools for Supervisors and IT
- KPI dashboards for leadership monitoring and exports for briefings

The application seeds user-facing documentation from `docs/USER_MANUAL.md` into `data/knowledge_base/user_guide.md` on first run (unless edited via the in-app Knowledge Base Admin).

## Getting Started

1. Open the app (Streamlit) and choose a role from the left sidebar.
2. If authentication is enabled, sign in; otherwise, select the role and pick your name where required.
3. Review your assigned dashboard tiles and alerts.

Quick tips:
- Use the `Knowledge Base` tab for how-to articles and this manual.
- Export CSVs regularly for offline backups when doing bulk edits.

---

## Roles & Dashboards

Each role has a tailored view and permission set. Below are concise responsibilities and common tasks.

Director / Deputy Director
- Purpose: Strategic oversight, leadership exports, escalation decisions
- Key views: Organization-level KPIs, Caseload Work Status, Leadership Exports
- Common tasks: Review escalated items, download briefing packet, set priorities

Department Manager / Senior Administrative Officer
- Purpose: Operational oversight for units or regions
- Key views: Unit KPIs, Reassignments, Team Performance
- Common tasks: Reassign caseloads, validate unit structure, review monthly throughput

Program Officer
- Purpose: Upload and seed reports, validate ingestion, and monitor program-level throughput
- Key views: Upload & Processing, Ingestion Registry, Program KPIs
- Common tasks: Upload reports, fix ingestion preview issues, run exports for program reporting

Supervisor
- Purpose: Team-level assignment, approve caseload submissions, and monitor team alerts
- Key views: My Team & Assignments, Worker Self-Pull, Team Performance
- Common tasks: Assign/reassign caseloads, acknowledge alerts, approve completed caseloads

Support Officer / Team Lead
- Purpose: Row-level processing of reports (case lines), narration, and completion
- Key views: My Assigned Reports, Caseload Dashboard, Knowledge Base
- Common tasks: Process case rows, add narration, save progress, submit caseload when done

IT Administrator
- Purpose: User and unit management, audit logs, system health, backups
- Key views: User & Caseload Management, System Status, Maintenance & Logs
- Common tasks: Add/remove users, create units, run diagnostics, back up logs

---

## KPIs & Metrics Dashboards

Dashboards show throughput (7/30-day), completion rates, and aging items. Common KPIs:

- Reports Ingested (period)
- Average Days to Complete
- % Completed On Time
- Unassigned Caseloads
- Escalations by Age Bucket

Leadership exports produce Excel and Word briefing packets with pre-formatted summaries and an ingestion activity sheet.

---

## Report Intake & Processing — Step-by-step

This section covers the canonical workflow from upload to caseload submission.

Uploading & Preview (Program Officer)
1. Role: select `Program Officer`.
2. Open `Upload & Processing` and choose a target caseload.
3. Click `Browse files`, select `.xlsx` or `.csv` and confirm.
4. Review the ingest preview; fix column mapping if needed.
5. Set metadata (report type, frequency, period year/value) and click `Process Report`.
6. Copy the ingestion ID for audit and future reference.

Duplicate Detection & QA
- The system uses a combination of metadata and content hashing to detect duplicate-period or near-duplicate uploads. If a duplicate is detected, you may:
  - Cancel if accidental
  - Proceed by enabling `Allow ingestion even if duplicate period report is detected` (use sparingly)

Processing Rows (Support Officer)
Follow this per-row checklist for reliable narration and consistent status:
1. Open your `My Assigned Reports` queue and expand the next unworked row.
2. Review data sources (linked systems shown in the UI) and prior actions.
3. Select `Action Taken / Status` from the context menu (Schedule GT, Prep ADS, Postal Verification, Refer to Court, Close Case, etc.).
4. Enter `Date Action Taken`, mark `Case Narrated (Y/N)` to `Y` when complete, and add `Comments`.
5. Click `💾 Save Progress` to persist edits.

Conditional Submit
- When all rows assigned to the Support Officer are `Completed`, the Supervisor-level `✅ Submit Caseload as Complete` button becomes available. The app validates required fields for specific report types (56RA, P-S, Locate) and blocks submission until rules are satisfied.

---

## Caseload Management & Assignment Flows

Assigning & Reassigning (Supervisor / IT)
1. Select `Supervisor` role and your supervisor name.
2. Open `My Team & Assignments` and choose the desired unit.
3. Use `Assign/Move Caseload` to move work between team members; confirm in modal.

Worker Self-Pull (Supervisor view — Team Leads)
- Team Leads and designated roles may claim unassigned caseloads by using the `Worker Self-Pull` control. Ensure `Simulate Current Worker` and `Pull As` match exactly.

How it works:
1. Select `Supervisor` role in the sidebar.
2. Choose your supervisor name from the dropdown.
3. In the `Unassigned Caseloads` list, select a caseload.
4. Click `Pull Selected Caseload to Myself` to assign it to yourself.

Availability hints:
- Green info box: Caseload already assigned to you
- Orange warning: Caseload assigned to someone else (pull blocked)
- No message: Caseload is available for claiming

Access: Supervisors, Director, Deputy Director, Senior Administrative Officer, Program Officer, Team Leads. Regular Support Officers (non-Team Leads) cannot claim via this control.

Audit Trail & Logs
- All assignment and removal actions are logged. IT Admins can filter `Recent System Activity` to review changes by user and timestamp.

---

Knowledge Base & Documentation Workflow

- The canonical manual is `docs/USER_MANUAL.md` in this repository.
- On first seed the application copies it to `data/knowledge_base/user_guide.md` and records the seed in `.seed_manifest.json`.
- If a document is edited through the in-app Knowledge Base Admin, the seeder will not overwrite it unless `edited_by_admin` is cleared.

Authoring notes:
- Keep the manual concise and role-focused.
- For KB edits that must persist, edit via the in-app Knowledge Base Admin to prevent overwrites from repository seeds.

---


Operational Notes & Troubleshooting

Common issues and quick fixes:

- I don't see my caseloads: select your name in `Act as Support Officer / Team Lead`.
- Upload preview looks wrong: verify `.xlsx`/`.csv` format and column headers.
- Duplicate ingestion blocked: confirm metadata and enable `Allow ingestion` if intentional.
- Can't pull a caseload: ensure you have permission and that `Simulate Current Worker` matches `Pull As`.
- Report not saving: click `💾 Save Progress`, check for session expiration, and export CSV as backup.

If the page won't load:
1. Check network and server (Streamlit) status.
2. Refresh the browser and clear cache.
3. Contact IT Admin if the problem persists.

---

## Screenshots & Training Aids

Placeholders for screenshots and short videos help new users. Suggested assets:

- Dashboard overview (roles and main tiles)
- Upload & preview walkthrough
- Row-level processing example (narration + update)
- Supervisor reassign flow

Add images to the Knowledge Base or attach them to training packets for briefing exports.

---

## Appendix: Report Types & Field Rules

Common report types and required fields:

- 56RA / Locate: require narration, `Action Taken` dropdown, and closure codes when applicable.
- P-S (Paternity-Support): `P-S Report` narration prefix; follow P-S action codes.
- Standard ingestion rules: period/frequency/type must be provided for duplicate detection.

Field rules & guards are enforced during submission; the UI will show specific required fields when attempting to mark a row `Completed`.

---

## Glossary & Contact

- NCP: Non-Custodial Parent
- CP/CTR: Custodial Parent / Contact
- GT: Genetic Testing
- ADS: Alternative Dispute Services
- OnBase: Document repository reference

For technical issues: contact IT Administrator — it-support@ocss.agency.gov
For workflow questions: contact your Supervisor
For enhancement requests: route through IT Admin and Director as described in-app

---

End of User Manual

For repository-based KB updates: edit `docs/USER_MANUAL.md` and then copy to `data/knowledge_base/user_guide.md` (the app seeds the KB on next startup if not edited in-app).
