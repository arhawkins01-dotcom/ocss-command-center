
# OCSS Establishment Command Center

Internal Director Command Center Web Application for the Cuyahoga County Office of Child Support Services.

## 🚀 Quick Access

**Want to launch the application?** Choose your method:

> 📘 **New User?** See the [**QUICK_START.md**](./QUICK_START.md) guide for detailed step-by-step instructions!

### Option 1: One-Click Launch (Recommended)
- **Open:** [`LAUNCH.html`](./LAUNCH.html) in your browser for instant access
- Click "Launch Application" button to open the Command Center

### Option 2: Command Line Launch

**Windows (PowerShell):**
```powershell
.\deploy\windows\Start-App.ps1
```

**Linux/Mac:**
```bash
./deploy/start-app.sh
```

### Option 3: Direct Access
Once running, access the application at:
```
http://localhost:8501
```

---

## Purpose
This repository contains the source code, governance documentation, and deployment materials for the
OCSS Establishment Command Center — a server‑hosted internal web application designed to:

- Centralize Excel report imports
- Standardize supervisor workflows
- Provide Director‑level KPI analytics
- Support CQI and SAVES governance alignment

## Production Hosting
⚠️ Production does NOT run from GitHub.

The live application runs internally from:

S:\OCSS\CommandCenter\App\

GitHub is used only for:
- Version control
- Documentation
- Update management

## Repository Structure
/app              → Application source code
/deploy           → Server deployment scripts
/docs/director    → Executive governance materials
/docs/it          → Technical deployment guidance

Generated: February 14, 2026
