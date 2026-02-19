
# OCSS Establishment Command Center

![Deployment](https://img.shields.io/badge/deployment-internal%20server-blue)
![Framework](https://img.shields.io/badge/framework-streamlit-red)
![Status](https://img.shields.io/badge/status-production-green)

Internal Director Command Center Web Application for the Cuyahoga County Office of Child Support Services.

## Purpose
This repository contains the source code, governance documentation, and deployment materials for the
OCSS Establishment Command Center — a server‑hosted internal web application designed to:

- Centralize Excel report imports
- Standardize supervisor workflows
- Provide Director‑level KPI analytics
- Support CQI and SAVES governance alignment

## Technology Stack
This is a **Streamlit** web application built with Python.

## Production Hosting
⚠️ Production does NOT run from GitHub or Streamlit Cloud.

The live application runs internally from:

S:\OCSS\CommandCenter\App\

**Deployment Method:** Internal Windows Server (not Streamlit Cloud)

GitHub is used only for:
- Version control
- Documentation
- Update management

### Why Not Streamlit Cloud?
This application is hosted internally on a secure Windows server to:
- Maintain data privacy and security for sensitive child support information
- Operate within the County's network infrastructure
- Control access to internal staff only
- Comply with organizational IT policies

## Repository Structure
/app              → Application source code
/deploy           → Server deployment scripts
/docs/director    → Executive governance materials
/docs/it          → Technical deployment guidance

📘 **[Deployment Options Guide](docs/DEPLOYMENT_OPTIONS.md)** - Detailed information about deployment  
❓ **[FAQ](docs/FAQ.md)** - Frequently Asked Questions

## Quick Start
```bash
# Install dependencies
pip install -r app/requirements.txt

# Run locally
streamlit run app/app.py
```

Access at: http://localhost:8501

Generated: February 14, 2026
