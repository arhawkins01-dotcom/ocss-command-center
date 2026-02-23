# 🚀 Deploy OCSS Command Center to Streamlit Cloud

This guide explains how to deploy the OCSS Establishment Command Center to Streamlit Cloud for easy access via a web URL.

---

## 📋 Quick Reference

**GitHub Repository URL:**
```
https://github.com/arhawkins01-dotcom/ocss-command-center
```

**⭐ Main Application File (IMPORTANT!):**
```
app/app.py
```
> **Note:** The path is `app/app.py` (not just `app.py`). Include the `app/` directory prefix!
> 
> See [MAIN_FILE_PATH.md](MAIN_FILE_PATH.md) for detailed visual guide.

**Requirements File:**
```
app/requirements.txt
```

**Branch to Deploy:**
```
copilot/build-streamlit-application
```
(or `main` once merged)

---

## 🌐 Streamlit Cloud Deployment Steps

### Step 1: Access Streamlit Cloud

1. Go to **https://streamlit.io/cloud**

2. Sign in with your GitHub account
3. Click **"New app"** or **"Deploy an app"**

### Step 2: Configure Your App

Fill in the deployment form with these values:

| Field | Value |
|-------|-------|
| **Repository** | `arhawkins01-dotcom/ocss-command-center` |
| **Branch** | `copilot/build-streamlit-application` (or `main`) |
| **Main file path** | `app/app.py` ⭐ |

> 🚨 **IMPORTANT:** The "Main file path" must be exactly `app/app.py` (with the `app/` prefix).
> 
> Common mistakes:
> - ❌ `app.py` (missing directory)
> - ❌ `./app/app.py` (don't use `./`)
> - ❌ `/app/app.py` (don't use leading `/`)
> - ✅ `app/app.py` (CORRECT!)

For a visual guide, see [MAIN_FILE_PATH.md](MAIN_FILE_PATH.md)

### Step 3: Advanced Settings (Optional)

Click **"Advanced settings"** if you need to configure:

- **Python version**: 3.10 or higher (recommended: 3.12)
- **Secrets**: Add any secrets from `.streamlit/secrets.toml.template` if needed
- **Custom subdomain**: Choose a memorable URL for your app

### Step 4: Deploy

1. Click **"Deploy!"**
2. Wait 2-3 minutes for the app to build and deploy
3. Your app will be available at: `https://[your-app-name].streamlit.app`

---

## 🔗 Direct Deploy Link

You can use this URL to quickly start the deployment process:

```
https://share.streamlit.io/deploy?repository=arhawkins01-dotcom/ocss-command-center&branch=copilot/build-streamlit-application&mainModule=app/app.py
```

---

## ⚙️ Configuration Options

### Environment Variables

If deploying to Streamlit Cloud, the app will automatically use development paths. To use production paths, add this to your app secrets in Streamlit Cloud:

```toml
[app]
environment = "production"
```

### Secrets Management

To add secrets in Streamlit Cloud:
1. Go to your app dashboard
2. Click **"⋮"** (three dots menu)
3. Select **"Settings"**
4. Navigate to **"Secrets"**
5. Copy contents from `.streamlit/secrets.toml.template` and customize

---

## 📱 Accessing Your Deployed App

Once deployed, your app will be accessible at:
```
https://[your-app-name].streamlit.app
```

Example:
```
https://ocss-command-center.streamlit.app
```

You can share this URL with:
- Directors for executive dashboards
- Program Officers for report uploads
- Supervisors for team monitoring
- Support Officers for caseload management
- IT Administrators for system configuration

---

## 🔧 Troubleshooting

### Issue: "Module not found" errors

**Solution:** Ensure `app/requirements.txt` contains all dependencies:
```txt
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
```

### Issue: "File not found: app.py"

**Solution:** Make sure you specified the correct path: `app/app.py` (not just `app.py`)

### Issue: App won't start

**Solution:** Check the logs in Streamlit Cloud:
1. Go to your app dashboard
2. Click **"Manage app"**
3. View the **"Logs"** tab for error messages

---

## 🔄 Updating Your Deployed App

Streamlit Cloud automatically redeploys when you push changes to your GitHub repository:

1. Make changes to your code
2. Commit and push to GitHub
3. Streamlit Cloud detects the changes
4. App automatically rebuilds and redeploys (takes ~2-3 minutes)

---

## 🏢 Alternative: Internal Server Deployment

If you prefer **internal deployment** on your Windows server instead of Streamlit Cloud:

See the **[Deployment Guide](deploy/DEPLOYMENT_GUIDE.md)** for instructions on deploying to:
```
S:\OCSS\CommandCenter\
```

Use the PowerShell script:
```powershell
cd deploy\windows
.\Start-App.ps1
```

---

## 📞 Support

### For Streamlit Cloud Issues:
- Streamlit Cloud Documentation: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Community Forum: https://discuss.streamlit.io/

### For Application Issues:
- Check the [App README](app/README.md)
- Review the [Deployment Guide](deploy/DEPLOYMENT_GUIDE.md)
- Open an issue on GitHub

---

## 📊 What You'll Get

After deployment, you'll have access to 5 role-based dashboards:

1. **Director** - Executive Dashboard with KPIs
2. **Program Officer** - Report Intake Portal
3. **Supervisor** - KPI Monitoring Dashboard
4. **Support Officer** - Caseload Management
5. **IT Administrator** - System Administration

All accessible through a single web URL! 🎉

---

**Last Updated:** February 2026
**Version:** 1.0.0
