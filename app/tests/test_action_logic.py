import sys
import os

# Ensure app package is importable when tests run in CI or locally
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from report_engine import Case
from action_logic import decide_next_action


def test_decide_56ra_default():
    c = Case(report_id='r1', report_type='56RA', payload={})
    dec = decide_next_action(c)
    assert dec['action'] in ('REVIEW_56RA', 'NO_OP')


def test_decide_56ra_paternity_established_ads_ready():
    c = Case(report_id='r2', report_type='56RA', payload={
        'paternity_status': 'Established',
        'gt_scheduled': False,
        'ads_ready': True
    })
    dec = decide_next_action(c)
    assert dec['status'] == 'Ready for GT'
    assert 'schedule GT' in dec['narration'] or 'Prepare ADS' in dec['narration'] or 'prepare ADS' in dec['narration']


def test_decide_locate_located():
    c = Case(report_id='r3', report_type='Locate', payload={
        'ncp_located': True
    })
    dec = decide_next_action(c)
    assert dec['status'] == 'Located'
    assert 'Located' in dec['narration'] or 'NCP located' in dec['narration']


def test_decide_ps_ready_for_ads():
    c = Case(report_id='r4', report_type='P-S', payload={
        'prior_contact_attempts': 2,
        'ads_ready': True,
        'refer_to_court': False
    })
    dec = decide_next_action(c)
    assert dec['status'] == 'Ready for ADS'
    assert 'ADS' in dec['narration']
