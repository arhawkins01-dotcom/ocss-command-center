# OCSS Command Center — User Manual

Version: 1.3.0
Last Updated: 2026-03-03

---

## Change Log
- 2026-02-27 — Consolidated manual, clarified role workflows, standardized UI label `💾 Save Progress` across instructions.
- 2026-03-02 — Documented Help Ticket Center workflow (auto-routing/assignment, statuses, IT actions) and updated instructions for Executive Intake step flow + Support Officer completion UX.
- 2026-03-03 — Simplified sidebar role selection (Role Group + Role dropdown), added Administrative role workflow distinction (non-caseload), and documented Program Officer agency-wide KPI filters (Department, Unit, Support Staff) synchronized across KPI/Caseload/Performance tabs.
- 2026-03-03 — Added Support Officer/Team Lead authenticated identity lock and self-only visibility for KPI Tracker + Throughput tables.

## Table of Contents

1. System Overview
2. Getting Started
3. Roles & Dashboards
4. KPIs & Metrics Dashboards
5. Report Intake & Processing — Step-by-step
6. Caseload Management & Assignment Flows
7. Knowledge Base & Documentation Workflow
8. Help Ticket Center Workflow
9. Operational Notes & Troubleshooting
10. Screenshots & Training Aids
11. Appendix: Report Types & Field Rules
12. Glossary & Contact

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

Role selection now uses a 2-step picker:
- `Role Group` (Leadership, Management, Program & CQI, Administrative, Support, IT)
- `Select Your Role` (filtered by selected group)

Tip: the app remembers your last selected role and reopens to that role/group by default.

Quick tips:
- Use the `Knowledge Base` tab for how-to articles and this manual.
- Export CSVs regularly for offline backups when doing bulk edits.

---

## Roles & Dashboards

Each role has a tailored view and permission set. Below are concise responsibilities and common tasks.

### Director / Deputy Director
- Purpose: Strategic oversight, leadership exports, escalation decisions
- Key views: Organization-level KPIs, Caseload Work Status, Team Performance Analytics, Leadership QA Exports
- Common tasks: Review escalated items, download briefing packet, set priorities

### Department Manager / Senior Administrative Officer
- Purpose: Operational oversight for units or regions
- Key views: Unit KPIs (Department scope for DM; Unit/Dept/Agency scope for SAO), QA Data Exports, Reassignments, Team Performance
- Common tasks: Reassign caseloads, validate unit structure, review monthly throughput

### Program Officer
- Purpose: Non-supervisory program/CQI oversight, report intake, and agency-wide KPI analysis
- Key views: Legacy Dashboard tabs (`Executive KPIs`, `Upload & Processing`, `Caseload Management`, `Performance Analytics`, `Ticket KPIs`, `Manage Users`, `Knowledge Base`)
- Common tasks: Upload reports, validate ingestion, monitor agency KPIs, and filter analytics across departments/units/support staff

### Administrative Roles (non-support workflow)
- Roles: `Administrative Assistant`, `Client Information Specialist`, `Client Information Specialist Team Lead`, `Case Information Specialist`, `Case Information Specialist Team Lead`
- Purpose: Administrative report processing workflows without Support Officer caseload ownership
- Key views: `Report Intake`, `Support Tickets`, `Knowledge Base`
- Notes:
  - These roles may process Excel reports but are not treated as Support Officers.
  - Assigned caseload dashboard behavior is intentionally disabled for this workflow.

### Supervisor
- Purpose: Team-level assignment, approve caseload submissions, and monitor team alerts
- Key views: KPI Metrics (Unit/Department scoped), QA Data Exports, My Team & Assignments, Worker Self-Pull, Team Performance Analytics
- Common tasks: Assign/reassign caseloads, acknowledge alerts, approve completed caseloads

### Support Officer / Team Lead
- Purpose: Row-level processing of reports (case lines), narration, and completion
- Key views: My Assigned Reports, Caseload Dashboard, Knowledge Base
- Common tasks: Process case rows, add narration, save progress, submit caseload when done
- Security behavior:
  - When authenticated, identity is locked to the signed-in Support Officer/Team Lead profile.
  - `Support Officer KPI Tracker (Assigned Reports)` and `Support Officer Throughput` show only the signed-in worker's rows.
  - In no-auth/demo mode, `Act as Support Officer / Team Lead` remains available for simulation.

### IT Administrator
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

Leadership exports produce Excel and Word briefing packets with pre-formatted summaries and an ingestion activity sheet. Exports are now directly available on the root KPI Metrics tab across all executive roles (Director, Deputy Director, Program Officer, Department Manager, SAO, and Supervisor). These exports include comprehensive QA flag summaries (FAIL/WARN/INFO/OK metrics with top failure reasons). Additionally, executive and supervisory roles now feature robust Team Performance Analytics views utilizing visual progress bars for individual worker completion rates.

### Program Officer KPI Filters (Agency-wide)
Program Officers have agency-wide KPI visibility with optional filters:
- `Department Filter`
- `Unit Filter`
- `Support Staff Filter (Support Officers + Team Leads)`

Behavior:
- Filters apply to KPI tiles, monthly submission trends, and support staff snapshot in `Executive KPIs`.
- The same filter scope is reused in Program Officer `Caseload Management` and `Performance Analytics` tabs for consistency.
- Use `Reset all Program Officer filters` to return to agency-wide view.

---

## Report Intake & Processing — Step-by-step

This section covers the canonical workflow from upload to caseload submission.

### Uploading & Preview (Program Officer)
1. Role: select `Program Officer`.
2. Open `Upload & Processing` and choose a target caseload.
3. Click `Browse files`, select `.xlsx` or `.csv` and confirm.
4. Review the ingest preview; fix column mapping if needed.
5. Set metadata (report type, frequency, period year/value).
6. Click `Process Report` (disabled until required fields are set).
7. Copy the ingestion ID for audit and future reference.

Notes:
- The intake UI follows a step flow (Upload → Process) to reduce accidental processing.
- Non-critical ingestion warnings are grouped in a collapsible warnings section.

### Duplicate Detection & QA
- The system uses a combination of metadata and content hashing to detect duplicate-period or near-duplicate uploads. If a duplicate is detected, you may:
  - Cancel if accidental
  - Proceed by enabling `Allow ingestion even if duplicate period report is detected` (use sparingly)

### Processing Rows (Support Officer)
Follow this per-row checklist for reliable narration and consistent status:
1. Open your `My Assigned Reports` queue and expand the next unworked row.
2. Review data sources (linked systems shown in the UI) and prior actions.
3. Select `Action Taken / Status` from the context menu (Schedule GT, Prep ADS, Postal Verification, Refer to Court, Close Case, etc.).
4. Enter `Date Action Taken`, mark `Case Narrated (Y/N)` to `Y` when complete, and add `Comments`.
5. Set `Worker Status` to `Completed` when the row is fully done. If required fields are missing for the report type, the app will revert the status and show what’s missing.
6. Click `💾 Save Progress` to persist edits.

Tip:
- If you are viewing `Pending / In Progress` rows, completed rows will be hidden by the filter.

### Conditional Submit
- When all rows assigned to the Support Officer are `Completed`, the Supervisor-level `✅ Submit Caseload as Complete` button becomes available. The app validates required fields for specific report types (56RA, P-S, Locate) and blocks submission until rules are satisfied.

---

## Caseload Management & Assignment Flows

Administrative workflow note:
- Administrative specialist roles (Client/Case Information Specialist tracks + Administrative Assistant) do not use Support Officer assigned-caseload dashboards.
- Team Leads remain in Support workflows (between Support Officer and Supervisor responsibilities).

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

## Knowledge Base & Documentation Workflow

- The canonical User Manual is `docs/USER_MANUAL.md` in this repository.
- The Technical Guide is maintained in `data/knowledge_base/technical_guide.md` (used as the seed source for the in-app Technical Guide).
- On first seed the application copies the sources into the Knowledge Base folder and records the seed in `.seed_manifest.json`.
- If a document is edited through the in-app Knowledge Base Admin, the seeder will not overwrite it unless `edited_by_admin` is cleared.

Authoring notes:
- Keep the manual concise and role-focused.
- For KB edits that must persist, edit via the in-app Knowledge Base Admin to prevent overwrites from repository seeds.

---

## Help Ticket Center Workflow

The Help Ticket Center is the single workflow for reporting issues (upload problems, authentication, validation, performance, etc.) and tracking resolution.

### Where to find it
- **Support Officer**: `🆘 Support Tickets` tab
- **Director / Program Officer / Supervisor**: `🆘 Ticket KPIs` tab (includes both KPI view and the Ticket Center)
- **IT Administrator**: `🆘 Ticket KPIs` tab (includes IT actions)

### Submitting a ticket
1. Enter your name and pick an Establishment, Priority, and Issue Category.
2. Describe the issue and click `Submit Help Ticket`.
3. The system adds a **Suggested resolution** to speed triage.
4. **Auto-routing / auto-assign:** if one or more IT Administrators exist in User Management, the ticket is auto-assigned to an IT Administrator and starts in `Assigned` status.

### Statuses (meaning)
- `Open`: created but not assigned
- `Assigned`: assigned to an IT Administrator
- `In Progress`: actively being worked
- `Waiting on Submitter`: needs additional info from the submitter
- `Resolved`: fixed (resolution recorded)
- `Closed`: resolved + closed (resolution recorded)

### Comments and audit trail
- Use `Add Comment` to add context; every comment and IT update is recorded in the Ticket Activity Log.

### IT actions
- IT can change `Assigned To`, update `Status`, mark `IT Verified`, and record `Resolution`.
- `Resolution` is required for `Resolved` and `Closed`.

### Persistence
- Tickets and their activity log persist in the app state file under `data/state/ocss_app_state.json` (best-effort persistence).

---


## Operational Notes & Troubleshooting

Common issues and quick fixes:

- I don't see my caseloads:
  - Authenticated mode: verify your signed-in account is mapped to a Support Officer/Team Lead user profile.
  - No-auth/demo mode: select your name in `Act as Support Officer / Team Lead`.
- Upload preview looks wrong: verify `.xlsx`/`.csv` format and column headers.
- Duplicate ingestion blocked: confirm metadata and enable `Allow ingestion` if intentional.
- Can't pull a caseload: ensure you have permission and that `Simulate Current Worker` matches `Pull As`.
- Report not saving: click `💾 Save Progress`, check for session expiration, and export CSV as backup.
- I can't find my ticket: verify your name matches the ticket submitter name exactly; in the Ticket Center choose `View: My Tickets` or switch to `All Tickets` (leadership/IT).
- Ticket stuck in Assigned: IT must update status to `In Progress`/`Resolved` and record a resolution when complete.

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
