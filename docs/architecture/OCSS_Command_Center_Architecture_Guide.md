# OCSS Command Center
## Enterprise Architecture & Data Flow Documentation

**Project:** OCSS Command Center  
**Application Type:** Operational Workflow Governance Platform  
**Framework:** Python + Streamlit  
**Prepared For:** Cuyahoga County IT Department Review  
**Prepared By:** Ashombia R. Hawkins  
**Last Updated:** March 9, 2026

---

## 1. Enterprise System Architecture

### Architecture Overview

The OCSS Command Center is an internal operational governance tool designed to improve report workflow transparency, performance monitoring, and leadership oversight across OCSS units.

The system is designed as a web-based operational governance platform that enhances report workflow visibility, caseload management, and leadership analytics across OCSS operations. The system operates as a companion application, supporting operational oversight while maintaining official case data within existing authorized systems.

### Enterprise System Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│ OCSS USERS / CLIENT LAYER                                        │
│                                                                  │
│ Director | Deputy Director | Program Officers | Supervisors     │
│ Team Leads | Support Officers | Administrative Specialists      │
│                                                                  │
│ Access via Modern Web Browser (Chrome / Edge / Firefox)          │
└───────────────────────────────┬──────────────────────────────────┘
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
└───────────────────────────────┬──────────────────────────────────┘
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
        ┌──────────────────────────────┐ ┌────────────────────────┐
        │ REPORT PROCESSING            │ │ APPLICATION STATE      │
        │                              │ │                        │
        │ Pandas Data Engine           │ │ Persistent Storage     │
        │                              │ │                        │
        │ • Excel Parsing              │ │ • Organizational Config│
        │ • CSV Imports                │ │ • User Assignments     │
        │ • Row Processing             │ │ • Help Tickets         │
        │ • KPI Aggregation            │ │ • Alert Acknowledges   │
        │                              │ │                        │
        └────────────┬─────────────────┘ └────────────┬───────────┘
                     │                                │
                     ▼                                ▼
           ┌──────────────────────┐ ┌──────────────────────────┐
           │ FILE STORAGE         │ │ EXPORT SERVICES          │
           │                      │ │                          │
           │ Uploaded Reports     │ │ Excel Exports            │
           │ CSV Imports          │ │ Word Leadership Packets   │
           │ Processing Logs      │ │ CSV Downloads            │
           │                      │ │                          │
           └──────────┬───────────┘ └──────────┬───────────────┘
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

---

## 2. Enterprise Data Flow

### Data Flow Overview

The Command Center processes operational reports through a structured ingestion workflow that ensures reports are normalized, routed to the appropriate caseloads, processed by staff, and surfaced to leadership dashboards.

The system supports multiple operational reports including:
- 56RA reports
- P-S reports
- Locate reports
- Other approved Excel or CSV operational datasets

### Enterprise Data Flow Diagram

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

## 3. Plain-Language Explanation for IT Review

**Step 1: Source Report Intake**

The process starts when a Program Officer uploads an approved operational report, such as:
- 56RA
- P-S
- Locate
- Other approved Excel/CSV files

These files serve as the operational input for Command Center workflows.

**Step 2: Ingestion and Validation**

The application then:
- Identifies the report type
- Applies period metadata
- Checks for likely duplicates
- Creates an ingestion record
- Displays validation warnings

This creates a controlled intake point before staff begin processing.

**Step 3: Normalization and Routing**

The report normalization engine converts uploaded files into a standardized processing format. During this stage the system:
- Standardizes column structure
- Maps records to the expected schema
- Assigns report IDs
- Computes due dates
- Triggers escalation timing logic
- Routes work to the correct caseload

**Step 4: Staff Processing Workflow**

Support Officers and Team Leads then process work through the Assigned Reports workflow, using:
- Row-level progress tracking
- Narration templates
- Required-field guidance
- Report-type indicators
- Save-progress logic

This reduces completion errors and improves consistency.

**Step 5: Validation and QA**

Before completion, the system checks whether rows are still pending or incomplete. Completed work can then feed:
- QA sampling
- Supervisor review
- Compliance dashboards
- Leadership oversight metrics

**Step 6: Leadership and Export Outputs**

Leadership users can view:
- KPI dashboards
- Team performance metrics
- Caseload status
- QA/compliance indicators

They can also export data to:
- Excel
- Word
- CSV

**Step 7: Persistence Boundary**

A very important architecture point for IT:

The Command Center only persists limited administrative state, such as:
- Organizational configuration
- Ticket records
- Acknowledgements

It is not the official system of record for child support case data.

---

## 4. Architectural Principle

The OCSS Command Center is designed as a **Workflow Governance Platform** that improves:
- Report workflow transparency
- Operational coordination
- Leadership oversight
- Performance analytics

While ensuring that official case records remain within the authorized child support systems.

---

## 5. Data Model Description

The OCSS Command Center processes operational case data from established OCSS report types:

| Caseload ID | Unit Assignment | Report Types |
|-------------|-----------------|--------------------:|
| 181000 | Downtown Establishment | 56RA / P-S / Locate |
| 181001 | Midtown Enforcement | 56RA / P-S / Locate |
| 181002 | Uptown Collections | 56RA / P-S / Locate |

Report data is normalized against OCSE 157 performance measures and SETS reporting requirements. Processing occurs during active user sessions; no case-level data is persisted within the platform database.

## 6. Data Security Model

The application does not persist case-level data within the platform database.

**Operational model:**
- Source reports originate from existing OCSS systems
- Data is processed in-memory during active user sessions
- Only organizational configuration and support tickets are persisted to disk
- All official case records remain within the authorized state child support systems

This design ensures that the Command Center functions as a workflow management and reporting companion, not a system of record.

## 7. Authentication & Access Control

The application supports three authentication modes:

| Mode | Purpose |
|------|---------|
| none | Development / testing environments |
| secrets | Credential-based login |
| header | Single Sign-On integration via reverse proxy |

**Production deployments should use Header Authentication Mode**, allowing integration with the county identity provider.

User roles are enforced through application-level role-based access control, with eight defined roles spanning Leadership, Management, Program/CQI, Administrative, and Support functions.

## 8. Infrastructure Impact

The OCSS Command Center is designed to operate within the existing county server infrastructure.

The application requires:
- One internal application server
- No external cloud dependencies
- Standard HTTPS reverse proxy configuration
- Integration with existing authentication systems (SSO header mode)

This minimizes infrastructure impact and aligns with county IT governance practices.

## 9. Intended Deployment Model

The application is intended to run within the county IT environment using:
- Internal application server
- HTTPS reverse proxy
- Secure authentication integration

This approach allows the system to integrate with existing county infrastructure while minimizing operational risk.

---

## 10. Authoritative Data Boundary

The OCSS Command Center enhances workflow coordination, processing visibility, and operational oversight. Official child support case records and authoritative case actions remain governed by existing authorized agency systems, including SETS and OnBase.

---

## Recommended Next Step

Approval is requested to deploy the OCSS Command Center in a county IT staging environment for pilot testing.

The pilot will allow:
- Infrastructure validation
- Authentication integration
- Limited user testing within OCSS units

Following successful pilot validation, the system can proceed to controlled production deployment.

---

**Document Version:** 1.1  
**Distribution:** Cuyahoga County IT Department Review  
**Classification:** Internal Use  
**Last Updated:** March 9, 2026
