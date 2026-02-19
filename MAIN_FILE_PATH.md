# 📂 Main File Path - Visual Guide

## ✅ THE CORRECT MAIN FILE PATH IS:

```
app/app.py
```

---

## 📊 Repository Structure

```
ocss-command-center/              ← Root of repository
│
├── app/                          ← Application directory
│   ├── app.py                    ← ⭐ THIS IS THE MAIN FILE ⭐
│   ├── requirements.txt          ← Dependencies
│   ├── report_utils.py           ← Utilities
│   ├── config/                   ← Configuration
│   └── sample_data/              ← Test data
│
├── .streamlit/
│   └── config.toml               ← Streamlit settings
│
├── deploy/                       ← Deployment scripts
├── docs/                         ← Documentation
└── README.md                     ← Main readme
```

---

## 🎯 For Streamlit Cloud Deployment

When deploying to Streamlit Cloud, enter this **EXACT PATH**:

### ✅ CORRECT:
```
app/app.py
```

### ❌ WRONG:
```
app.py          ← Missing the "app/" directory prefix
./app/app.py    ← Don't include "./" 
/app/app.py     ← Don't include leading "/"
```

---

## 🔍 How to Verify

### Method 1: Manual Check
Run this command to verify the file exists:

```bash
# From repository root
ls -la app/app.py
```

You should see:
```
-rw-rw-r-- 1 user user 69083 Feb 19 app/app.py
```

### Method 2: Automated Verification Script
Run the included verification script:

```bash
# From repository root
./verify-path.sh
```

This will check:
- ✓ File exists at correct location
- ✓ File size is correct
- ✓ File is a valid Python script

The script will show "✅ VERIFICATION PASSED" if everything is correct.

---

## 📝 Streamlit Cloud Configuration

When deploying, use these settings:

| Setting | Value |
|---------|-------|
| **Repository** | `arhawkins01-dotcom/ocss-command-center` |
| **Branch** | `copilot/build-streamlit-application` or `main` |
| **Main file path** | `app/app.py` ⭐ |
| **Python version** | 3.10 or higher |

---

## 🚀 Quick Deploy

Use this pre-configured link with the correct path:

```
https://share.streamlit.io/deploy?repository=arhawkins01-dotcom/ocss-command-center&branch=copilot/build-streamlit-application&mainModule=app/app.py
```

Notice the `mainModule=app/app.py` parameter!

---

## ❓ Why "app/app.py"?

The application is organized with:
- **`app/`** directory = Contains all application code
- **`app.py`** file = The main Streamlit application file

So the path is: **directory** + **file** = `app/app.py`

---

## 🆘 Troubleshooting

### Error: "File not found: app.py"
**Problem:** You entered just `app.py` instead of `app/app.py`

**Solution:** 
1. Go to your Streamlit Cloud app settings
2. Change "Main file path" from `app.py` to `app/app.py`
3. Save and redeploy

### Error: "No module named 'streamlit'"
**Problem:** Requirements file not found or incorrect path

**Solution:**
- Verify `app/requirements.txt` exists
- Streamlit Cloud automatically looks in the same directory as your main file
- The `requirements.txt` is in `app/` so this should work automatically

---

## ✨ Summary

**Main File Path:** `app/app.py`

Copy and paste this exact path when deploying to Streamlit Cloud!

---

For complete deployment instructions, see:
- [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md)
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
