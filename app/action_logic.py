"""Decision logic stubs for Command Center report processing.

These functions are intentionally small and side-effect free. They accept a
`Case`-like object (from `report_engine`) and return a structured decision
dictionary. Implement concrete rules incrementally and add unit tests for each
rule set.
"""
from typing import Dict


def decide_next_action(case) -> Dict[str, str]:
    """Return a decision dict for the given case.

    The returned structure should be:
      { 'action': str, 'status': str, 'narration': str }

    For now this implements minimal, conservative defaults to avoid changing
    existing application behavior.
    """
    report_type = getattr(case, 'report_type', '') or case.payload.get('report_type', '') if hasattr(case, 'payload') else ''
    report_type = (report_type or '').upper()

    # Default safe decision: no-op (preserve status/narration)
    decision = {
        'action': 'NO_OP',
        'status': getattr(case, 'status', 'unassigned'),
        'narration': getattr(case, 'narration', '') or ''
    }

    # Lightweight, non-invasive suggestions for demo/test usage
    if report_type.startswith('56') or report_type == '56RA' or report_type == '56':
        decision['action'] = 'REVIEW_56RA'
        decision['status'] = decision['status'] if decision['status'] != 'Completed' else 'Completed'
        if not decision['narration']:
            decision['narration'] = '56RA: review required. Verify paternity and schedule GT as appropriate.'

    elif report_type == 'LOCATE' or report_type.startswith('LOCATE'):
        decision['action'] = 'REVIEW_LOCATE'
        if not decision['narration']:
            decision['narration'] = 'Locate: run database clears, attempt contact, and evaluate UNL/NAS.'

    elif report_type == 'P-S' or report_type == 'P-S REPORT' or report_type.startswith('P'):
        decision['action'] = 'REVIEW_PS'
        if not decision['narration']:
            decision['narration'] = 'P-S: follow P-S SOP for GT scheduling and ADS preparation.'

    return decision
