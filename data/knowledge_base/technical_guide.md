# OCSS Command Center — Technical Guide

Last Updated: 2026-03-02

---

## Executive Summary

The OCSS Command Center is a role-based web application designed to streamline establishment report processing and caseload management. Built on the Streamlit framework with Python, it provides an integrated dashboard system for multiple user roles with real-time data processing and export capabilities.

Key operational features implemented in Feb 2026 include:
- Escalation alerts with role-based timing windows and acknowledgements
- Report due-date clocks computed at upload time for monthly QA sources (56RA / P-S / Locate)
- Senior leadership exports in Excel and Word formats
- Help Ticket Center workflow with auto-routing/assignment and ticket KPI views
- Mixed persistence model: organizational configuration + help tickets persisted on disk; report/work data remains session-based

**Project Status:** Production-Ready (v1.0.0)  
**Framework:** Streamlit 1.x with Python 3.8+  
**Deployment:** Single-server containerized application  
**Target Launch:** Ready for IT Department Review

---

## 1. Technical Architecture

### 1.1 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser/Client Layer                      │
│              (Firefox, Chrome, Safari, Edge)                │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/HTTPS
┌────────────────▼────────────────────────────────────────────┐
│                  Streamlit Web Server                        │
│  Port: 8501 | Framework: Streamlit 1.x (Python)            │
│  - Session State Management                                  │
│  - Role-Based Access Control                                │
│  - Data Validation & Processing                             │
└────────────────┬────────────────────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼────┐  ┌───▼────┐  ┌───▼────┐
│ Pandas │  │ Excel  │  │ Session│
│DataFrame   │Files  │  │ State  │
│Processing  │(I/O)  │  │Storage │
└────────────┴───────┘  └────────┘
```

### 1.2 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Frontend Framework** | Streamlit | 1.x | Web UI & Dashboard |
| **Backend Language** | Python | 3.8+ | Business Logic |
| **Data Processing** | Pandas | Latest | DataFrames & Excel/CSV |
| **Excel Support** | openpyxl | Latest | Read/Write Excel Files |
| **Word Export** | python-docx | Latest | Generate leadership packets (.docx) |
| **Version Control** | Git | - | Source Code Management |
| **Container** | Docker | 24.x | Application Deployment |
| **Session Storage** | In-Memory | - | User Session Data |

### 1.3 Application Structure

```
/workspaces/ocss-command-center/
├── app/
│   ├── app.py                          # Main Streamlit application
│   ├── auth.py                         # Optional authentication modes (none/demo/secrets/header)
│   ├── report_utils.py                 # Utility functions (expandable)
│   └── requirements.txt                # Python dependencies
├── deploy/
│   ├── windows/
│   │   └── Start-App.ps1              # Windows launcher script
│   └── docker/                         # Docker configuration (to be added)
├── docs/
│   ├── TECHNICAL_GUIDE.md             # This document
│   ├── director/
│   │   └── README_DIRECTOR_OVERVIEW.md
│   └── it/
│       └── README_IT_DEPLOYMENT.md
├── README.md                           # Project overview
└── .git/                               # Version control (v1.0.0 tagged)
```

---

## 2. Core Features & Components

### 2.1 Role-Based Access Control

The application supports multiple roles with specialized interfaces. The UI may display expanded leadership and sub-role names (for example: Deputy Director, Department Manager, Senior Administrative Officer, Team Lead) which map to a smaller set of capability-backed views.

Roles commonly used in the UI:
- Director / Deputy Director
- Department Manager
- Senior Administrative Officer
- Program Officer
- Supervisor
- Team Lead
- Support Officer
- IT Administrator

**Note on Leadership Titles (Director role):**
The app keeps the sidebar role list to these five roles, but User Management supports leadership titles under the Director role via a **Unit Role** field:
- Director (only one allowed)
- Deputy Director
- Department Manager
- Senior Administrative Officer

Operational note: Senior Administrative Officer (SAO), Supervisor, and Program Officer often have similar operational needs (workload visibility, alerts, exports). The app supports both explicit roles and leadership titles (Unit Role) depending on deployment mode.

#### 1. **Director** 
- **Dashboard Tabs:** KPIs, Caseload Management, Team Performance, Report Intake, Ticket KPIs, Manage Users
- **Capabilities:** 
  - View organization-wide KPIs and metrics
  - Manage worker caseload assignments
  - Monitor team performance analytics
  - Reassign workloads across teams

#### 2. **Program Officer**
- **Dashboard Tabs:** Upload & Processing, Caseload Management, Ticket KPIs, Manage Users
- **Capabilities:**
  - Upload Excel/CSV reports
  - Rename and organize uploaded reports
  - Monitor processing status across all caseloads
  - Track team metrics for assigned reports

#### 3. **Supervisor**
- **Dashboard Tabs:** KPI Metrics, Team Caseload, Performance Analytics, Report Intake, Ticket KPIs, Manage Users
- **Capabilities:**
  - View team member workloads
  - Monitor individual worker performance
  - Track caseload metrics by team member
  - Review performance trends

**Worker Self-Pull (permissions):**
Worker Self-Pull is intentionally restricted to **Director / Program Officer** and the unit's **Support Officer Team Leads**.

#### 4. **Support Officer** ⭐ *Primary Report Processor*
- **Dashboard Tabs:** 
  - 📊 **Caseload Dashboard** - View reports by caseload number (181000, 181001, 181002)
  - 📝 **Assigned Reports** - Process and update report rows one case-line at a time
  - 🎫 **Support Tickets** - Manage support requests
  - 📚 **Knowledge Base** - Access FAQs and training materials
- **Capabilities:**
  - View Excel reports uploaded by Program Officer and routed by caseload assignment
  - Edit one case row at a time with row-level workflow status
  - **Save Progress:** Persist edits to session state without submitting
  - **Safe Submission:** Validation prevents submitting reports with incomplete ("Pending") rows
  - Track workload through reports-worked and case-lines-worked KPIs
  - Export processed reports as CSV
  - Download reports for offline processing

#### 5. **IT Administrator**
- **Dashboard Tabs:** System Status, User & Caseload Management, Maintenance & Logs, Ticket KPIs
- **Capabilities:**
  - Monitor system health and performance
  - Manage user and caseload assignments
  - Review system logs and audit trails
  - Perform maintenance operations

### 2.2 Caseload Structure

Reports are organized by **Caseload Numbers** (unique identifiers):

| Caseload ID | Name | Reports | Student Population |
|------------|------|---------|-------------------|
| **181000** | Downtown Elementary | 2 | 245 Students |
| **181001** | Midtown Middle School | 2 | 520 Students |
| **181002** | Uptown High School | 1 | 1200 Students |

### 2.3 Report Fields & Data Processing

Each report contains **7-9 editable fields** with automatic type detection:

**Example Report (181000-001):**
- Total Students: 245 (numeric, editable)
- Staff: 15 (numeric, editable)
- Classrooms: 12 (numeric, editable)
- Completion %: 85 (numeric, editable)
- Grade Levels: 3-5 (text, editable)
- Assessment Date: 2/15/2026 (text, editable)
- Quality Score: 94 (numeric, editable)

### 2.4 Data Export & Download

Support Officers can export reports in multiple formats:
- **CSV Download:** One-click CSV export from any report
- **Format:** Field-Value pairs for easy spreadsheet import
- **Batch Operations:** Download multiple reports as individual files

Senior leadership (Director / Program Officer / Supervisor) can also export executive briefing packets from live application state:
- **Excel (.xlsx):** Multi-sheet export (caseload status, alerts, assignments, ingestion/audit snapshots)
- **All Ingested Reports (sheet):** Consolidated view of all reports ingested via upload/import (built from the ingestion registry and upload audit log, with caseload ownership context)
- **Word (.docx):** Executive packet with summary sections and embedded tables

### 2.5 Interactive Workflow Enhancements

Recent updates (Feb 2026) have introduced significant usability and data integrity improvements:

#### 2.5.1 Enhanced User Experience
- **Collapsible Warnings:** File upload validation warnings are now grouped in a collapsible expander (``st.expander``) to prevent UI clutter while maintaining visibility of issues.
- **Robust Exception Handling:** Fixed charting errors in Program Officer dashboards by standardizing on Streamlit native charts (``st.bar_chart``) instead of unsupported backends.

#### 2.5.2 Real-Time Data Aggregation
- **Director & Program Officer Dashboards:** Now aggregate live data from all organizational units rather than displaying static placeholders. Caseload counts, completion rates, and worker assignments reflect the actual state of the application.
- **Supervisor Analytics:** Performance metrics are dynamically calculated based on the specific casework assigned to the selected unit's team members.

**Caseload Work Status (Real-Time):**
Director/Program Officer views include a caseload rollup table that combines assignment ownership with report-level workflow into one overall status: **Pending / Finished / Completed / Unassigned**.

#### 2.5.3 Logic & Validation
- **Caseload Reassignment:** Directors and Supervisors can now functionally move caseloads between workers. This updates the underlying session state immediately, reflecting changes across all dashboards.
- **Submission Safety:** Support Officers cannot submit a caseload as "Complete" if any row remains in "Pending" or "In Progress" status. A warning is displayed, ensuring data completeness before supervisory review.

**User Management (Unit Role column):**
User Management displays a derived **Unit Role** column:
- Support Officers: **Team Lead** vs **Support Officer** based on unit configuration
- Director role users: leadership title from the stored Unit Role (Director / Deputy Director / Department Manager / Senior Administrative Officer)

---

## 3. System Requirements

### 3.1 Server Environment

**Minimum Requirements:**
- **OS:** Ubuntu 22.04 LTS or later (Linux), Windows Server 2019+, or macOS 12+
- **CPU:** 2 cores minimum (4 cores recommended)
- **RAM:** 4 GB minimum (8 GB recommended)
- **Storage:** 20 GB minimum (SSD recommended for performance)
- **Network:** 1 Mbps minimum connection bandwidth

**Recommended Production Setup:**
- **OS:** Ubuntu 24.04 LTS (current in dev container)
- **CPU:** 4-8 cores
- **RAM:** 16 GB
- **Storage:** 100 GB SSD
- **Network:** 10+ Mbps connection

### 3.2 Client Environment

**Supported Browsers:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Client Requirements:**
- Modern web browser with JavaScript enabled
- Minimum 1024x768 screen resolution
- 2 MB/s connection speed

### 3.3 Python Dependencies

**Core Requirements:**
```
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.10.0
numpy>=1.24.0
python-docx>=1.1.2
```

**Development (Optional):**
- pytest >= 7.0 (for testing)
- black >= 23.0 (for code formatting)
- pylint >= 2.17.0 (for linting)

---

## 4. Data Flow Architecture

### 4.1 Report Processing Workflow

```
┌──────────────────┐
│ Program Officer  │
│  Ingest Report   │
│ (Excel/CSV +     │
│  period metadata)│
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────┐
OCSS Command Center — Technical Guide

Version: 1.1.0
Last Updated: 2026-02-27

---

This file mirrors the new User Manual structure and documents implementation, runtime behavior, seeding rules, deployment options, and developer notes.

Key locations:
- App entry: `app/app.py`
- KB seed sources: `docs/USER_MANUAL.md`, `docs/TECHNICAL_GUIDE.md`
- KB targets: `data/knowledge_base/user_guide.md`, `data/knowledge_base/technical_guide.md`
- Seed manifest: `data/knowledge_base/.seed_manifest.json`

### KB Admin behavior
- In-app editing persists to `data/knowledge_base/*.md` and sets `edited_by_admin: true` in the manifest. The seeder will not overwrite such files.

---

## Architecture & Data Flow (Developer View)

- Streamlit UI (`app/app.py`) orchestrates role routing and tab layout.
- Ingestion & parsing: `app/report_engine.py` and `app/report_utils.py` handle file parsing, normalization, and row mapping.
- KB seeding: `_kb_seed_docs()`, `_ensure_kb_seeded()` in `app/app.py`.
- Persistence: `data/state/ocss_app_state.json` (org config + help tickets), session state for row work, `exports/` for CSVs.

Report ingestion sequence (high level):
1. File selected in `Upload & Processing` → `streamlit.file_uploader` reads bytes.
2. `report_engine` normalizes into DataFrame and computes a content hash.
3. Duplicate candidates found via `find_duplicate_candidates()`.
4. Ingestion registry entry created with `ingestion_id` and stored in session for immediate processing and audit.

Important helpers:
- `_sha256_file(path)` — compute file hash used by manifest
- `_read_text_file(path)` — robust file read used by KB rendering
- `render_knowledge_base()` — presents KB and admin UI (download, upload, edit)

---

## Due-Date Logic & Alerts

- Due-date clock is computed at ingestion time by `_compute_due_at()` using `period` and `MONTHLY_QA_DUE_DAYS_BY_MONTH`.
- Alerts are derived from ingestion timestamps and `due_at`, and the escalation ladder maps ages to roles.
- Acknowledgements persist to `data/state/ocss_app_state.json` so leadership views can filter acknowledged items.

---

## Deployment & Runtime

Local development:
```bash
pip install -r app/requirements.txt
streamlit run app/app.py --server.enableCORS false --server.enableXsrfProtection false
```

Production recommendations:
- Run behind TLS-terminating reverse proxy (Nginx) and enable `OCSS_AUTH_MODE=header` for SSO.
- Containerize with Docker; mount `./data` for persisted KB and state.

Health & monitoring:
- Streamlit health endpoint available at `/_stcore/health` in container setups.
- Exported files and logs: `exports/` and `logs/` directories.

---

## Developer & Maintenance Notes

- To reseed KB from repo sources: update/delete the KB target in `data/knowledge_base/` or clear `edited_by_admin` in `.seed_manifest.json`, then restart the app.
- When updating `docs/` files, update the manifest `source_hash` if you need deterministic control; otherwise `_kb_seed_docs()` computes hashes automatically.
- Run `pytest -q` after code changes; unit tests focus on `report_utils` and `action_logic`.

End of Technical Guide

---

## 8. Maintenance & Operations

### 8.1 Regular Maintenance Tasks

**Daily:**
- Monitor application uptime
- Check error logs
- Verify database backups

**Weekly:**
- Review audit logs
- Check disk space usage
- Update dependencies (if patches available)

**Monthly:**
- Full application backup
- Performance review
- Security scan
- Update documentation

**Quarterly:**
- Major version updates
- Full system audit
- Disaster recovery drill
- Capacity planning

### 8.2 Backup & Recovery Strategy

**Backup Schedule:**
- **Files:** Daily incremental, weekly full (to S3)
- **Database:** Hourly incremental, daily full (to separate server)
- **Retention:** 30 days for incremental, 90 days for full

**Recovery Time Objectives (RTO):**
- File loss: 24 hours
- Database loss: 1 hour

**Recovery Testing:**
- Monthly restore drill
- Quarterly full system restore

### 8.3 Logging & Monitoring

**Application Logs:**
```bash
# Streamlit logs location (Docker)
docker logs ocss-app

# System logs
/var/log/ocss/application.log
/var/log/ocss/error.log
/var/log/ocss/audit.log
```

**Recommended Monitoring Tools:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Prometheus + Grafana
- Datadog or New Relic

**Key Metrics to Monitor:**
- Application uptime
- Response time (p50, p95, p99)
- User sessions active
- Memory usage
- CPU usage
- Error rate

---

## 9. Implementation Timeline

### Phase 1: Pre-Launch (Week 1-2)
- [ ] IT security review
- [ ] Network configuration (firewall rules)
- [ ] SSL certificate procurement
- [ ] Staging environment setup
- [ ] Performance testing

### Phase 2: Pilot Launch (Week 3-4)
- [ ] Limited user access (10-20 users)
- [ ] Collect feedback
- [ ] Monitor performance
- [ ] Bug fixes and improvements

### Phase 3: Full Production (Week 5-6)
- [ ] All staff access
- [ ] Training complete
- [ ] Support team ready
- [ ] Documentation complete

### Phase 4: Post-Launch (Ongoing)
- [ ] Collect usage metrics
- [ ] Plan enhancements
- [ ] Database migration (Month 2)
- [ ] Advanced features (Month 3)

---

## 10. Support & Documentation

### 10.1 Documentation Maintained

- **TECHNICAL_GUIDE.md** - This document (for IT/Technical staff)
- **README_DIRECTOR_OVERVIEW.md** - Director role guide
- **README_IT_DEPLOYMENT.md** - Deployment instructions
- **USER_MANUAL.md** - End user guide (to be created)
- **API_DOCUMENTATION.md** - For developers (to be created)

### 10.2 Support Structure

**Level 1 - User Support**
- Email support queue
- FAQ/Knowledge base
- In-app help tooltips

**Level 2 - Technical Support**
- Application troubleshooting
- Performance issues
- Data recovery

**Level 3 - Development Support**
- Bug fixes
- Feature enhancements
- Database issues

### 10.3 Contact Information

- **Project Lead:** [Your Name]
- **Technical Contact:** [IT Staff]
- **Support Email:** support@yourdomain.com
- **Emergency Contact:** [On-call number]

---

## 11. Risk Assessment

### 11.1 Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| Data loss on session timeout | High | Medium | Implement persistent database |
| Concurrent user limit exceeded | Medium | Medium | Add load balancing |
| File upload causes server crash | High | Low | Implement file size limits |
| Excel parsing errors | Medium | Low | Enhanced error handling |
| Session state memory leak | High | Low | Regular server restarts |

### 11.2 Operational Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| Insufficient IT support skills | Medium | Low | Comprehensive training |
| Network bandwidth issues | High | Low | Monitor and upgrade |
| Lack of data backups | High | Low | Automated daily backups |
| Security breach | High | Low | Security audit before launch |

---

## 12. Cost Estimation

### 12.1 Infrastructure Costs

| Item | Cost | Notes |
|------|------|-------|
| **Server (VM)** | $200-500/month | 4-core, 16GB RAM |
| **Database (if cloud)** | $100-300/month | PostgreSQL managed |
| **File Storage (S3)** | $20-50/month | 100GB storage |
| **SSL Certificate** | $50-100/year | Auto-renewal |
| **Monitoring Tools** | $100-200/month | Optional but recommended |
| **Backup Storage** | $30-50/month | Redundant backups |
| **Total Monthly** | **$450-1,200** | Varies by scale |

### 12.2 Development/Support Costs

| Item | Cost | Notes |
|------|------|-------|
| **Initial Setup** | $2,000-5,000 | One-time |
| **Pre-Launch Testing** | $1,000-2,000 | One-time |
| **Training & Documentation** | $1,000-3,000 | One-time |
| **Monthly Support** | $1,000-2,000 | Ongoing |
| **Quarterly Enhancements** | $3,000-5,000 | Per quarter |

---

## 13. Success Metrics

### 13.1 Business Metrics

- **User Adoption:** >80% of target users active by Month 2
- **Report Processing Time:** Reduced by 40% vs. manual
- **Error Rate:** <1% of processed reports
- **User Satisfaction:** >4.0/5.0 in surveys
- **Uptime:** >99% availability

### 13.2 Technical Metrics

- **Application Response Time:** <500ms (p95)
- **Server CPU Usage:** <75% average
- **Server Memory Usage:** <80% average
- **Error Rate:** <0.1% of requests
- **Backup Success Rate:** 100%

---

## Appendix A: Quick Reference

### A.1 Useful Commands

**Start Application:**
```bash
streamlit run /path/to/app.py
```

**Access Application:**
```
http://localhost:8501  # Development
https://ocss.yourdomain.com  # Production
```

**Check Dependencies:**
```bash
pip list | grep -E "streamlit|pandas|openpyxl"
```

**View Application Logs:**
```bash
docker logs -f ocss-app
journalctl -u ocss-command-center -f
```

### A.2 File Locations

```
Source Code:        /opt/ocss-command-center/app/app.py
Configuration:      /opt/ocss-command-center/app/config.py (planned)
Logs:               /var/log/ocss/
Database:           /var/lib/ocss/data.db (SQLite) or PostgreSQL
Backups:            /backup/ocss/ (local) or S3 (cloud)
```

### A.3 Port Information

| Service | Port | Protocol | Notes |
|---------|------|----------|-------|
| Streamlit App | 8501 | HTTP | Development only |
| Web App | 443 | HTTPS | Production |
| HTTP Redirect | 80 | HTTP | Redirects to 443 |
| Database | 5432 | TCP | PostgreSQL |
| Redis Cache | 6379 | TCP | Optional |

---

## Appendix B: Troubleshooting Guide

### Issue: Application won't start

**Symptoms:** `streamlit run app.py` fails

**Solutions:**
1. Check Python version: `python3 --version` (need 3.8+)
2. Verify dependencies: `pip install -r requirements.txt`
3. Check port availability: `lsof -i :8501`
4. Review error logs for specifics

### Issue: Slow report loading

**Symptoms:** Reports take >2 seconds to open

**Solutions:**
1. Check server resources: `top`, `free -m`, `df -h`
2. Reduce report data size
3. Implement caching for Excel parsing
4. Add database indexing (after DB migration)

### Issue: CSV export fails

**Symptoms:** Download button produces error

**Solutions:**
1. Verify Pandas installation: `python3 -c "import pandas"`
2. Check report data format
3. Ensure sufficient disk space
4. Review error logs

### Issue: Users losing data on disconnect

**Symptoms:** Report edits disappear after page refresh

**Solutions:**
1. This is expected (currently uses session state)
2. Workaround: Save/Download CSV before page close
3. Plan: Implement database persistence (Phase 2)

---

## Appendix C: Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-18 | Initial release - MVP with 5 roles |
| 1.1.0 | Planned | Database integration, authentication |
| 1.2.0 | Planned | Load balancing, improved security |
| 2.0.0 | Planned | API layer, advanced analytics |

---

## Conclusion

The OCSS Command Center is a well-architected, production-ready application built on proven technologies. With proper deployment and the recommended Phase-based implementation plan, it will provide significant value to your organization.

**Recommended Action:** Approve for staging environment deployment with target launch 4-6 weeks from IT approval.

---

**Document Version:** 1.0  
**Last Updated:** February 21, 2026  
**Prepared For:** IT Department Review  
**Contact:** [Your contact information]
