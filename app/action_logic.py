"""Decision logic for Command Center report processing.

These functions are intentionally small and side-effect free. They accept a
`Case`-like object (from `report_engine`) and return a structured decision
dictionary: { 'action': str, 'status': str, 'narration': str }.

Make conservative decisions so existing app behavior is preserved when data
is incomplete. Add more rules incrementally and keep functions testable.
"""
from typing import Dict, Any


def _get_report_type(case: Any) -> str:
    rt = getattr(case, 'report_type', None)
    if not rt and hasattr(case, 'payload') and isinstance(case.payload, dict):
        rt = case.payload.get('report_type')
    return (rt or '').strip().upper()


def _safe_field(case: Any, key: str, default=None):
    if hasattr(case, 'payload') and isinstance(case.payload, dict):
        return case.payload.get(key, default)
    return getattr(case, key, default) if hasattr(case, key) else default


def _decide_56ra(case: Any, decision: Dict[str, str]) -> Dict[str, str]:
    decision['action'] = decision.get('action') or 'REVIEW_56RA'
    # Preserve existing status unless explicit close/completion signals present
    status = decision.get('status') or getattr(case, 'status', 'unassigned')

    paternity = _safe_field(case, 'paternity_status', '').lower() or ''
    gt_scheduled = bool(_safe_field(case, 'gt_scheduled', False))
    ads_ready = bool(_safe_field(case, 'ads_ready', False))

    if paternity == 'established' and not gt_scheduled and ads_ready:
        status = 'Ready for GT'
        narration = '56RA: Paternity established; prepare ADS and schedule GT.'
    elif paternity == 'established' and gt_scheduled:
        status = 'In Progress'
        narration = '56RA: GT scheduled; monitor until completed.'
    else:
        narration = decision.get('narration') or '56RA: review required. Verify paternity and schedule GT as appropriate.'

    decision['status'] = status
    if not decision.get('narration'):
        decision['narration'] = narration
    return decision


def _decide_locate(case: Any, decision: Dict[str, str]) -> Dict[str, str]:
    decision['action'] = decision.get('action') or 'REVIEW_LOCATE'
    status = decision.get('status') or getattr(case, 'status', 'unassigned')

    ilsu = (_safe_field(case, 'ilsu_status', '') or '').lower()
    located = bool(_safe_field(case, 'ncp_located', False))
    postal = _safe_field(case, 'postal_verification', None)

    if located:
        status = 'Located'
        narration = 'Locate: NCP located; advance workflow and document findings.'
    elif ilsu == 'clear' and postal == 'verified':
        status = 'Postal Verified'
        narration = 'Locate: ILSU cleared and postal verification complete.'
    else:
        narration = decision.get('narration') or 'Locate: run database clears, attempt contact, and evaluate UNL/NAS.'

    decision['status'] = status
    if not decision.get('narration'):
        decision['narration'] = narration
    return decision


def _decide_ps(case: Any, decision: Dict[str, str]) -> Dict[str, str]:
    decision['action'] = decision.get('action') or 'REVIEW_PS'
    status = decision.get('status') or getattr(case, 'status', 'unassigned')

    prior_contacts = int(_safe_field(case, 'prior_contact_attempts', 0) or 0)
    ads_ready = bool(_safe_field(case, 'ads_ready', False))
    court_criteria = bool(_safe_field(case, 'refer_to_court', False))

    if court_criteria:
        status = 'Pending Court Referral'
        narration = 'P-S: meets referral criteria; prepare court packet.'
    elif ads_ready and prior_contacts >= 2:
        status = 'Ready for ADS'
        narration = 'P-S: ADS ready and sufficient contact attempts; proceed.'
    else:
        narration = decision.get('narration') or 'P-S: follow P-S SOP for GT scheduling and ADS preparation.'

    decision['status'] = status
    if not decision.get('narration'):
        decision['narration'] = narration
    return decision


def decide_next_action(case) -> Dict[str, str]:
    """Return a conservative decision dict for the given case.

    The function tries to enrich decisions using available payload fields but
    falls back to no-op behavior when data is missing so it does not degrade
    existing application behavior.
    """
    report_type = _get_report_type(case)

    # Default safe decision: preserve existing status/narration
    decision = {
        'action': 'NO_OP',
        'status': getattr(case, 'status', 'unassigned'),
        'narration': getattr(case, 'narration', '') or ''
    }

    if report_type.startswith('56') or report_type == '56RA' or report_type == '56':
        return _decide_56ra(case, decision)

    if report_type == 'LOCATE' or report_type.startswith('LOCATE'):
        return _decide_locate(case, decision)

    if report_type in ('P-S', 'P-S REPORT') or report_type.startswith('P'):
        return _decide_ps(case, decision)

    return decision
