
# OCSS Establishment Command Center

Internal Director Command Center Web Application for the Cuyahoga County Office of Child Support Services.

## Purpose
This repository contains the source code, governance documentation, and deployment materials for the
OCSS Establishment Command Center — a server‑hosted internal web application designed to:

- Centralize Excel report imports
- Standardize supervisor workflows
- Provide Director‑level KPI analytics
- Support CQI and SAVES governance alignment

## 🚀 Quick Start

### ✅ Latest Enhancements Included (v1.3.0)

**👉 [See What's Included Guide](WHATS_INCLUDED.md)** - Complete list of all features already in the Streamlit app!

Recent updates now in this repo include:
- Simplified role picker (`Role Group` + `Select Your Role`) with last-role default.
- Program Officer retained on legacy dashboard with agency-wide filters (Department, Unit, Support Staff) synced across KPI/Caseload/Performance tabs.
- Administrative specialist workflow split from Support Officer caseload dashboard (intake + tickets + KB).
- Updated manuals/technical guides in both `docs/` and `data/knowledge_base/`.

### Deploy to Streamlit Cloud
**GitHub URL:** https://github.com/arhawkins01-dotcom/ocss-command-center
**Main file path:** `app/app.py` ⭐

👉 **[See Streamlit Cloud Deployment Guide](STREAMLIT_CLOUD_DEPLOYMENT.md)** for step-by-step instructions.

📂 **[Main File Path Visual Guide](MAIN_FILE_PATH.md)** - Clear explanation of the correct path

### Local Development
```bash
pip install -r app/requirements.txt
./scripts/start_app.sh
```

### IT + Developer Demo Prep

- Runbook: `docs/IT_DEVELOPER_DEMO_RUNBOOK.md`
- Day-of checklist: `docs/DEMO_DAY_CHECKLIST.md`
- Preflight: `./scripts/demo_preflight.sh`

### QA & Compliance System

**New in v1.4.0:** Automated Quality Assurance with Ohio OAC/ORC/OCSE compliance tracking

- **Auto-sampling:** 5 cases per worker per report (automatic on submission)
- **Supervisors:** QA Review tab with Ohio compliance criteria
- **Executives:** QA & Compliance dashboard with agency-wide metrics
- **Documentation:** `docs/QA_COMPLIANCE_SYSTEM_COMPLETE.md`

**Key Features:**
- ✅ Ohio-specific compliance criteria (OAC 5101:12, ORC 3111.04, OCSE guidance)
- ✅ Automated case sampling (deterministic, reproducible)
- ✅ Real-time compliance scoring and trending
- ✅ Executive KPI integration for strategic oversight

## Production Hosting
⚠️ Production does NOT run from GitHub.

The live application runs internally from:

S:\OCSS\CommandCenter\App\

GitHub is used only for:
- Version control
- Documentation
- Update management

### Deployment Options

1. **Streamlit Cloud** (Web-based) - See [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md)
2. **Internal Server** (Windows) - See [deploy/DEPLOYMENT_GUIDE.md](deploy/DEPLOYMENT_GUIDE.md)

## Repository Structure
/app              → Application source code
/deploy           → Server deployment scripts
/docs/director    → Executive governance materials
/docs/it          → Technical deployment guidance

Generated: February 14, 2026

Last updated: March 3, 2026
