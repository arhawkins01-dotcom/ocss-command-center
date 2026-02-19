# CHANGELOG

## Version 1.1.0 (Enhanced) - February 19, 2026

### New Features

#### Data Persistence
- Added session save/load functionality in sidebar
- Session data can be saved to JSON files for later restoration
- Automatic backup capability with timestamped backups

#### Enhanced Export Capabilities
- **Excel Export**: Added Excel (.xlsx) export alongside existing CSV exports
- **Multi-sheet Excel Export**: Support for exporting multiple DataFrames to a single Excel file
- **Enhanced Download Buttons**: Available in Program Officer, Support Officer, and IT Administrator sections

#### Data Validation
- Comprehensive data validation for uploaded reports
- Statistics display: total rows, columns, null values, duplicates
- Error and warning reporting with detailed messages
- Visual validation report with expandable details

#### Search and Filter
- Search functionality across DataFrames
- Filter controls for reports in Support Officer view
- Search in audit logs for IT Administrators
- Filter by actor in audit trail

#### Enhanced Audit Logging
- Persistent audit log storage to JSONL files
- Read audit log with pagination (up to 100 entries)
- Search and filter capabilities in audit trail
- Export audit logs to CSV and Excel formats
- Proper audit log formatting with timestamps

#### IT Administrator Tools
- **Real System Diagnostics**: Displays actual system checks with status
  - Session data check
  - Audit log check
  - Report data check
  - Units configuration check
  - File system check
- **Enhanced Backup**: Session data backup with timestamps
- **Audit Report Generation**: Generate comprehensive audit reports
- **Enhanced Maintenance Tools**: All buttons now have functional implementations

#### Visual Enhancements
- Added custom CSS styling for success, warning, and info boxes
- Better visual feedback for all user actions
- Improved color coding and icons throughout
- Enhanced footer with version and feature list

### Improvements

#### Code Quality
- Created comprehensive `report_utils.py` module with reusable functions
- Added type hints to all utility functions
- Comprehensive docstrings for all functions
- Better error handling throughout the application
- Modular code structure for maintainability

#### User Experience
- Session Management buttons prominently displayed in sidebar
- Clear feedback messages for all actions (✓ saved, ✓ loaded, etc.)
- Better organization of export options
- Improved help text and tooltips
- More intuitive button labels

### Technical Details

#### New Utility Functions in report_utils.py
- `save_session_data()` - Save session state to JSON
- `load_session_data()` - Load session state from JSON
- `export_to_excel()` - Export DataFrame to Excel format
- `export_multiple_sheets_to_excel()` - Export multiple DataFrames to Excel
- `validate_report_data()` - Comprehensive data validation
- `search_dataframe()` - Search functionality for DataFrames
- `format_audit_log_entry()` - Format audit log entries
- `write_audit_log()` - Write audit entries to file
- `read_audit_log()` - Read audit entries from file
- `get_caseload_summary()` - Generate caseload summary
- `validate_caseload_id()` - Validate caseload ID format

#### Dependencies
- No new dependencies required
- Uses existing: `streamlit`, `pandas`, `openpyxl`

### Files Changed
- `app/app.py` - Main application with all enhancements
- `app/report_utils.py` - New utility module (was placeholder)
- `.gitignore` - Added to exclude cache and temporary files

### Testing
- All features tested manually in browser
- Session save/load verified working
- Export functionality (CSV and Excel) tested
- Data validation tested with sample data
- IT Administrator diagnostics verified
- No security vulnerabilities found (CodeQL scan clean)

### Breaking Changes
- None - all existing functionality preserved

### Known Limitations
- Session data persistence is file-based (Phase 2 will add database)
- No authentication system yet (planned for Phase 2)
- Single-server deployment only (no load balancing yet)

### Migration Notes
- No migration needed
- Existing session data will work as before
- New features are additive only

---

## Version 1.0.0 - February 14, 2026

Initial release with:
- Role-based dashboards (5 roles)
- Caseload management
- Report processing
- Basic export functionality (CSV)
- Support tickets (basic)
- Knowledge base/FAQ
