# OCSS Command Center - Director Demo Packet

**Date:** February 19, 2026  
**Audience:** Agency Director and leadership stakeholders  
**Purpose:** One-document packet for soft demo delivery

---

## Packet Contents

1. One-Page Executive Brief
2. Verbatim Opening + Transitions Script
3. Q&A Answer Bank (Short/Medium/Long)
4. Fast Demo Checklist

---

## 1) One-Page Executive Brief

### What This Application Delivers
- A single operational view from report ingestion through case-line completion
- Controlled ingestion with duplicate-period protection and confirmation IDs (`ING-...`)
- Caseload-based routing that sends work to assigned Support Officers
- Row-level case processing for high-volume reports (50+ lines)
- KPI visibility for leadership and IT (productivity + support trends)

### Key Features (Updated Feb 2026)
- **Role-Based Access**: 5 distinct operational views
- **Command Center Visibility**: Program Officers see aggregated real-time stats from all units
- **Interactive Workload Management**: Director/Supervisor can instantly reassign caseloads
- **Safe Ingestion**: Duplicate protection and collapsible warning details
- **Row-Level Workflow**: Support Officers save progress row-by-row with pre-submission validation

### End-to-End Workflow (Current Build)
1. Program Officer ingests report (`.xlsx`, `.xls`, `.csv`) with metadata
2. System validates/normalizes and runs duplicate-period checks
3. System routes report workload by caseload assignment
4. Support Officer processes one case row at a time
5. Supervisor submission is gated until assigned rows are complete
6. Leadership and IT monitor KPI and ticket trend views

### KPI Model
- **Reports Worked**
- **Case Lines Worked**
- **Case Lines Completed**
- **Throughput (7d/30d)**

### Governance
- All roles can submit support tickets
- Director/Program Officer/Supervisor/IT can analyze Ticket KPI dashboards
- IT maintains verification and log entries

### Supported Roles (Leadership Talking Point)
- The app supports five roles with distinct capability views:
  - Director
  - Program Officer
  - Supervisor
  - Support Officer
  - IT Administrator

### Next Phase
- Persistent storage for durable audit/report history
- Enterprise authentication/authorization integration

---

## 2) Verbatim Opening + Transitions (Read-As-Is)

## 60-Second Opening
“Thank you for the time today. I’ll walk you through a soft demo of the OCSS Command Center and focus on one question: can this application improve operational control from intake to case completion?

This platform is built to manage report ingestion, route work by caseload, support row-level case processing, and provide leadership KPI visibility in real time.

What you’ll see today is not just file upload and dashboards. You’ll see process controls: ingestion confirmation IDs, duplicate-period checks, row-by-row workflow for high-volume reports, and support ticket analytics that leadership and IT can use for decision-making.

By the end of this walkthrough, you’ll see how this can reduce rework, improve accountability, and give us a clearer line of sight into team performance and operational risk.”

## Agenda Transition
“I’ll cover this in five quick sections: executive KPI view, controlled ingestion, support officer row-level processing, supervisor readiness checks, and leadership support-ticket analytics.”

## Section Transitions
- **To Director KPIs:** “I’ll start in the Director workspace to show what leadership can monitor at a glance.”
- **To Program Officer Ingestion:** “Next, I’ll show how reports enter the system safely and consistently.”
- **To Support Officer Workflow:** “Now I’ll show where case work happens row-by-row.”
- **To KPI Integrity:** “These KPI values come from the same row-level workflow data being processed live.”
- **To Ticket Governance:** “Finally, I’ll show issue governance and trend visibility for leadership and IT.”

## 45-Second Close
“To close, this demo shows a complete operating model: controlled ingestion, caseload-based routing, row-level case execution, supervisor readiness controls, and leadership/IT analytics. This gives us stronger operational discipline with better visibility and fewer blind spots. The current build is soft-demo ready, and the next maturity step is durable persistence plus enterprise authentication.”

---

## 3) Director Q&A Answer Bank

## Q: What problem does this solve today?
- **Short:** “It replaces fragmented report intake and manual tracking with one controlled workflow.”
- **Medium:** “It addresses intake control, workload visibility, and leadership oversight in one platform.”
- **Long:** “It standardizes ingestion, routing, row-level work, and KPI governance so operations and leadership stay aligned.”

## Q: How do we prevent duplicate monthly reports?
- **Short:** “The app blocks duplicate-period ingest by default.”
- **Medium:** “It checks type/frequency/period/caseload and content similarity before processing.”
- **Long:** “Duplicate-period and hash checks run pre-ingest; users must intentionally override duplicates.”

## Q: Can this handle 50+ line reports?
- **Short:** “Yes, each line is treated as an individual case.”
- **Medium:** “Support Officers process one row at a time and save row-level progress.”
- **Long:** “Submission is gated until assigned rows are complete, ensuring high-volume reports are worked safely and consistently.”

## Q: Are KPI numbers reliable?
- **Short:** “Yes, they come from row-level workflow data.”
- **Medium:** “Reports worked and case lines worked/completed are derived from actual processing activity.”
- **Long:** “KPI logic uses the same dataset as operational work, reducing reporting mismatch and manual rollup error.”

## Q: Can leadership monitor support issues?
- **Short:** “Yes, through Ticket KPI tabs with filters.”
- **Medium:** “Leadership and IT can analyze ticket trends by scope, category, priority, and date window.”
- **Long:** “All roles can submit tickets; governance views support rapid triage and pattern detection with IT verification.”

## Q: Is this production-ready?
- **Short:** “Soft-demo and pilot ready today; enterprise hardening next.”
- **Medium:** “Core workflow is implemented; add persistence and authentication for broad rollout.”
- **Long:** “The process model is operational now. Next phase adds durable storage, authN/authZ, and compliance-grade audit retention.”

---

## 4) Fast Demo Checklist (Use Right Before Meeting)

- App open and responsive at `http://localhost:8501`
- Role selector visible in sidebar
- Sample report available for ingest
- At least one Support Officer has assigned caseloads
- Ticket KPI tabs verified in Director and IT views
- 3-screen fallback prepared:
  1. Program Officer ingestion controls
  2. Support Officer row-level processing
  3. Director Ticket KPI analytics

---

## Related Documents
- [Director One-Page Brief](DIRECTOR_ONE_PAGE_BRIEF.md)
- [Director Opening + Transitions](DIRECTOR_OPENING_AND_TRANSITIONS.md)
- [Director Q&A Answer Bank](DIRECTOR_QA_ANSWER_BANK.md)
- [Director Soft Demo Script](DIRECTOR_SOFT_DEMO_SCRIPT.md)
