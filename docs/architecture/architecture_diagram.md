# OCSS Command Center - Enterprise System Architecture

**Version:** 1.1  
**Last Updated:** March 9, 2026

## System Architecture Overview

The OCSS Command Center is an internal operational governance tool designed to improve report workflow transparency, performance monitoring, and leadership oversight across OCSS units.

The system operates as a web-based operational governance platform that enhances report workflow visibility, caseload management, and leadership analytics. It functions as a companion application, supporting operational oversight while maintaining official case data within existing authorized systems.

---

## Enterprise System Architecture Diagram

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

## Key Architectural Components

### 1. Client Layer
Modern web browsers accessing the application via HTTPS. Supports all major operational roles from Director to Support Officers.

### 2. Authentication & Security Layer
County-managed reverse proxy (NGINX) providing SSL/TLS encryption, Single Sign-On integration, and security filtering.

### 3. Application Layer
Python + Streamlit web application with role-based access control, report processing, dashboards, and knowledge base.

### 4. Data Processing Layer
Pandas-based engine for Excel/CSV parsing, data normalization, and KPI aggregation.

### 5. Persistence Layer
Limited persistent storage for organizational configuration, user assignments, help tickets, and alert acknowledgments.

### 6. Integration Layer
Interfaces with existing OCSS systems (SETS, OnBase, ODJFS) as a companion governance platform, not a replacement system of record.

---

## Deployment Model

- **Hosting:** County-hosted internal application server
- **Network:** Internal county network only (no external internet exposure)
- **Authentication:** SSO header mode integration with county authentication infrastructure
- **Database:** File-based persistence (no external database server required)
- **Dependencies:** Python 3.x runtime, standard application libraries

---

**For complete technical documentation, see:**
- [OCSS_Command_Center_Architecture_Guide.md](./OCSS_Command_Center_Architecture_Guide.md)
- [Data Flow Diagram](./data_flow_diagram.md)
