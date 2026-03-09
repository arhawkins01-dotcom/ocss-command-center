# OCSS Command Center - Enterprise Data Flow

**Version:** 1.1  
**Last Updated:** March 9, 2026

## Data Flow Overview

The Command Center processes operational reports through a structured ingestion workflow that ensures reports are normalized, routed to the appropriate caseloads, processed by staff, and surfaced to leadership dashboards.

### Supported Report Types
- **56RA reports** - Primary operational case reports
- **P-S reports** - Paternity and support reports
- **Locate reports** - Case location tracking
- **Other approved Excel or CSV operational datasets**

---

## Enterprise Data Flow Diagram

```text
┌──────────────────────────────────────────────────────────────────────┐
│ SOURCE REPORT / INPUT LAYER                                          │
│                                                                      │
│ ODJFS / OCSS Operational Reports                                     │
│                                                                      │
│ • 56RA Report                                                        │
│ • P-S Report                                                        │
│ • Locate Report                                                     │
│ • Other approved Excel / CSV files                                  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ Upload / Import
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ PROGRAM OFFICER INGESTION WORKFLOW                                   │
│                                                                      │
│ Upload & Processing Module                                           │
│                                                                      │
│ • File selection                                                     │
│ • Report-type identification                                         │
│ • Period metadata assignment                                         │
│ • Duplicate detection                                                │
│ • Ingestion registry creation                                        │
│ • Initial validation warnings                                        │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ REPORT NORMALIZATION ENGINE                                           │
│                                                                      │
│ Python / Pandas Processing                                           │
│                                                                      │
│ • Parse Excel / CSV structure                                        │
│ • Normalize column names                                             │
│ • Map rows to report schema                                          │
│ • Assign report identifiers                                          │
│ • Compute due-date clocks                                            │
│ • Compute escalation timing windows                                  │
│ • Route report to assigned caseload                                  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
               ┌────────────────┼────────────────┐
               │                │                │
               ▼                ▼                ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────────┐
│ CASELOAD ASSIGNMENT │ │ ALERTS ENGINE   │ │ INGESTION AUDIT LAYER   │
│                     │ │                 │ │                         │
│ • Unit ownership    │ │ • Due soon      │ │ • Upload timestamp      │
│ • Worker assignment │ │ • Overdue       │ │ • Source file name      │
│ • Team lead views   │ │ • Escalations   │ │ • Content hash          │
│ • Work queue routing│ │ • Acknowledges  │ │ • Ingestion ID          │
└───────────┬─────────┘ └────────┬────────┘ └────────────┬────────────┘
            │                    │                       │
            └──────────────┬─────┴───────────────┬───────┘
                           │                     │
                           ▼                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ SUPPORT OFFICER / TEAM LEAD PROCESSING                               │
│                                                                      │
│ Assigned Reports Workflow                                            │
│                                                                      │
│ • Caseload-based report queue                                        │
│ • Row-by-row processing                                              │
│ • Required-field guidance                                            │
│ • Report-type badges                                                 │
│ • Narration templates                                                │
│ • Row progress indicators                                            │
│ • Save progress                                                      │
│ • Submit completed work                                              │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ VALIDATION & QUALITY CONTROL                                          │
│                                                                      │
│ • Prevent incomplete submission                                       │
│ • Identify pending rows                                               │
│ • Trigger QA sampling                                                 │
│ • Route completed caseloads for supervisor review                     │
│ • Feed QA / compliance dashboards                                     │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
               ┌────────────────┼────────────────┐
               │                │                │
               ▼                ▼                ▼
┌─────────────────────┐ ┌──────────────────┐ ┌────────────────────────┐
│ LEADERSHIP METRICS  │ │ EXPORT SERVICES  │ │ SUPPORT TICKET CENTER  │
│                     │ │                  │ │                        │
│ • KPI dashboards    │ │ • Excel exports  │ │ • Issue intake         │
│ • Team performance  │ │ • Word packets   │ │ • Auto-routing         │
│ • Caseload status   │ │ • CSV downloads  │ │ • Ticket tracking      │
│ • Throughput views  │ │                  │ │ • Ticket KPIs          │
└───────────┬─────────┘ └────────┬─────────┘ └────────────┬───────────┘
            │                    │                        │
            └──────────────┬─────┴──────────────┬─────────┘
                           │                    │
                           ▼                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│ LIMITED PERSISTENCE / SYSTEM STATE                                   │
│                                                                      │
│ Persisted to Disk                                                    │
│                                                                      │
│ • Organizational configuration                                       │
│ • Caseload assignments                                               │
│ • Help tickets                                                       │
│ • Alert acknowledgements                                             │
│                                                                      │
│ Session-Based Workflow Data                                          │
│                                                                      │
│ • Active report work                                                 │
│ • Row processing state                                               │
│ • Temporary workflow data                                            │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ OFFICIAL OCSS / STATE SYSTEMS OF RECORD                              │
│                                                                      │
│ • SETS Child Support System                                          │
│ • Hyland OnBase                                                      │
│ • ODJFS reporting infrastructure                                     │
│                                                                      │
│ The Command Center provides workflow visibility and operational      │
│ governance but does not replace official case management systems.    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Stages

### 1. Report Ingestion
Program Officers upload operational reports (Excel/CSV) with metadata including report type, period, and caseload assignment.

### 2. Normalization & Processing
Pandas engine parses files, normalizes data structure, computes due dates, and routes to appropriate caseloads.

### 3. Caseload Assignment & Alerts
Reports are assigned to units and workers. Alert engine monitors due dates and generates escalation notifications.

### 4. Staff Processing
Support Officers and Team Leads process assigned reports row-by-row with guided workflows and progress tracking.

### 5. Quality Control
Validation engine prevents incomplete submissions, triggers QA sampling, and routes work to supervisors.

### 6. Leadership Analytics
Completed work feeds KPI dashboards, performance metrics, and leadership reporting views.

### 7. Persistence Model
- **Persistent Storage:** Org config, caseload assignments, help tickets, alert acknowledgments
- **Session-Based:** Active report processing, temporary workflow state
- **Systems of Record:** Official case data remains in SETS and OnBase

---

## Data Security Boundaries

### What the Command Center Stores
- Organizational configuration and caseload assignments
- Help ticket tracking and alert acknowledgments
- Temporary session data for active report processing

### What Remains in Official Systems
- Official case records (SETS Child Support System)
- Case documentation (Hyland OnBase)
- State reporting data (ODJFS infrastructure)

The Command Center operates as a **workflow governance companion**, not a system of record. It provides operational visibility without duplicating or replacing authorized case management systems.

---

**For complete technical documentation, see:**
- [OCSS_Command_Center_Architecture_Guide.md](./OCSS_Command_Center_Architecture_Guide.md)
- [System Architecture Diagram](./architecture_diagram.md)
