# 🚀 Quick Start Guide - Launch OCSS Command Center

**New to the OCSS Command Center?** This guide will have you up and running in under 2 minutes!

---

## ⚡ Fastest Method (10 seconds)

### Step 1: Open the Launcher
1. Navigate to the repository folder
2. **Double-click** `LAUNCH.html`
3. Your browser will open with a professional launch portal

### Step 2: Launch the App
1. Click the big **"🚀 Launch Application"** button
2. The Command Center opens in a new tab automatically!
3. That's it! You're in! ✅

**Visual Guide:**
```
📁 Repository Folder
  └── 📄 LAUNCH.html  ← Double-click this file
        ↓
  🌐 Browser Opens (Launch Portal)
        ↓
  👆 Click "Launch Application" button
        ↓
  ✅ Command Center Opens!
```

---

## 🖥️ Alternative Methods

### Method 1: Using Command Line (Linux/Mac)

```bash
# Navigate to repository
cd /path/to/ocss-command-center

# Run the startup script
./deploy/start-app.sh
```

The script will:
- ✅ Check your Python installation
- ✅ Install dependencies automatically
- ✅ Launch the application
- ✅ Open your browser to http://localhost:8501

### Method 2: Using PowerShell (Windows)

```powershell
# Navigate to repository
cd C:\path\to\ocss-command-center

# Run the startup script
.\deploy\windows\Start-App.ps1
```

The script will:
- ✅ Check your Python installation
- ✅ Install dependencies automatically
- ✅ Launch the application
- ✅ Open your browser automatically

### Method 3: Manual Launch (For Developers)

```bash
# Navigate to app folder
cd app

# Install dependencies (first time only)
pip install -r requirements.txt

# Launch the application
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

---

## 📱 What You'll See

Once launched, the OCSS Command Center displays:

![OCSS Command Center Running](https://github.com/user-attachments/assets/ce6770b4-e387-4cdc-8de2-3c8ceff5f066)
*The Command Center dashboard showing all recent updates*

### ✅ Status Indicator (NEW!)
- **Green banner** in sidebar: "✅ System Status: OPEN - Ready for Operations"
- Confirms the system is operational

### 🎯 Role Selection
Choose your role from the sidebar:
- **Director** - Executive Dashboard with KPIs
- **Program Officer** - Report Upload & Management
- **Supervisor** - Team Management
- **Support Officer** - Caseload Processing
- **IT Administrator** - System Management

### 📊 Live Data Dashboard
- Real-time metrics and analytics
- Interactive reports
- Team performance data
- Workload management tools

---

## 🆘 Troubleshooting

### Problem: "Python not found"
**Solution:** Install Python 3.8 or higher from [python.org](https://python.org)

### Problem: "Module not found" errors
**Solution:** Install dependencies:
```bash
cd app
pip install -r requirements.txt
```

### Problem: "Port 8501 already in use"
**Solution:** Stop any existing Streamlit processes:
```bash
# Find the process
ps aux | grep streamlit

# Kill the process (replace PID with actual number)
kill <PID>
```

### Problem: LAUNCH.html shows "Application Not Running"
**Solution:** 
1. First, start the app using one of the command-line methods
2. Then the LAUNCH.html button will work

### Problem: Browser doesn't open automatically
**Solution:** Manually navigate to **http://localhost:8501** in your browser

---

## 🎓 First Time User Guide

### 1. Start with Director Role
- See the high-level KPIs and metrics
- Get familiar with the interface
- No technical knowledge needed!

### 2. Try Support Officer Role
- View caseload management
- See how reports are processed
- Experience the main workflow

### 3. Explore IT Administrator
- Check system status
- See user management features
- View technical diagnostics

---

## 🔗 Quick Reference

| Access Method | Speed | Difficulty | Best For |
|--------------|-------|------------|----------|
| LAUNCH.html | ⚡ Instant | ⭐ Easy | Everyone |
| Bash Script | 🚀 Fast | ⭐⭐ Medium | Linux/Mac Users |
| PowerShell Script | 🚀 Fast | ⭐⭐ Medium | Windows Users |
| Manual Launch | 🐢 Slower | ⭐⭐⭐ Advanced | Developers |

---

## 📞 Need Help?

- **Documentation:** Check the `docs/` folder for detailed guides
- **Technical Guide:** See `docs/TECHNICAL_GUIDE.md`
- **IT Guide:** See `docs/IT_QUICK_START.md`
- **User Manual:** See `docs/USER_MANUAL.md`

---

## ✅ You're All Set!

**The Command Center is ready for you!** Just:
1. Open `LAUNCH.html` 
2. Click "Launch Application"
3. Start exploring!

**Enjoy using the OCSS Command Center!** 🎉
