# Frequently Asked Questions (FAQ)

## Deployment & Hosting

### Q: Is this app saved on Streamlit?
**A:** This depends on what you mean:

- ✅ **YES** - This IS a Streamlit application (built using the Streamlit framework)
- ❌ **NO** - This is NOT deployed on Streamlit Community Cloud
- 📍 **Hosted internally** on a Windows server at `S:\OCSS\CommandCenter\App\`

**Bottom line:** It uses Streamlit as the web framework, but runs on our internal server, not on Streamlit's cloud platform.

### Q: Why isn't it on Streamlit Cloud?
**A:** Security and privacy. This application handles sensitive child support data that must remain within the County's secure network. Streamlit Cloud is a public hosting service, which would expose data to the internet.

### Q: Can I access it from home?
**A:** No, it's only accessible from within the County network for security reasons.

### Q: Can we deploy it to Streamlit Cloud later?
**A:** Not recommended due to data privacy and security requirements. See [DEPLOYMENT_OPTIONS.md](DEPLOYMENT_OPTIONS.md) for details.

---

## Technical Questions

### Q: What is Streamlit?
**A:** Streamlit is a Python framework for building web applications. It's just software you install - you can run it anywhere (your computer, a server, the cloud, etc.). Using Streamlit doesn't mean you have to use Streamlit Cloud.

Think of it like:
- **Microsoft Word** (the software) vs **OneDrive** (Microsoft's cloud storage)
- **Streamlit** (the framework) vs **Streamlit Cloud** (Streamlit's hosting service)

### Q: How do I run it locally?
**A:** 
```bash
# Install dependencies
pip install -r app/requirements.txt

# Run the app
streamlit run app/app.py
```
Then open http://localhost:8501 in your browser.

### Q: What version of Python is needed?
**A:** Python 3.7 or higher. See `requirements.txt` for dependencies.

---

## Repository Questions

### Q: What is GitHub used for?
**A:** GitHub stores the source code, documentation, and version history. It's for development and collaboration - NOT for hosting the live application.

### Q: How do updates get deployed?
**A:** 
1. Developers make changes and push to GitHub
2. IT team reviews and tests changes
3. IT deploys updated code to internal server at `S:\OCSS\CommandCenter\App\`

### Q: Who has access to this repository?
**A:** Authorized OCSS staff and IT personnel involved in maintaining the application.

---

## Data & Security

### Q: Is the data stored in GitHub?
**A:** No. GitHub only contains the application code, not the Excel reports or sensitive data that users upload when running the application.

### Q: Where is data stored?
**A:** Data uploaded to the application is stored in the application's session state (temporary memory) and is not persisted to disk unless specifically saved by users on the internal server.

### Q: Is this application secure?
**A:** Yes, it runs on the County's secure internal network with:
- Network-level access controls
- No internet exposure
- Internal authentication
- Compliance with County IT policies

---

## Support

### Q: Who do I contact for help?
**A:** 
- **Application issues:** OCSS IT support team
- **Access issues:** Your supervisor or IT helpdesk
- **Feature requests:** Submit through appropriate OCSS channels

### Q: Can I suggest improvements?
**A:** Yes! Contact the OCSS IT team or your supervisor with suggestions.

---

Generated: February 19, 2026
