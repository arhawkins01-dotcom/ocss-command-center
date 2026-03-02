import sys
import pathlib

# Ensure repository root is on path so `app` package can be imported
root = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))

from app import report_utils


def test_validate_locate_requires_core_fields():
    row = {
        'Case Narrated': 'No',
        'Date Case Reviewed': '',
        'Results of Review': '',
        'Case Closure Code': '',
        'Comment': '',
    }
    issues = report_utils.validate_support_workflow_row_completion('LOCATE', row)
    assert 'Case Narrated must be Yes' in issues
    assert 'Date Case Reviewed is required for Locate' in issues
    assert 'Results of Review is required for Locate' in issues


def test_validate_locate_other_results_needs_comment():
    row = {
        'Case Narrated': 'Yes',
        'Date Case Reviewed': '2026-03-01',
        'Results of Review': 'OTHER',
        'Case Closure Code': '',
        'Comment': '',
    }
    issues = report_utils.validate_support_workflow_row_completion('Locate', row)
    assert 'Comment required when Results of Review = OTHER' in issues


def test_validate_locate_unl_needs_comment():
    row = {
        'Case Narrated': 'Yes',
        'Date Case Reviewed': '2026-03-01',
        'Results of Review': 'Closed UNL (2+ years w/ SSN)',
        'Case Closure Code': 'UNL',
        'Comment': '',
    }
    issues = report_utils.validate_support_workflow_row_completion('LOCATE', row)
    assert any('Comment required' in it for it in issues)


def test_validate_ps_requires_action_and_narration():
    row = {
        'Case Narrated': '',
        'Action Taken/Status': '',
        'Comment': '',
    }
    issues = report_utils.validate_support_workflow_row_completion('PS', row)
    assert 'Case Narrated must be Yes' in issues
    assert 'Action Taken/Status is required for PS/56 when Completed' in issues


def test_validate_ps_other_requires_comment():
    row = {
        'Case Narrated': 'Yes',
        'Action Taken/Status': 'OTHER',
        'Comment': '',
    }
    issues = report_utils.validate_support_workflow_row_completion('PS', row)
    assert 'Comment required when Action Taken/Status = OTHER' in issues


def test_validate_56_requires_date_action_taken():
    row = {
        'Case Narrated': 'Yes',
        'Action Taken/Status': 'Scheduled GT',
        'Date Action Taken': '',
        'Comment': '',
    }
    issues = report_utils.validate_support_workflow_row_completion('56', row)
    assert 'Date Action Taken is required for 56 when Completed' in issues


def test_validate_case_closure_requires_all_yn_and_initials():
    row = {
        'All F&Rs filed?': '',
        'Termination of Support needed?': 'Y',
        'Minor child still exists?': 'N',
        'SETS updated?': 'Y',
        'Unallocated Hold on PHAS?': 'Y',
        'Hold release request to Post app?': 'N',
        'Did you propose closure?': 'Y',
        'Initials': '',
        'Comments': '',
    }
    issues = report_utils.validate_support_workflow_row_completion('CASE_CLOSURE', row)
    assert any('All F&Rs filed?' in it for it in issues)
    assert 'Initials is required' in issues


def test_validate_case_closure_requires_comments_when_not_proposed():
    row = {
        'All F&Rs filed?': 'Y',
        'Termination of Support needed?': 'N',
        'Minor child still exists?': 'N',
        'SETS updated?': 'Y',
        'Unallocated Hold on PHAS?': 'N',
        'Hold release request to Post app?': 'N',
        'Did you propose closure?': 'N',
        'Initials': 'AB',
        'Comments': '',
    }
    issues = report_utils.validate_support_workflow_row_completion('CASE_CLOSURE', row)
    assert 'Comments required when closure is not proposed' in issues
