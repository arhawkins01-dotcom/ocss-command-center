
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

### Deploy to Streamlit Cloud
**GitHub URL:** https://github.com/arhawkins01-dotcom/ocss-command-center

👉 **[See Streamlit Cloud Deployment Guide](STREAMLIT_CLOUD_DEPLOYMENT.md)** for step-by-step instructions.

### Local Development
```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```

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
