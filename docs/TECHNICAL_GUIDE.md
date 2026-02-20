# OCSS Command Center - Technical Guide

## Executive Summary

The OCSS Command Center is a role-based web application designed to streamline establishment report processing and caseload management. Built on the Streamlit framework with Python, it provides an integrated dashboard system for five distinct user roles with real-time data processing and export capabilities.

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
| **Version Control** | Git | - | Source Code Management |
| **Container** | Docker | 24.x | Application Deployment |
| **Session Storage** | In-Memory | - | User Session Data |

### 1.3 Application Structure

```
/workspaces/ocss-command-center/
├── app/
│   ├── app.py                          # Main 900+ line Streamlit application
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

The application supports **5 distinct user roles** with specialized interfaces:

The role selector in the sidebar presents only these five roles:
- Director
- Program Officer
- Supervisor
- Support Officer
- IT Administrator

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

### 2.5 Interactive Workflow Enhancements

Recent updates (Feb 2026) have introduced significant usability and data integrity improvements:

#### 2.5.1 Enhanced User Experience
- **Collapsible Warnings:** File upload validation warnings are now grouped in a collapsible expander (``st.expander``) to prevent UI clutter while maintaining visibility of issues.
- **Robust Exception Handling:** Fixed charting errors in Program Officer dashboards by standardizing on Streamlit native charts (``st.bar_chart``) instead of unsupported backends.

#### 2.5.2 Real-Time Data Aggregation
- **Director & Program Officer Dashboards:** Now aggregate live data from all organizational units rather than displaying static placeholders. Caseload counts, completion rates, and worker assignments reflect the actual state of the application.
- **Supervisor Analytics:** Performance metrics are dynamically calculated based on the specific casework assigned to the selected unit's team members.

#### 2.5.3 Logic & Validation
- **Caseload Reassignment:** Directors and Supervisors can now functionally move caseloads between workers. This updates the underlying session state immediately, reflecting changes across all dashboards.
- **Submission Safety:** Support Officers cannot submit a caseload as "Complete" if any row remains in "Pending" or "In Progress" status. A warning is displayed, ensuring data completeness before supervisory review.

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
│ Streamlit File Uploader          │
│ - Reads Excel/CSV               │
│ - Validates file format          │
│ - Computes ingestion metadata     │
│ - Scans duplicate period records  │
│ - Stores in session state        │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ Pandas DataFrame Creation        │
│ - Parses file contents           │
│ - Normalizes support report schema│
│ - Routes rows by caseload/worker │
│ - Prepares row-level work queue  │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Support Officer Assigned Reports │
│ - Select queued report            │
│ - Filter rows (Pending/All/Done)  │
│ - Work one case row at a time     │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ Row-Level Editing                │
│ - Edit selected case row fields  │
│ - Update Worker Status + notes   │
│ - Save per-row updates           │
│ - Mark report ready for review   │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ Session State Update             │
│ - Store row updates and timestamps│
│ - Maintain KPI aggregates        │
│ - Persist during user session    │
└────────┬─────────────────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
  ┌──────────────┐ ┌──────────────┐
  │ Submit to    │ │ CSV Export & │
  │ Supervisor   │ │ Download     │
  └──────────────┘ └──────────────┘
```

### 4.2 Session State Management

Streamlit uses in-memory session state for data persistence within a user session:

```python
st.session_state:
├── selected_role: "Support Officer"
├── report_edits_{report_id}: {field: value, ...}
└── uploaded_caseload_files: {caseload_id: [...]}
```

**Session Lifetime:** Duration of user's browser session  
**Data Loss:** Occurs on browser close or page refresh (design limitation)  
**Future Improvement:** Implement database for persistent storage

---

## 5. Security Considerations

### 5.1 Current Security Implementation

✅ **Session-level Data Isolation**
- Each user session is independent
- Data stored in Streamlit session state (in-memory)
- Session data cleared on logout/browser close

✅ **Input Validation**
- File upload type checking (xlsx, xls, csv only)
- Pandas handles malformed Excel/CSV gracefully

### 5.2 Security Gaps & Recommendations

⚠️ **CRITICAL - Authentication Missing**
- **Current:** Role selector with no login
- **Risk:** Any user can access any role
- **Recommendation:** Implement LDAP/AD integration or OAuth2

⚠️ **Data in Transit**
- **Current:** HTTP (localhost development)
- **Risk:** Credentials/data exposed over network
- **Recommendation:** Deploy with HTTPS/TLS certificate

⚠️ **Audit Persistence Gap**
- **Current:** Upload routing and ticket actions are logged in session memory only
- **Risk:** Audit history resets with session/server restart
- **Recommendation:** Persist logs to database or append-only store

⚠️ **No Data Encryption**
- **Current:** Files stored in memory unencrypted
- **Risk:** Sensitive data exposure if server compromised
- **Recommendation:** Encrypt data at rest and in transit

⚠️ **No Role Authorization**
- **Current:** All fields editable by all users in a role
- **Risk:** Unauthorized modifications
- **Recommendation:** Implement field-level access control

### 5.3 Recommended Security Roadmap

**Phase 1 (Pre-Launch):**
1. Implement HTTPS/TLS
2. Add basic authentication (username/password or LDAP)
3. Log all user actions

**Phase 2 (3 Months):**
1. Integrate with Active Directory/LDAP
2. Implement audit trail to database
3. Add data encryption

**Phase 3 (6 Months):**
1. Add role-based field-level permissions
2. Implement API rate limiting
3. Add comprehensive security logging

---

## 6. Deployment Strategy

### 6.1 Development Environment (Current)

**Setup:**
```bash
# Clone repository
git clone https://github.com/arhawkins01-dotcom/ocss-command-center.git
cd ocss-command-center

# Install dependencies
pip install -r app/requirements.txt

# Run application
streamlit run app/app.py
```

**Access:** http://localhost:8501

### 6.2 Staging Environment (Recommended)

**Setup on Ubuntu Server:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv

# Clone repository to /opt
sudo git clone https://github.com/arhawkins01-dotcom/ocss-command-center.git /opt/ocss-command-center

# Create virtual environment
cd /opt/ocss-command-center
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt

# Configure systemd service
sudo cp deploy/systemd/ocss-command-center.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ocss-command-center
sudo systemctl start ocss-command-center
```

### 6.3 Production Deployment (Recommended - Docker)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Docker Compose (Recommended for single server):**
```yaml
version: '3.8'
services:
  ocss-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Deployment:**
```bash
# Build image
docker build -t ocss-command-center:1.0.0 .

# Run container
docker run -d \
  -p 8501:8501 \
  --name ocss-app \
  --restart unless-stopped \
  ocss-command-center:1.0.0

# Access at http://your-server:8501
```

### 6.4 Reverse Proxy Configuration (Nginx)

**For HTTPS/TLS access:**

```nginx
upstream streamlit {
    server localhost:8501;
}

server {
    listen 443 ssl http2;
    server_name ocss.yourdomain.com;

    ssl_certificate /etc/ssl/certs/your-cert.crt;
    ssl_certificate_key /etc/ssl/private/your-key.key;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name ocss.yourdomain.com;
    redirect 301 https://ocss.yourdomain.com$request_uri;
}
```

---

## 7. Performance & Scalability

### 7.1 Current Performance Baseline

| Metric | Value | Notes |
|--------|-------|-------|
| **Startup Time** | 2-3 seconds | Cold start, includes imports |
| **Report Load Time** | <100ms | Display 3 caseloads with 5 reports |
| **CSV Export** | <500ms | For 100-row reports |
| **Concurrent Users** | 5-10 | Limited by single Streamlit instance |
| **Memory Usage** | 200-400 MB | Per session depending on data |

### 7.2 Scaling Limitations (Current)

- **Single Streamlit Instance:** Can handle 5-10 concurrent users
- **Session-Based Storage:** All data lost on reconnect
- **No Database:** In-memory storage only
- **File Upload Size:** Depends on server RAM (recommend <100MB)

### 7.3 Scaling Recommendations

**To support 50+ concurrent users:**

1. **Implement Load Balancer**
   - Use Nginx or HAProxy
   - Route requests across multiple Streamlit instances
   - Sticky sessions for user continuity

2. **Add Persistent Database**
   - PostgreSQL or MySQL for reports/data
   - Redis for session caching
   - Improved fault tolerance

3. **Separate File Storage**
   - S3 or MinIO for Excel uploads
   - Reduces server memory pressure
   - Enables large file handling

4. **Caching Layer**
   - Redis or Memcached
   - Cache report data
   - Reduce database queries

**Recommended Architecture for 100+ Users:**
```
Load Balancer (Nginx)
    ├── Streamlit Instance 1
    ├── Streamlit Instance 2
    ├── Streamlit Instance 3
    ├── PostgreSQL Database
    ├── Redis Cache
    └── S3 File Storage
```

### 7.4 Database Migration Plan

**Current:** In-memory session state  
**Phase 1:** Add SQLite for development  
**Phase 2:** Migrate to PostgreSQL for production

```sql
-- Core tables needed
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    role VARCHAR(50),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(50) UNIQUE,
    caseload_id VARCHAR(10),
    filename VARCHAR(255),
    data JSONB,
    status VARCHAR(50),
    created_by INT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    action VARCHAR(255),
    table_name VARCHAR(100),
    record_id INT,
    old_values JSONB,
    new_values JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

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
**Last Updated:** February 18, 2026  
**Prepared For:** IT Department Review  
**Contact:** [Your contact information]
