
# OCSS Command Center

**Operational Workflow Governance Platform for Cuyahoga County Office of Child Support Services**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-County%20Internal-green.svg)]()

---

## Overview

The **OCSS Command Center** is an internal operational governance platform designed to improve report workflow transparency, performance monitoring, and leadership oversight across OCSS units.

Built with Python and Streamlit, the system operates as a companion application that enhances workflow visibility and operational governance while maintaining official case data within existing authorized systems (SETS, OnBase).

### Key Capabilities

- **Report Workflow Management** - Centralized ingestion and processing of 56RA, P-S, and Locate reports
- **Caseload Oversight** - Unit-based work queue routing and assignment tracking
- **Leadership Analytics** - Real-time KPI dashboards for Director and Program Officer visibility
- **QA & Compliance** - Automated quality assurance with Ohio OAC/ORC/OCSE compliance criteria
- **Help Ticket Center** - Internal issue tracking and resolution workflow
- **Knowledge Base** - Embedded technical documentation and user guides

---

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run application
./scripts/start_app.sh
```

### County-Hosted Deployment

For internal production deployment to county infrastructure:

- **IT Deployment Guide:** [docs/it/IT_IMPLEMENTATION_GUIDE.md](docs/it/IT_IMPLEMENTATION_GUIDE.md)
- **Security Overview:** [docs/it/SECURITY_AND_DEPLOYMENT_BRIEF.md](docs/it/SECURITY_AND_DEPLOYMENT_BRIEF.md)
- **Windows Deployment:** [deploy/windows/](deploy/windows/)

---

## Documentation

### For IT & Technical Staff

- **[Enterprise Architecture Guide](docs/architecture/OCSS_Command_Center_Architecture_Guide.md)** - Complete system architecture and data flow
- **[System Architecture Diagram](docs/architecture/architecture_diagram.md)** - Visual system architecture
- **[Data Flow Diagram](docs/architecture/data_flow_diagram.md)** - End-to-end data processing flow
- **[IT Implementation Guide](docs/it/IT_IMPLEMENTATION_GUIDE.md)** - Deployment instructions
- **[Security & Deployment Brief](docs/it/SECURITY_AND_DEPLOYMENT_BRIEF.md)** - Security model and infrastructure requirements

### For Leadership & Directors

- **[Executive Summary](docs/director/EXECUTIVE_SUMMARY.md)** - High-level business case and benefits
- **[Director Overview](docs/director/README_DIRECTOR_OVERVIEW.md)** - Leadership role and capabilities
- **[Command Center Brief](docs/director/DIRECTOR_ONE_PAGE_BRIEF.md)** - One-page executive brief

### For End Users

- **[User Manual](docs/user_manual/USER_MANUAL.md)** - Complete end-user documentation
- **[Technical Guide](docs/user_manual/TECHNICAL_GUIDE.md)** - Detailed system functionality
- **[QA System Guide](docs/training/QA_COMPLIANCE_SYSTEM_COMPLETE.md)** - Quality assurance workflows

---

## Repository Structure

```
ocss-command-center/
│
├── app/                    # Application source code
│   ├── app.py             # Main Streamlit application
│   ├── auth.py            # Authentication module
│   ├── report_engine.py   # Report processing engine
│   └── requirements.txt   # Python dependencies
│
├── docs/                   # Documentation
│   ├── architecture/      # System architecture & diagrams
│   ├── director/          # Executive governance materials
│   ├── it/                # IT deployment & security guides
│   ├── user_manual/       # End-user documentation
│   └── training/          # Training & QA materials
│
├── deploy/                 # Deployment configurations
│   ├── docker/            # Docker deployment (future)
│   ├── nginx/             # Reverse proxy configs (future)
│   └── windows/           # Windows server deployment
│
├── data/                   # Runtime data
│   ├── knowledge_base/    # In-app documentation
│   ├── state/             # Application state files
│   └── sample_reports/    # Sample data for testing
│
├── exports/                # Generated reports
├── logs/                   # Application logs
└── tests/                  # Automated tests
```

---

## Technology Stack

- **Framework:** Python 3.9+ with Streamlit 1.x
- **Data Processing:** Pandas
- **Authentication:** County SSO header mode (production) | No-auth testing mode (development)
- **Deployment:** County-hosted internal application server
- **Database:** File-based persistence (JSON)

---

## System Boundaries

### What the Command Center Provides

- Operational workflow visibility and governance
- Report processing and caseload assignment
- Leadership KPI dashboards and analytics
- QA compliance tracking and metrics

### What Remains in Official Systems of Record

- **SETS Child Support System** - Official case records
- **Hyland OnBase** - Case documentation
- **ODJFS Infrastructure** - State reporting data

The Command Center operates as a **companion governance platform**, not a replacement for authorized case management systems.

---

## Deployment Model

### Production Environment

- **Hosting:** County-hosted internal application server
- **Network:** Internal county network only (no external internet exposure)
- **Authentication:** SSO header mode integration with county authentication infrastructure
- **Persistence:** File-based storage (organizational config, help tickets, alert acknowledgments)

### Development Environment

- **Local Development:** No-auth testing mode for development and validation
- **Demo Environment:** Streamlit Cloud for demonstrations (see [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md))

---

## Latest Release: v1.4.0

### New Features

- **Automated QA System** - 5-case sampling per worker with Ohio compliance criteria
- **Enhanced Role-Based Access** - Simplified role picker with last-role memory
- **Administrative Specialist Workflow** - Dedicated intake and ticket management interface
- **Improved Support Officer UI** - Enhanced caseload dashboard with progress tracking

**[See What's Included Guide](WHATS_INCLUDED.md)** for complete feature list.

---

## Support & Contact

**Project Lead:** Ashombia R. Hawkins  
**Organization:** Cuyahoga County Office of Child Support Services  
**For IT Questions:** See [docs/it/README_IT_DEPLOYMENT.md](docs/it/README_IT_DEPLOYMENT.md)

---

**Last Updated:** March 9, 2026  
**Version:** 1.4.0  
**Status:** Ready for IT Review
