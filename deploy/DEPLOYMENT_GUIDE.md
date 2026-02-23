# OCSS Command Center - Deployment Guide

## Quick Start

### Prerequisites
- Windows Server 2016 or later
- Python 3.10 or higher
- PowerShell 5.1 or higher
- Network access to S: drive (for production deployment)

### Installation Steps

#### 1. Install Python
1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```cmd
   python --version
   ```

#### 2. Copy Application Files
Copy the entire application to the production server:
```
S:\OCSS\CommandCenter\
```

Directory structure should be:
```
S:\OCSS\CommandCenter\
├── app\
│   ├── app.py
│   ├── report_utils.py
│   ├── requirements.txt
│   └── config\
│       ├── __init__.py
│       └── settings.py
├── .streamlit\
│   ├── config.toml
│   └── secrets.toml (create from template)
├── deploy\
│   └── windows\
│       └── Start-App.ps1
├── data\        (created automatically)
├── logs\        (created automatically)
└── exports\     (created automatically)
```

#### 3. Configure Secrets (Optional)
If using custom configuration:
1. Copy `.streamlit/secrets.toml.template` to `.streamlit/secrets.toml`
2. Edit the file with production values
3. Ensure `environment = "production"` in the secrets file

#### 4. Run Deployment Script
Open PowerShell as Administrator and run:
```powershell
cd S:\OCSS\CommandCenter\deploy\windows
.\Start-App.ps1
```

The script will:
- ✓ Check Python installation
- ✓ Create required directories
- ✓ Install/update dependencies
- ✓ Start the Streamlit application

#### 5. Access the Application
Once started, access the application at:
- **Local**: http://localhost:8501
- **Network**: http://[server-ip]:8501

### Manual Installation (Alternative)

If the PowerShell script doesn't work, install manually:

```cmd
cd S:\OCSS\CommandCenter\app
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the application:
```cmd
cd S:\OCSS\CommandCenter\app
streamlit run app.py --server.port 8501 --server.headless true
```

## Configuration

### Environment Variables
Set for production deployment:
```cmd
set OCSS_ENV=production
```

### Port Configuration
Default port is 8501. To change:
- Edit `.streamlit/config.toml`
- Update the `[server]` section:
  ```toml
  [server]
  port = 8501
  ```

### File Paths
Production paths are configured in `app/config/settings.py`:
- Data: `S:\OCSS\CommandCenter\Data`
- Logs: `S:\OCSS\CommandCenter\Logs`
- Exports: `S:\OCSS\CommandCenter\Exports`

## Troubleshooting

### Application Won't Start

**Problem**: "Python not found"
- **Solution**: Ensure Python is in PATH. Reinstall Python with "Add to PATH" checked.

**Problem**: "Module not found" errors
- **Solution**: Run dependency installation again:
  ```cmd
  pip install -r requirements.txt
  ```

**Problem**: Port 8501 already in use
- **Solution**: 
  1. Stop existing Streamlit instances
  2. Or change port in `.streamlit/config.toml`

### Performance Issues

**Problem**: Slow file uploads
- **Solution**: Check `max_upload_size_mb` in `secrets.toml` or `settings.py`

**Problem**: Application crashes with large files
- **Solution**: Increase memory limits in Streamlit config:
  ```toml
  [server]
  maxUploadSize = 200
  ```

### Permission Issues

**Problem**: Cannot create directories
- **Solution**: Run PowerShell as Administrator

**Problem**: Cannot access S: drive
- **Solution**: Verify network permissions and drive mapping

## Maintenance

### Viewing Logs
Application logs are stored in:
```
S:\OCSS\CommandCenter\Logs\
```

Audit logs:
```
S:\OCSS\CommandCenter\app\audit_log.jsonl
```

### Updating the Application

1. Stop the running application (Ctrl+C in PowerShell)
2. Copy new files to production directory
3. Restart using `Start-App.ps1`

### Backup Recommendations

Regular backups of:
- Configuration files (`.streamlit/secrets.toml`, `app/config/settings.py`)
- Data directory (`S:\OCSS\CommandCenter\Data\`)
- Audit logs (`audit_log.jsonl`)

## Security Considerations

1. **Secrets Management**: Never commit `secrets.toml` to version control
2. **Access Control**: Configure Windows Server permissions appropriately
3. **Network Security**: Use internal network only (not exposed to internet)
4. **Audit Logging**: Regularly review audit logs for unusual activity
5. **Updates**: Keep Python and dependencies up to date

## Support

For technical support:
- Check logs in `S:\OCSS\CommandCenter\Logs\`
- Review Streamlit documentation: https://docs.streamlit.io
- Contact IT Administrator through the application's Support Tickets module

## Production Checklist

Before going live:
- [ ] Python 3.10+ installed
- [ ] All dependencies installed
- [ ] Directory permissions configured
- [ ] `.streamlit/secrets.toml` created (if needed)
- [ ] Environment set to "production"
- [ ] Application accessible on network
- [ ] All 5 roles tested and functional
- [ ] File upload/download working
- [ ] Audit logging enabled
- [ ] Backup procedure established
- [ ] IT staff trained on deployment script

## Application Features

### Role-Based Access
The application supports 5 roles:
1. **Director**: Executive dashboard, KPIs, team management
2. **Program Officer**: Report intake and processing
3. **Supervisor**: Team monitoring, workflow management
4. **Support Officer**: Assigned reports, caseload management
5. **IT Administrator**: System settings, user management, audit logs

### Data Management
- Excel (.xlsx, .xls) and CSV file support
- Maximum upload size: 50 MB (configurable)
- Automatic data validation
- Export to Excel, CSV, or JSON formats

### System Health
The IT Administrator dashboard includes:
- System status monitoring
- Component health checks
- User activity tracking
- Audit log viewing

## Version Information

- **Application Version**: 1.0.0
- **Streamlit Version**: 1.30.0+
- **Python Version**: 3.10+
- **Last Updated**: February 2026
