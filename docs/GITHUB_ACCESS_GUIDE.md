# OCSS Command Center - GitHub Access & Deployment Guide

## How to Access from GitHub

### **For Developers & IT Team**

#### **Step 1: Clone from GitHub**

```bash
# Clone the repository
git clone https://github.com/arhawkins01-dotcom/ocss-command-center.git

# Navigate to folder
cd ocss-command-center
```

#### **Step 2: Install Dependencies**

```bash
# Option A: Using pip
pip install -r app/requirements.txt

# Option B: Using virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r app/requirements.txt
```

#### **Step 3: Run the Application**

```bash
# Start Streamlit app
streamlit run app/app.py

# It will show:
# Local URL: http://localhost:8501
# Network URL: http://[your-ip]:8501
```

#### **Step 4: Open in Browser**

- **Local (your machine):** `http://localhost:8501`
- **From network:** `http://[your-ip]:8501`

---

## For End Users (After Production Deployment)

Once deployed to production, users won't use GitHub. They'll access via a **web URL**:

### **Access URLs (Production)**

| User Type | URL |
|-----------|-----|
| **Director** | `https://ocss.yourdomain.com` |
| **Program Officer** | `https://ocss.yourdomain.com` |
| **Support Officer** | `https://ocss.yourdomain.com` |
| **Supervisor** | `https://ocss.yourdomain.com` |
| **IT Admin** | `https://ocss.yourdomain.com` |

**Everyone uses the same URL**, then logs in with their credentials and gets their role-specific dashboard.

---

## Development vs. Production Access

### **During Development** (What You're Doing Now)
```
GitHub Clone → Run Locally → http://localhost:8501
```

### **In Production** (After IT Deployment)
```
Deployed Server → HTTPS URL → https://ocss.yourdomain.com
```

**Key Difference:** Production will have:
- ✅ Authentication login system
- ✅ HTTPS encryption
- ✅ Database backend
- ✅ No role selector (automatic based on login)
- ✅ Multiple users/sessions

---

## Complete Setup Instructions

### **Quick Start (5 minutes)**

```bash
# 1. Clone
git clone https://github.com/arhawkins01-dotcom/ocss-command-center.git
cd ocss-command-center

# 2. Install
pip install -r app/requirements.txt

# 3. Run
streamlit run app/app.py

# 4. Open browser
# http://localhost:8501
```

### **Production Deployment (see IT_IMPLEMENTATION_GUIDE.md)**

```bash
# 1. Clone to server
sudo git clone https://github.com/arhawkins01-dotcom/ocss-command-center.git /opt/ocss-command-center

# 2. Set up Docker
cd /opt/ocss-command-center
docker-compose up -d

# 3. Configure Nginx reverse proxy
# See IT_IMPLEMENTATION_GUIDE.md for full setup

# 4. Access via
# https://ocss.yourdomain.com
```

---

## Repository Structure

When you clone, you'll get:

```
ocss-command-center/
├── app/
│   ├── app.py                    # Main application (run this)
│   ├── requirements.txt          # Dependencies to install
│   └── report_utils.py           # Utilities
│
├── docs/
│   ├── TECHNICAL_GUIDE.md        # Full technical docs
│   ├── IT_IMPLEMENTATION_GUIDE.md # Production setup
│   ├── EXECUTIVE_SUMMARY.md      # Business case
│   └── IT_QUICK_START.md         # Quick reference
│
├── deploy/
│   ├── windows/
│   │   └── Start-App.ps1         # Windows launcher
│   └── docker/
│       ├── Dockerfile           # Docker config
│       └── docker-compose.yml   # Multi-container setup
│
└── README.md                     # Project overview
```

---

## Quick Command Reference

### **Local Development**

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run application
streamlit run app/app.py

# Stop application
Ctrl + C

# Access
http://localhost:8501
```

### **Docker (Recommended for Production)**

```bash
# Build image
docker build -t ocss-command-center:1.0.0 .

# Run container
docker run -d -p 8501:8501 ocss-command-center:1.0.0

# Using Docker Compose
docker-compose up -d
docker-compose down
docker-compose logs -f
```

### **Check What's Running**

```bash
# Is it running?
ps aux | grep streamlit

# What port?
netstat -tlnp | grep 8501

# Full logs
streamlit run app/app.py  # Remove the & at end to see logs
```

---

## GitHub Repository Links

**Main Repository:**
```
https://github.com/arhawkins01-dotcom/ocss-command-center
```

**To Watch for Updates:**
1. Go to GitHub repo
2. Click **"Watch"** button (top right)
3. Get notified of new releases

**To Get Latest Changes:**
```bash
cd ocss-command-center
git pull origin main
```

---

## User Roles & Testing

After you start the app, you'll see a **role selector** (this is demo-only):

| Role | Purpose | Test Task |
|------|---------|-----------|
| **Program Officer** | Upload Excel files | Upload a file, see it transfer to Support Officer |
| **Support Officer** | Process reports | View uploaded files, edit data, export CSV |
| **Director** | Executive dashboard | View KPIs and team metrics |
| **Supervisor** | Team management | Monitor staff workload |
| **IT Admin** | System management | View system health & logs |

**Test the connection:**
1. Select **Program Officer**
2. Upload a file to Caseload 181000
3. Switch to **Support Officer**
4. View the same file in Caseload 181000
5. ✅ Success! Real-time data working!

---

## When Ready for Production

**See these documents:**
- `docs/IT_IMPLEMENTATION_GUIDE.md` - Full deployment steps
- `docs/EXECUTIVE_SUMMARY.md` - Business justification for approvals
- `docs/TECHNICAL_GUIDE.md` - Architecture details

**Key Production Setup:**
1. Docker containerization
2. Nginx reverse proxy + SSL/TLS
3. PostgreSQL database (Phase 2)
4. Authentication system (LDAP/AD)
5. Monitoring & backups

---

## Troubleshooting GitHub Access

### **"Command not found: git"**
```bash
# Install Git
sudo apt install git

# Or on macOS
brew install git
```

### **"Cannot clone repository"**
```bash
# Check internet connection
ping github.com

# Check SSH keys (if using SSH)
ssh -T git@github.com
```

### **"Module not found"**
```bash
# Ensure you installed requirements
pip install -r app/requirements.txt

# Check what was installed
pip list | grep streamlit
```

### **"Port 8501 already in use"**
```bash
# Find what's using port 8501
lsof -i :8501

# OR change port
streamlit run app/app.py --server.port=8502
```

---

## Summary

**For GitHub Access:**

| Need | Command |
|------|---------|
| **Clone app** | `git clone https://github.com/arhawkins01-dotcom/ocss-command-center.git` |
| **Install deps** | `pip install -r app/requirements.txt` |
| **Run locally** | `streamlit run app/app.py` |
| **Access it** | `http://localhost:8501` |
| **For production** | See `docs/IT_IMPLEMENTATION_GUIDE.md` |

---

**Ready to go live?** Contact IT with the EXECUTIVE_SUMMARY.md and they can handle the production deployment! 🚀
