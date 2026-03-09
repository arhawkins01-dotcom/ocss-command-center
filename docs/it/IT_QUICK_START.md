# OCSS Command Center - Quick Start for IT Team

## Access Instructions

### Current Development Environment

**Status:** Application Running ✅

**Access URL:** 
```
http://localhost:8501
```

**For Network Access (from other computers on your network):**
```
http://[YOUR-IP-ADDRESS]:8501
```

Example if host IP is 192.168.1.25:
```
http://192.168.1.25:8501
```

---

## What You're Looking At

### Demo Users (No Authentication in v1.0)

Select any role from the sidebar to test:

| Role | Purpose | Key Features |
|------|---------|--------------|
| **Director** | Executive oversight | KPIs, team workload, performance analytics |
| **Program Officer** | Report upload & management | File upload, processing monitoring |
| **Supervisor** | Team management | Staff workload, individual performance |
| **Support Officer** ⭐ | Primary processor | Caseload dashboard, report editing, CSV export |
| **IT Administrator** | System management | Health monitoring, user/caseload assignment |

---

## Test Scenarios

### Scenario 1: Basic Report Processing (5 minutes)

1. Select **Support Officer** from sidebar
2. Click **Tab 1: Caseload Dashboard**
3. Select Caseload **181000 - Downtown Establishment**
4. Click the first report expander to view details
5. Edit a field (e.g., change "Total Students" from 245 to 250)
6. Click **💾 Update Report** button
7. Click **📥 Download CSV** to export

### Scenario 2: Program Officer Upload (5 minutes)

1. Select **Program Officer** from sidebar
2. Click **Tab 1: Upload & Processing**
3. Upload a sample file and set metadata:
   - Report Type (expanded list includes Financial, Compliance, QA, Policy, and Training types)
   - Frequency and reporting period
   - Owning Department
4. Click **Process Report** and verify ingestion confirmation ID (`ING-...`)
5. Confirm duplicate-period scanning behavior

### Scenario 3: Director Dashboard (3 minutes)

1. Select **Director** from sidebar
2. Review **Tab 1: KPIs** for metrics
3. Check **Tab 2: Caseload Management** for worker assignments
4. View **Tab 3: Team Performance** analytics

---

## Key Observations for IT Review

### Technology Stack
- **Framework:** Streamlit (Python)
- **Dependencies:** pandas, openpyxl (see `app/requirements.txt`)
- **Architecture:** Single-page web application
- **Port:** 8501 (default Streamlit)

### Data Flow
1. Reports organized by **Caseload Number** (181000, 181001, 181002)
2. Ingestion captures metadata (report type, frequency, period, owning department)
3. Duplicate-period and hash checks run before ingest
4. Support Officers process assigned report rows one case-line at a time
5. KPI tracking reflects reports worked and case-lines worked/completed
6. Export as CSV with one-click download

### Current Limitations (v1.0)
- ⚠️ No user authentication (role selector is open)
- ⚠️ No persistent database (data lost on refresh)
- ⚠️ Single Streamlit instance (5-10 concurrent users max)
- ✅ Session-based data isolation

---

## Environment Details

**Repository:** https://github.com/arhawkins01-dotcom/ocss-command-center

**File Structure:**
```
/workspaces/ocss-command-center/
├── app/
│   ├── app.py                    # Main application (900 lines)
│   ├── requirements.txt          # Python dependencies
│   └── report_utils.py           # Utilities
├── docs/
│   ├── TECHNICAL_GUIDE.md        # Full technical documentation
│   ├── IT_IMPLEMENTATION_GUIDE.md # Deployment procedures
│   ├── EXECUTIVE_SUMMARY.md      # Business case & ROI
│   └── README_IT_DEPLOYMENT.md   # IT quick reference
└── deploy/
    └── windows/
        └── Start-App.ps1         # Windows launcher
```

---

## Next Steps for IT

1. **Review Documentation:**
   - Read `TECHNICAL_GUIDE.md` for architecture details
   - Review `IT_IMPLEMENTATION_GUIDE.md` for deployment options
   - Check `EXECUTIVE_SUMMARY.md` for business justification

2. **Staging Environment Setup:**
   - Deploy to staging server (see IT_IMPLEMENTATION_GUIDE.md)
   - Test with load simulation
   - Configure Nginx reverse proxy
   - Set up SSL/TLS

3. **Security Assessment:**
   - Review pre-launch security requirements
   - Plan authentication integration (LDAP/AD)
   - Configure firewall and access controls
   - Set up monitoring and alerting

4. **Questions to Consider:**
   - Can we provide a 4-core/8GB server?
   - Should authentication be LDAP or other method?
   - Timeline for production launch?
   - Support model for post-launch?

---

## Command Reference

**Start/Stop Application:**
```bash
# Application is running via systemd or manual startup

# View running status
ps aux | grep streamlit

# View logs
journalctl -u ocss-command-center -f

# Kill process (if needed)
pkill -f "streamlit run"
```

**Install Dependencies Locally:**
```bash
cd /workspaces/ocss-command-center
pip install -r app/requirements.txt
streamlit run app/app.py
```

---

## Support

- **For questions about the application:** See documentation files
- **For deployment help:** Contact development team
- **For technical specifications:** Review TECHNICAL_GUIDE.md
- **For IT concerns:** Reference IT_IMPLEMENTATION_GUIDE.md

---

**Document Version:** 1.0  
**Application Version:** v1.0.0  
**Date:** February 18, 2026
