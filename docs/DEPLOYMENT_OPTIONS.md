# Deployment Options for OCSS Command Center

## Current Deployment: Internal Windows Server

### Status
✅ **Active** - The application is currently deployed on an internal Windows server.

**Location:** `S:\OCSS\CommandCenter\App\`

**Access:** Internal staff only via local network

**Method:** Streamlit running on internal Windows Server

### Why Internal Hosting?
- **Data Security:** Sensitive child support information remains within County network
- **Access Control:** Limited to authorized internal staff only
- **IT Compliance:** Meets organizational security and privacy requirements
- **Network Integration:** Direct access to internal resources and databases

---

## Alternative: Streamlit Community Cloud

### What is Streamlit Cloud?
Streamlit Community Cloud is a free hosting platform for public Streamlit applications.

### ⚠️ NOT RECOMMENDED for this application because:
1. **Data Privacy Concerns:** Would expose sensitive child support data to public internet
2. **Security Requirements:** County data must remain on internal servers
3. **Access Control:** Cannot restrict to internal staff only on free tier
4. **Compliance Issues:** May violate HIPAA and other privacy regulations

### If Streamlit Cloud Were Needed (Hypothetical)

To deploy to Streamlit Cloud, you would need to:

1. **Prepare the Repository:**
   - Ensure `requirements.txt` is in the root directory
   - Remove any sensitive data or credentials
   - Add `.streamlit/secrets.toml` to `.gitignore`

2. **Configure Streamlit Cloud:**
   - Connect your GitHub repository at [share.streamlit.io](https://share.streamlit.io)
   - Select the main branch
   - Specify `app/app.py` as the main file
   - Add any secrets through the Streamlit Cloud dashboard

3. **Repository Structure:**
   ```
   /
   ├── app/
   │   ├── app.py          # Main application
   │   └── report_utils.py
   ├── requirements.txt     # Dependencies
   └── .streamlit/
       └── config.toml      # Configuration
   ```

4. **Required Files:**
   - `app/app.py` - Main Streamlit application
   - `requirements.txt` - Python dependencies
   - `.streamlit/config.toml` - Streamlit configuration (optional)

**Note:** This is for educational purposes only. This application should NOT be deployed to public cloud services.

---

## Deployment Comparison

| Feature | Internal Server (Current) | Streamlit Cloud |
|---------|-------------------------|-----------------|
| **Security** | ✅ High - Internal only | ❌ Public internet |
| **Data Privacy** | ✅ Full control | ❌ Limited control |
| **Access Control** | ✅ Network-based | ❌ Limited on free tier |
| **Cost** | Internal IT resources | Free (public) / Paid (private) |
| **Compliance** | ✅ Meets requirements | ❌ May not comply |
| **Maintenance** | IT team manages | Streamlit manages |
| **Recommended** | ✅ **YES** | ❌ **NO** |

---

## Current Deployment Process

See `/deploy/windows/Start-App.ps1` for the Windows server deployment script.

### Running Locally
```bash
# Install dependencies
pip install -r app/requirements.txt

# Run the application
streamlit run app/app.py
```

### Running on Internal Server
```powershell
# Navigate to deployment directory
cd S:\OCSS\CommandCenter\App\

# Run deployment script
.\Start-App.ps1
```

---

## Questions?

**Q: Is this app saved on Streamlit Cloud?**  
**A:** No, this application is NOT deployed on Streamlit Cloud. It runs on an internal Windows server for security and privacy reasons.

**Q: Can I access this app from outside the office?**  
**A:** No, it's only accessible from within the County network for security purposes.

**Q: Why use Streamlit if not using Streamlit Cloud?**  
**A:** Streamlit is a Python framework for building web applications. It can be deployed anywhere Python runs - you don't need to use Streamlit Cloud to use the Streamlit framework.

---

Generated: February 19, 2026
