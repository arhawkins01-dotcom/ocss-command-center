# OCSS Command Center - Application

This directory contains the main Streamlit web application for the OCSS Establishment Command Center.

## Files

### Core Application
- **app.py** - Main Streamlit application with role-based dashboards
- **report_utils.py** - Data processing utilities for Excel/CSV file handling
- **requirements.txt** - Python dependencies

### Configuration
- **config/** - Configuration management
  - `settings.py` - Application settings and environment configuration
  - `__init__.py` - Package initialization

### Sample Data
- **sample_data/** - Example data files for testing
  - `sample_establishment_report.xlsx/csv` - Example establishment report
  - `sample_monthly_summary.xlsx/csv` - Example monthly summary
  - `sample_cqi_alignment.xlsx/csv` - Example CQI alignment data

### Testing & Development
- **create_sample_data.py** - Generate sample data files for testing
- **test_integration.py** - Integration tests for the application

## Quick Start

### Run the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will start on http://localhost:8501

### Run Tests

```bash
# Run integration tests
python test_integration.py

# Create sample data
python create_sample_data.py
```

## Application Features

### Role-Based Access

The application provides 5 distinct role-based interfaces:

1. **Director** - Executive dashboard with KPIs and team management
2. **Program Officer** - Report intake and processing portal
3. **Supervisor** - Team monitoring and workflow management
4. **Support Officer** - Assigned reports and caseload management
5. **IT Administrator** - System settings and audit logs

### Data Processing

- Upload Excel (.xlsx, .xls) or CSV files
- Automatic data validation
- Data cleaning and normalization
- Export to multiple formats (Excel, CSV, JSON)

### Key Modules

#### report_utils.py

Provides classes for data processing:
- `ReportProcessor` - File reading, validation, and cleaning
- `ReportExporter` - Export to various formats
- `DataValidator` - Business rule validation
- `AuditLogger` - Audit log management

#### config/settings.py

Configuration management:
- Environment detection (development/production)
- Path configuration for data, logs, exports
- Default organizational structure
- KPI thresholds and validation rules

## Configuration

### Environment Variables

- `OCSS_ENV` - Set to "production" for production deployment (default: "development")

### Production Paths

When `OCSS_ENV=production`, the application uses:
- Data: `S:\OCSS\CommandCenter\Data`
- Logs: `S:\OCSS\CommandCenter\Logs`
- Exports: `S:\OCSS\CommandCenter\Exports`

### Development Paths

In development mode, paths are relative to the repository:
- Data: `../data`
- Logs: `../logs`
- Exports: `../exports`

## Architecture

### Session State Management

The application uses Streamlit's session state to maintain:
- Uploaded reports
- Organizational units and assignments
- Report processing status
- User selections

### File Processing Pipeline

1. File upload via Streamlit file_uploader
2. Validation using ReportProcessor
3. Data cleaning and normalization
4. Display in editable DataFrame
5. Export options for processed data

### Audit Logging

All administrative actions are logged to `audit_log.jsonl` with:
- Timestamp
- User/role
- Action performed
- Additional details

## Development

### Adding New Features

1. Update `app.py` with new UI components
2. Add processing functions to `report_utils.py`
3. Update configuration in `config/settings.py`
4. Update tests in `test_integration.py`

### Code Style

- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Document functions with docstrings
- Add logging for important operations

## Troubleshooting

### Module Import Errors

If you see "Module not found" errors:
```bash
pip install -r requirements.txt --upgrade
```

### File Upload Issues

Check the configuration in `config/settings.py`:
- `MAX_UPLOAD_SIZE_MB` - Maximum file size (default: 50MB)
- `ALLOWED_UPLOAD_EXTENSIONS` - Allowed file types

### Path Issues

Verify environment variable:
```bash
echo $OCSS_ENV  # Should be "production" or not set
```

## Testing

### Integration Tests

The `test_integration.py` script validates:
- ✓ Module imports
- ✓ Configuration loading
- ✓ Report processing
- ✓ Data validation
- ✓ Export functionality
- ✓ Utility functions

Run tests before deployment:
```bash
python test_integration.py
```

### Sample Data

Generate test data:
```bash
python create_sample_data.py
```

This creates sample files in `sample_data/` for testing uploads.

## Support

For technical issues:
1. Check logs in the logs directory
2. Run integration tests
3. Review Streamlit documentation: https://docs.streamlit.io
4. Contact IT Administrator

## Version

- **Application Version**: 1.0.0
- **Python**: 3.10+
- **Streamlit**: 1.30.0+
