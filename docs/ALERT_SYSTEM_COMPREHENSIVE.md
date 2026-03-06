# Comprehensive Alert & Notification System
## Upgraded Alert Logic for OCSS Command Center

## Overview

The new Alert System provides a comprehensive, centralized approach to managing all notifications, warnings, and alerts throughout the OCSS Command Center. It replaces scattered `st.success()`, `st.warning()`, and `st.error()` calls with a structured, persistent, and role-aware alert management system.

### Key Features

✅ **Structured Alert Types** - 5 severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)  
✅ **Persistent Storage** - Alerts retained in history for audit/compliance  
✅ **Role-Based Routing** - Target alerts to specific roles or users  
✅ **Alert Acknowledgment** - Track who acknowledged which alerts and when  
✅ **Expiring Alerts** - Auto-dismiss temporary alerts after set time  
✅ **Action Tracking** - Alerts can require user action with callbacks  
✅ **Dashboard & Reporting** - View alerts, history, metrics, and export data  
✅ **Filtering & Search** - Filter by level, category, role, date range  

---

## Architecture

### Alert Levels

| Level | Value | Color | Emoji | Use Case |
|-------|-------|-------|-------|----------|
| **DEBUG** | 0 | Gray | 🐛 | Development/troubleshooting |
| **INFO** | 1 | Blue | ℹ️ | General information |
| **WARNING** | 2 | Orange | ⚠️ | Action recommended |
| **ERROR** | 3 | Red | ❌ | Action required |
| **CRITICAL** | 4 | Dark Red | 🚨 | System failure/urgent |

### Components

#### 1. **AlertSystem.py** (622 lines)
Core alert management engine with:
- `Alert` class - Individual alert objects
- `AlertLevel` enum - Severity levels
- `AlertManager` class - Central management hub
- Persistence layer - File-based storage
- Configuration management
- Alert history and export

#### 2. **AlertUI.py** (372 lines)
Streamlit UI rendering components:
- `render_alert_banner()` - Single alert display
- `render_alert_with_action()` - Interactive alerts
- `render_alert_toast()` - Non-blocking notifications
- `render_alert_badge()` - Status indicators
- `render_active_alerts()` - Alert panel
- `render_alert_dashboard()` - Full dashboard
- `render_category_alerts()` - Category filtering
- `render_alert_preferences()` - Configuration UI

---

## Alert Properties

Each alert can have:

```python
Alert(
    title: str,                      # Short title
    message: str,                    # Detailed message
    level: AlertLevel,               # Severity (INFO, WARNING, ERROR, etc.)
    category: str,                   # Group/filter category
    alert_id: str,                   # Unique identifier (auto-generated)
    dismissible: bool,               # Can user dismiss?
    persistent: bool,                # Store in history?
    requires_action: bool,           # Needs user response?
    action_label: str,               # Button text if action required
    metadata: Dict,                  # Additional context
    expires_in_seconds: int,         # Auto-dismiss after N seconds
    affected_role: str,              # Target role (e.g., "Supervisor")
    affected_user: str               # Target user
)
```

### Example: Alert with Full Properties

```python
from app.alert_system import AlertLevel, create_alert

create_alert(
    title="High Workload Detected",
    message="Michael Chen has exceeded recommended caseload",
    level=AlertLevel.WARNING,
    category="performance",           # For filtering
    persistent=True,                  # Store in history
    requires_action=True,             # Show action button
    action_label="View Details",      # Button text
    metadata={                        # Context data
        'worker': 'Michael Chen',
        'current_load': '32 caseloads',
        'recommended_max': '25 caseloads'
    },
    affected_role="Supervisor",       # Only show to supervisors
    dismissible=False,                # User can't dismiss
    expires_in_seconds=86400          # Auto-dismiss after 24 hours
)
```

---

## Usage Patterns

### Pattern 1: Success Notification (Replacing st.success)

**Before:**
```python
st.success(f"✓ Report '{report_name}' processed!")
```

**After:**
```python
from app.alert_system import AlertLevel, create_alert

create_alert(
    title="Report Processed",
    message=f"Report '{report_name}' successfully processed",
    level=AlertLevel.INFO,
    category="processing"
)
```

### Pattern 2: Error with Recovery (Replacing st.error)

**Before:**
```python
st.error(f"Error reading file: {str(e)}")
```

**After:**
```python
create_alert(
    title="File Processing Failed",
    message=str(e),
    level=AlertLevel.ERROR,
    category="file_operations",
    persistent=True,          # Log for audit
    requires_action=True,
    action_label="Retry",
    metadata={'file': filename}
)
```

### Pattern 3: Business Warning (Replacing st.warning)

**Before:**
```python
st.warning(f"Caseload {caseload} already assigned to {person}")
```

**After:**
```python
create_alert(
    title="Caseload Already Assigned",
    message=f"Caseload {caseload} is currently assigned",
    level=AlertLevel.WARNING,
    category="assignment",
    metadata={
        'caseload': caseload,
        'current_owner': person,
        'current_unit': unit
    }
)
```

### Pattern 4: Information Message (Replacing st.info)

**Before:**
```python
st.info("✅ All systems operational")
```

**After:**
```python
create_alert(
    title="System Status",
    message="All systems operational and monitoring normally",
    level=AlertLevel.INFO,
    category="system",
    expires_in_seconds=300  # Temporary notification
)
```

---

## Integration with App.py

### 1. Initialize at App Start

```python
# At top of app.py
from app.alert_system import get_alert_manager, AlertLevel
from app.alert_ui import render_alert_badge

# Initialize alert manager
manager = get_alert_manager()

# Show alert badge in sidebar
st.sidebar.markdown("---")
render_alert_badge(position="sidebar")
```

### 2. Replace Inline Messages

Replace scattered `st.success()` calls:

```python
# OLD
st.success(f"✓ Report '{report_name}' progress saved!")

# NEW
from app.alert_system import create_alert
create_alert(
    title="Report Saved",
    message=f"Report '{report_name}' progress saved",
    level=AlertLevel.INFO,
    category="file_operations"
)
```

### 3. Add Alert Dashboard for Admin/Supervisor

```python
# In IT Administrator tab
from app.alert_ui import render_alert_dashboard

with it_tab1:
    st.subheader("Systems & Alerts")
    manager = get_alert_manager()
    render_alert_dashboard(manager)
```

### 4. Show Active Alerts at Top of Role Section

```python
# In each role section
from app.alert_ui import render_active_alerts

if role == "Supervisor":
    manager = get_alert_manager()
    render_active_alerts(manager, role="Supervisor", exclude_acknowledged=True)
```

---

## Features

### Alert Filtering

```python
from app.alert_system import get_alert_manager, AlertLevel

manager = get_alert_manager()

# Get critical errors only
alerts = manager.get_active_alerts(level_min=AlertLevel.CRITICAL)

# Get compliance-related warnings
alerts = manager.get_active_alerts(
    level_min=AlertLevel.WARNING,
    category="compliance"
)

# Get alerts for specific role
alerts = manager.get_active_alerts(role="Supervisor")

# Exclude already-acknowledged alerts
alerts = manager.get_active_alerts(exclude_acknowledged=True)
```

### Alert Acknowledgment

```python
# Acknowledge an alert
manager.acknowledge_alert(alert_id="abc123", user="Michael Chen")

# Track in session state for audit
if 'alert_acknowledgments' in st.session_state:
    acks = st.session_state.alert_acknowledgments
```

### Alert History

```python
# Get alerts from past 7 days (WARNING level and above)
history = manager.get_history(days=7, level_min=AlertLevel.WARNING)

# Export to CSV
csv_data = manager.export_history(format='csv')

# Export to JSON
json_data = manager.export_history(format='json')
```

### Alert Configuration

```python
manager = get_alert_manager()

# Adjust settings
manager.alert_config['min_level_to_persist'] = 'WARNING'  # What levels to store
manager.alert_config['retention_days'] = 30              # How long to keep
manager.alert_config['max_simultaneous_alerts'] = 50     # Max active alerts
manager.alert_config['default_expires_seconds'] = 300    # Auto-dismiss time

# Save configuration
manager._save_config()
```

---

## UI Components

### Alert Badge (Shows in Sidebar)

```python
from app.alert_ui import render_alert_badge

render_alert_badge(position="sidebar")  # Shows: 🚨 2 or ✅ Good
```

### Active Alerts Panel

```python
from app.alert_ui import render_active_alerts

manager = get_alert_manager()
render_active_alerts(manager, exclude_acknowledged=True)
```

### Alert Dashboard (Admin View)

```python
from app.alert_ui import render_alert_dashboard

manager = get_alert_manager()
render_alert_dashboard(manager)  # Full dashboard with history and export
```

### Toast Notifications

```python
from app.alert_ui import render_alert_toast

render_alert_toast(state_key="toast_alerts")  # Shows temporary notifications
```

---

## Categories for Organization

Suggested categories for filtering/routing:

- **system** - Database, server, infrastructure
- **file_operations** - Upload, download, processing
- **file_validation** - Format, data quality checks
- **data_quality** - Missing values, inconsistencies
- **compliance** - CQI alignment, regulations, requirements
- **performance** - Workload, response time, efficiency
- **assignment** - Caseload assignment/reassignment
- **workload** - Workload limits, distribution
- **security** - Password, access, authentication
- **reporting** - Report generation, export
- **processing** - Long-running operations
- **general** - Miscellaneous

---

## Real-World Scenario: File Upload Handler

### Current Implementation (Alert System)

```python
from app.alert_system import AlertLevel, create_alert

uploaded_file = st.file_uploader("Upload Report")

if uploaded_file is not None:
    try:
        # Try to read file
        df = pd.read_excel(uploaded_file)
        
        # Validate structure
        if len(df) == 0:
            create_alert(
                title="Empty File",
                message=f"File '{uploaded_file.name}' contains no data rows",
                level=AlertLevel.WARNING,
                category="file_validation",
                persistent=True,
                requires_action=True,
                action_label="Upload Different File"
            )
        elif df.isnull().sum().sum() > 0:
            null_count = df.isnull().sum().sum()
            create_alert(
                title="Missing Values Detected",
                message=f"File contains {null_count} missing values that may affect processing",
                level=AlertLevel.WARNING,
                category="data_quality",
                persistent=True,
                metadata={
                    'missing_cells': null_count,
                    'total_cells': df.size,
                    'impact': f"{(null_count/df.size)*100:.1f}%"
                }
            )
        else:
            create_alert(
                title="File Processed Successfully",
                message=f"✓ {uploaded_file.name} loaded with {len(df)} rows",
                level=AlertLevel.INFO,
                category="file_operations",
                metadata={'rows': len(df), 'columns': len(df.columns)}
            )
        
        # Continue processing
        process_report(df, uploaded_file.name)
                
    except Exception as e:
        create_alert(
            title="File Processing Failed",
            message=f"Unable to process file: {str(e)}",
            level=AlertLevel.ERROR,
            category="file_operations",
            persistent=True,
            requires_action=True,
            action_label="View Error Details",
            metadata={'error': str(e), 'file': uploaded_file.name}
        )
```

---

## Implementation Checklist

- [ ] Copy `app/alert_system.py` to your app folder
- [ ] Copy `app/alert_ui.py` to your app folder
- [ ] Update `app/app.py` imports to include alert system
- [ ] Create `data/alerts/` directory
- [ ] Replace 20-30 basic `st.success/warning/error` calls with `create_alert()`
- [ ] Add alert badge to sidebar
- [ ] Add alert dashboard to IT Administrator tab
- [ ] Add alert filtering to relevant sections
- [ ] Test persistence (alerts saved across sessions)
- [ ] Test role-based filtering
- [ ] Test alert acknowledgment tracking
- [ ] Train team on new alert system usage

---

## Benefits

1. **Better UX** - Consistent, professional alert presentation
2. **Audit Trail** - All alerts logged for compliance/debugging
3. **Role-Based** - Alerts only shown to relevant users
4. **Persistent** - Can review alert history
5. **Actionable** - Alerts can trigger workflows
6. **Routable** - Direct alerts to specific people/roles
7. **Configurable** - Adjust alert settings per role/context
8. **Dashboards** - Executive visibility into system health
9. **Export** - Generate reports from alert history
10. **Scalable** - Handles 50+ simultaneous alerts

---

## Future Enhancements

- Email notifications for CRITICAL alerts
- Slack/Teams integration for role-based routing
- Alert recipes/templates for common scenarios
- Machine learning to detect anomalies and auto-create alerts
- Alert escalation (e.g., if unacknowledged for 2 hours)
- Custom alert rules engine
- Performance metrics on alert response times
- Multi-language alert messages
- Alert webhooks for external system integration

---

## Technical Specifications

**File Structure:**
```
app/
  alert_system.py     # Core alert engine (300+ lines)
  alert_ui.py         # UI components (200+ lines)

data/
  alerts/
    alert_history.jsonl  # Persistent alert log
  alert_config.json      # Configuration file
```

**Storage:**
- Alerts stored in session state for immediate access
- Persistent alerts written to `alert_history.jsonl` (JSONL format)
- Configuration stored in `alert_config.json`
- History automatically pruned per retention policy

**Performance:**
- In-memory alert manager for <100ms response
- Lazy loading of history (only on dashboard load)
- Configurable max simultaneous alerts (default: 50)
- Automatic cleanup of expired alerts

**Security:**
- No PII in alert storage (only user IDs)
- Audit trail of who acknowledged what
- Role-based access to alert dashboard
- Encrypted alert history (recommended for production)

---

## Support & Questions

For questions on alert system implementation, refer to:
- `/docs/ALERT_SYSTEM_EXAMPLES.md` - Integration examples
- `/app/alert_system.py` - Inline documentation
- `/app/alert_ui.py` - Component reference
