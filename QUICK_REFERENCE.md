# 🎯 Quick Reference - OCSS Command Center Deployment

## GitHub Repository
```
https://github.com/arhawkins01-dotcom/ocss-command-center
```

## Streamlit Cloud Deployment

### Repository Settings
- **Repository:** `arhawkins01-dotcom/ocss-command-center`
- **Branch:** `copilot/build-streamlit-application` or `main`
- **Main file path:** `app/app.py` ⭐
- **Python version:** 3.10+

> **⚠️ CRITICAL:** Main file path MUST be `app/app.py` (not just `app.py`)
> 
> See [MAIN_FILE_PATH.md](MAIN_FILE_PATH.md) for visual guide

### Direct Deploy URL
Click this link to deploy directly:
```
https://share.streamlit.io/deploy?repository=arhawkins01-dotcom/ocss-command-center&branch=copilot/build-streamlit-application&mainModule=app/app.py
```

### Your App URL (after deployment)
```
https://[your-app-name].streamlit.app
```

## Local Development

### Start the App
```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```

### Access Locally
```
http://localhost:8501
```

## Full Documentation
- **Streamlit Cloud Guide:** [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md)
- **Internal Server Guide:** [deploy/DEPLOYMENT_GUIDE.md](deploy/DEPLOYMENT_GUIDE.md)
- **App Documentation:** [app/README.md](app/README.md)

---
**Need Help?** See the full deployment guides linked above.
