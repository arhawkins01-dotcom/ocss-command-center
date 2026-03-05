"""
Support Officer UI Helper Functions
Provides enhanced UI components for seamless report processing
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional


def render_report_type_badge(report_source: str) -> None:
    """Render a prominent visual badge indicating the report type."""
    badge_config = {
        'LOCATE': {
            'label': '🔵 LOCATE Report',
            'color': '#1E88E5',
            'bg': '#E3F2FD',
            'description': 'Locating absent parents - requires Date Reviewed, Results, Narration'
        },
        'PS': {
            'label': '🟢 P-S Report',
            'color': '#43A047',
            'bg': '#E8F5E9',
            'description': 'Parenting & Support - requires Action Taken, Narration'
        },
        '56': {
            'label': '🟠 56RA Report',
            'color': '#FB8C00',
            'bg': '#FFF3E0',
            'description': 'Establishment - requires Date Processed, Action Taken, Narration'
        },
        'CASE_CLOSURE': {
            'label': '🟣 Case Closure',
            'color': '#8E24AA',
            'bg': '#F3E5F5',
            'description': 'Closure Review - requires Y/N responses, Initials, Comments'
        },
    }

    config = badge_config.get(report_source, badge_config['LOCATE'])
    
    st.markdown(
        f"""
        <div style="
            background-color: {config['bg']};
            border-left: 4px solid {config['color']};
            padding: 12px 16px;
            margin: 8px 0 16px 0;
            border-radius: 4px;
        ">
            <div style="font-size: 18px; font-weight: 600; color: {config['color']}; margin-bottom: 4px;">
                {config['label']}
            </div>
            <div style="font-size: 14px; color: #555;">
                {config['description']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_required_fields_for_report_type(report_source: str) -> Dict[str, Any]:
    """Return required fields configuration for a given report type."""
    
    if report_source == 'CASE_CLOSURE':
        return {
            'type': 'Case Closure',
            'fields': [
                {'name': 'All F&Rs filed?', 'type': 'Y/N', 'always_required': True},
                {'name': 'Termination of Support needed?', 'type': 'Y/N', 'always_required': True},
                {'name': 'Minor child still exists?', 'type': 'Y/N', 'always_required': True},
                {'name': 'SETS updated?', 'type': 'Y/N', 'always_required': True},
                {'name': 'Unallocated Hold on PHAS?', 'type': 'Y/N', 'always_required': True},
                {'name': 'Hold release request to Post app?', 'type': 'Y/N', 'always_required': True},
                {'name': 'Did you propose closure?', 'type': 'Y/N', 'always_required': True},
                {'name': 'Initials', 'type': 'text', 'always_required': True},
                {'name': 'Comments', 'type': 'text', 'condition': 'Required if closure NOT proposed'},
            ]
        }
    elif report_source == 'PS':
        return {
            'type': 'P-S (Parenting & Support)',
            'fields': [
                {'name': 'Action Taken/Status', 'type': 'dropdown', 'always_required': True},
                {'name': 'Case Narrated', 'type': 'Yes/No', 'always_required': True, 'must_be': 'Yes'},
                {'name': 'Comment', 'type': 'text', 'condition': 'Required if Action = OTHER'},
            ]
        }
    elif report_source == '56':
        return {
            'type': '56RA (Establishment)',
            'fields': [
                {'name': 'Date Action Taken', 'type': 'date', 'always_required': True, 'display': 'Date Report was Processed'},
                {'name': 'Action Taken/Status', 'type': 'dropdown', 'always_required': True},
                {'name': 'Case Narrated', 'type': 'Yes/No', 'always_required': True, 'must_be': 'Yes'},
                {'name': 'Comment', 'type': 'text', 'condition': 'Required if Action = OTHER'},
            ]
        }
    else:  # LOCATE
        return {
            'type': 'LOCATE',
            'fields': [
                {'name': 'Date Case Reviewed', 'type': 'date', 'always_required': True},
                {'name': 'Results of Review', 'type': 'dropdown', 'always_required': True},
                {'name': 'Case Narrated', 'type': 'Yes/No', 'always_required': True, 'must_be': 'Yes'},
                {'name': 'Case Closure Code', 'type': 'dropdown', 'condition': 'If closing case'},
                {'name': 'Comment', 'type': 'text', 'condition': 'Required for closures/OTHER'},
            ]
        }


def render_required_fields_panel(report_source: str, current_row_data: Optional[Dict] = None) -> None:
    """Render an interactive panel showing required fields with completion status."""
    
    config = get_required_fields_for_report_type(report_source)
    
    with st.expander(f"📋 Required Fields for {config['type']}", expanded=True):
        st.markdown("**Complete these fields before marking row as 'Completed':**")
        st.markdown("")
        
        if current_row_data:
            for field in config['fields']:
                field_name = field['name']
                field_value = str(current_row_data.get(field_name, '')).strip()
                
                # Check if field is filled
                is_filled = bool(field_value and field_value not in ['nan', 'None', ''])
                
                # Special handling for "must_be" fields
                if field.get('must_be'):
                    is_filled = is_filled and field_value == field.get('must_be')
                
                # Status icon
                status_icon = "✅" if is_filled else "⬜"
                
                # Build field description
                field_desc = field_name
                if field.get('display'):
                    field_desc = f"{field['display']} ({field_name})"
                if field.get('must_be'):
                    field_desc += f" → must be '{field.get('must_be')}'"
                
                # Conditional requirement note
                condition_note = ""
                if not field.get('always_required') and field.get('condition'):
                    condition_note = f" *({field['condition']})*"
                    status_icon = "ℹ️" if not is_filled else "✅"
                
                st.markdown(f"{status_icon} **{field_desc}**{condition_note}")
        else:
            # No row data - just show the list
            for field in config['fields']:
                field_name = field['name']
                field_desc = field.get('display', field_name)
                
                if field.get('must_be'):
                    field_desc += f" → must be '{field.get('must_be' )}'"
                
                condition_note = ""
                if not field.get('always_required') and field.get('condition'):
                    condition_note = f" *({field['condition']})*"
                
                st.markdown(f"⬜ **{field_desc}**{condition_note}")


def get_narration_templates_for_report_type(report_source: str) -> List[Dict[str, str]]:
    """Return copy-paste narration templates specific to report type."""
    
    if report_source == '56':
        return [
            {
                'action': 'Scheduled GT',
                'template': 'Case pending GTU. Action taken: Scheduled GT. Next steps: follow up after appointment date __/__/____.',
            },
            {
                'action': 'Pending GTU',
                'template': 'Case pending GTU. Next steps: monitor GT queue and follow up.',
            },
            {
                'action': 'Pending Court',
                'template': 'PCR pending at court. Next hearing: __/__/____. Next steps: monitor docket and follow up.',
            },
            {
                'action': 'Sent COBO Letter(s)',
                'template': 'COBO. Sent COBO letter(s) to all parties. Deadline: __/__/____.',
            },
            {
                'action': 'Referred to Court',
                'template': 'Referred to court for establishment. Court date: __/__/____. Next steps: monitor and follow up.',
            },
        ]
    elif report_source == 'PS':
        return [
            {
                'action': 'CONTACT LETTER',
                'template': 'Contacted client via phone/web portal. Action taken: CONTACT LETTER. Next steps: follow up by __/__/____.',
            },
            {
                'action': 'GT',
                'template': 'Genetic testing scheduled. GT date: __/__/____. Next steps: verify completion and follow up.',
            },
            {
                'action': 'COURT REFERRAL',
                'template': 'Referred to court. Court date: __/__/____. Next steps: monitor docket.',
            },
            {
                'action': 'POSTAL',
                'template': 'Sent postal verification. Deadline: __/__/____. Next steps: follow up on response.',
            },
        ]
    else:  # LOCATE
        return [
            {
                'action': 'Cleared Databases',
                'template': 'Cleared BMV/SVES/dockets/ODRC/Work Number; no info. Contacted CP; no new address. Continue investigation.',
            },
            {
                'action': 'Closed UNL',
                'template': 'Cleared BMV/SVES/dockets/ODRC/Work Number; no info. Contacted CP; no new address. Case in locate 2+ years with SSN; closed UNL.',
            },
            {
                'action': 'Closed NAS',
                'template': 'Cleared databases; no info. No response from CP. Case in locate 6+ months without SSN; closed NAS.',
            },
            {
                'action': 'Located NCP',
                'template': 'Located NCP via [source]. Address: [address]. Next steps: process next action within 5 business days.',
            },
            {
                'action': 'CLEAR Requested',
                'template': 'Potential out-of-state. CLEAR request submitted __/__/____. Awaiting response.',
            },
        ]
    
    return []


def render_narration_templates(report_source: str) -> None:
    """Render quick-copy narration templates specific to report type."""
    
    templates = get_narration_templates_for_report_type(report_source)
    
    if not templates:
        return
    
    with st.expander("📝 Quick-Copy Narration Templates", expanded=False):
        st.caption("Click to copy, then paste into the Comment/Narration field:")
        
        for template_data in templates:
            with st.container():
                st.markdown(f"**{template_data['action']}:**")
                st.code(template_data['template'], language=None)
                st.markdown("---")


def calculate_row_completion_percentage(row_data: Dict, report_source: str) -> Tuple[int, List[str]]:
    """Calculate completion percentage and return list of missing fields."""
    
    config = get_required_fields_for_report_type(report_source)
    required_fields = [f for f in config['fields'] if f.get('always_required')]
    
    total = len(required_fields)
    completed = 0
    missing = []
    
    for field in required_fields:
        field_name = field['name']
        field_value = str(row_data.get(field_name, '')).strip()
        
        is_filled = bool(field_value and field_value not in ['nan', 'None', ''])
        
        # Special handling for "must_be" fields
        if field.get('must_be'):
            is_filled = is_filled and field_value == field.get('must_be')
        
        if is_filled:
            completed += 1
        else:
            display_name = field.get('display', field_name)
            if field.get('must_be'):
                display_name += f" (must be '{field.get('must_be')}')"
            missing.append(display_name)
    
    percentage = int((completed / total) * 100) if total > 0 else 0
    
    return percentage, missing


def render_row_progress_indicator(row_data: Dict, report_source: str) -> None:
    """Render a visual progress indicator for a single row."""
    
    percentage, missing = calculate_row_completion_percentage(row_data, report_source)
    
    # Color based on completion
    if percentage == 100:
        color = "#43A047"  # Green
        emoji = "✅"
        message = "Ready to mark Complete"
    elif percentage >= 50:
        color = "#FB8C00"  # Orange
        emoji = "🔄"
        message = f"{len(missing)} field(s) remaining"
    else:
        color = "#E53935"  # Red
        emoji = "⚠️"  
        message = f"{len(missing)} field(s) required"
    
    st.markdown(
        f"""
        <div style="
            background-color: {color}15;
            border-left: 3px solid {color};
            padding: 8px 12px;
            margin: 4px 0;
            border-radius: 3px;
        ">
            <div style="font-size: 14px; color: {color}; font-weight: 600;">
                {emoji} Row Completion: {percentage}%
            </div>
            <div style="font-size: 12px; color: #666; margin-top: 2px;">
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if missing and percentage < 100:
        with st.expander("Missing fields", expanded=False):
            for field in missing:
                st.markdown(f"- {field}")
