"""
Alert System Integration Examples
Shows how to use the alert system throughout the app
"""

import streamlit as st
from app.alert_system import AlertLevel, create_alert, get_alert_manager


# Example 1: Basic alert creation
def example_basic_alerts():
    """Show basic alert usage"""
    create_alert(
        title="File Uploaded Successfully",
        message="report_Q1_2026.xlsx has been processed",
        level=AlertLevel.SUCCESS,
        category="file_operations",
        dismissible=True
    )


# Example 2: Alert with metadata
def example_alert_with_metadata():
    """Alert with additional context"""
    create_alert(
        title="High Workload Detected",
        message="Michael Chen has exceeded recommended caseload",
        level=AlertLevel.WARNING,
        category="performance",
        persistent=True,
        metadata={
            'worker': 'Michael Chen',
            'current_load': '32 caseloads',
            'recommended_max': '25 caseloads',
            'overage': '7 caseloads',
            'action_required': 'true'
        }
    )


# Example 3: Alert requiring user action
def example_action_required_alert():
    """Alert that needs user response"""
    create_alert(
        title="CQI Alignment Review Needed",
        message="3 reports require CQI alignment verification before release",
        level=AlertLevel.WARNING,
        category="compliance",
        requires_action=True,
        action_label="Review Now",
        dismissible=False,
        persistent=True
    )


# Example 4: Role-specific alert
def example_role_specific_alert(role):
    """Alert targeted to specific role"""
    if role == "Supervisor":
        create_alert(
            title="Team Performance Report Ready",
            message="Monthly performance summary is available for review",
            level=AlertLevel.INFO,
            category="reporting",
            affected_role="Supervisor",
            dismissible=True,
            expires_in_seconds=86400  # 24 hours
        )


# Example 5: Critical system alert
def example_critical_alert():
    """System-level critical alert"""
    create_alert(
        title="Database Connection Error",
        message="Unable to connect to audit log database. Some functionality may be degraded.",
        level=AlertLevel.CRITICAL,
        category="system",
        dismissible=False,
        persistent=True,
        requires_action=True,
        action_label="Contact IT Support"
    )


# Example 6: User-specific alert
def example_user_alert(username):
    """Alert for specific user"""
    create_alert(
        title="Password Expiration Warning",
        message=f"Your password will expire in 7 days. Please update it soon.",
        level=AlertLevel.WARNING,
        category="security",
        affected_user=username,
        persistent=True
    )


# Example 7: Expiring alert
def example_temporary_alert():
    """Alert that auto-expires"""
    create_alert(
        title="Processing in Progress",
        message="Your report is being processed. This message will auto-dismiss.",
        level=AlertLevel.INFO,
        category="processing",
        dismissible=False,
        expires_in_seconds=30  # Auto-dismiss after 30 seconds
    )


# Integration patterns in app.py
def integration_pattern_file_upload():
    """How to use alerts in file upload handler"""
    code = '''
# In app.py file upload section:
from app.alert_system import AlertLevel, create_alert, get_alert_manager

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        # Check for validation issues
        if len(df) == 0:
            create_alert(
                title="Empty File",
                message=f"{uploaded_file.name} contains no data rows",
                level=AlertLevel.WARNING,
                category="file_validation"
            )
        elif df.isnull().sum().sum() > 0:
            null_count = df.isnull().sum().sum()
            create_alert(
                title="Missing Values Detected",
                message=f"File contains {null_count} missing values",
                level=AlertLevel.WARNING,
                category="data_quality",
                metadata={'missing_cells': null_count},
                persistent=True
            )
        else:
            create_alert(
                title="File Processed Successfully",
                message=f"✓ {uploaded_file.name} ready for processing",
                level=AlertLevel.INFO,
                category="file_operations"
            )
                
    except Exception as e:
        create_alert(
            title="File Processing Failed",
            message=str(e),
            level=AlertLevel.ERROR,
            category="file_operations",
            persistent=True,
            requires_action=True,
            action_label="View Error Details"
        )
    '''
    return code


def integration_pattern_caseload_assignment():
    """How to use alerts in caseload assignment logic"""
    code = '''
# In action_logic.py or assignment handler:
from app.alert_system import AlertLevel, create_alert

def assign_caseload(caseload_id, worker_name, unit_name):
    """Assign caseload with alerts"""
    
    # Check if already assigned
    existing = find_caseload_owner(caseload_id)
    if existing:
        create_alert(
            title="Caseload Already Assigned",
            message=f"Caseload {caseload_id} is assigned to {existing['person']} in {existing['unit']}",
            level=AlertLevel.WARNING,
            category="assignment",
            metadata={
                'caseload': caseload_id,
                'current_owner': existing['person'],
                'current_unit': existing['unit']
            }
        )
        return False
    
    # Check workload
    worker_load = count_worker_caseloads(worker_name)
    if worker_load >= 25:  # Max is 25
        create_alert(
            title="Workload Warning",
            message=f"{worker_name} already has {worker_load} caseloads (recommended max: 25)",
            level=AlertLevel.WARNING,
            category="workload",
            metadata={'worker': worker_name, 'current_load': worker_load},
            persistent=True
        )
    
    # Perform assignment
    perform_assignment(caseload_id, worker_name, unit_name)
    
    create_alert(
        title="Caseload Assigned",
        message=f"Caseload {caseload_id} assigned to {worker_name}",
        level=AlertLevel.SUCCESS,
        category="assignment"
    )
    
    return True
    '''
    return code


def integration_pattern_compliance_check():
    """How to use alerts for compliance validation"""
    code = '''
# In compliance checking logic:
from app.alert_system import AlertLevel, create_alert

def validate_cqi_alignment(report_data):
    """Validate CQI alignment with alerts"""
    
    issues = []
    
    # Check required fields
    required_fields = ['student_count', 'staff_count', 'grade_levels']
    for field in required_fields:
        if field not in report_data or report_data[field] is None:
            issues.append(f"Missing required field: {field}")
    
    if issues:
        create_alert(
            title="CQI Alignment Validation Failed",
            message="Report does not meet CQI alignment requirements",
            level=AlertLevel.ERROR,
            category="compliance",
            persistent=True,
            requires_action=True,
            action_label="Fix Report",
            metadata={'issues': ', '.join(issues)}
        )
        return False
    
    # Check data quality
    if report_data.get('completion_pct', 0) < 80:
        create_alert(
            title="Low Completion Rate",
            message=f"Report completion is only {report_data['completion_pct']}%",
            level=AlertLevel.WARNING,
            category="data_quality",
            metadata={'completion_rate': f"{report_data['completion_pct']}%"}
        )
    
    create_alert(
        title="CQI Alignment Verified",
        message="Report meets CQI alignment requirements",
        level=AlertLevel.SUCCESS,
        category="compliance"
    )
    
    return True
    '''
    return code


if __name__ == "__main__":
    print("Alert System Integration Examples")
    print("=" * 50)
    print()
    print("Example 1: File Upload Integration")
    print(integration_pattern_file_upload())
    print()
    print("Example 2: Caseload Assignment Integration")
    print(integration_pattern_caseload_assignment())
    print()
    print("Example 3: Compliance Check Integration")
    print(integration_pattern_compliance_check())
