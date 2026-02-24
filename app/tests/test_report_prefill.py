import sys
import pathlib
import pandas as pd

# Ensure repository root is on path so `app` package can be imported
root = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))

from app import report_utils


def test_prefill_case_number_and_caseload():
    # Build a sample canonical-like dataframe
    df = pd.DataFrame({
        'case_number': ['7123456890', 'ABC7123456890', '0007123456'],
        'caseload': ['181000', '1100', '0181000'],
        'case_type': ['pa4a', 'NpFa', 'npmO'],
        'case_mode': ['S', 'p', 'something'],
        'service_due_date': [pd.NaT, pd.NaT, pd.NaT],
        'report_source': ['56', 'PS', '56']
    })

    wf = report_utils.canonical_to_workflow_dataframe(df)

    # Case Number should be digits only and the 56 source should keep 10-digit
    assert wf['Case Number'].iloc[0] == '7123456890'
    assert wf['Case Number'].iloc[1].isdigit()

    # Caseload short form: for 181000 -> 1000? Expect last 4 of 6-digit 18xxxx -> last 4
    # Our implementation returns short 4-digit when possible
    assert wf['Caseload'].iloc[0].isdigit()
    assert wf['Case Type'].iloc[0] == 'PA4A'
    assert wf['Case Mode'].iloc[1] == 'P' or wf['Case Mode'].iloc[1] == 'p'


def test_56_case_number_formatting():
    df = pd.DataFrame({'case_number': ['X7123456890123', '1234567890'], 'caseload': ['181000', '1100'], 'report_source': ['56', '56']})
    wf = report_utils.canonical_to_workflow_dataframe(df)
    # Long numeric case -> last 10 digits should be used
    assert wf['Case Number'].iloc[0] == '3456890123'
    assert wf['Case Number'].iloc[1] == '1234567890'


def test_locate_and_edge_cases():
    # LOCATE reports may not have case_mode/case_type; ensure service due and caseload parse
    df = pd.DataFrame({
        'case_number': ['0012345678', ''],
        'caseload': ['1100', '181000'],
        'case_type': ['', 'NPFA'],
        'case_mode': ['', 'S'],
        'service_due_date': [pd.NaT, pd.to_datetime('2026-03-01')],
        'report_source': ['LOCATE', 'LOCATE']
    })
    wf = report_utils.canonical_to_workflow_dataframe(df)
    assert wf['Case Number'].iloc[0].isdigit()
    assert wf['Caseload'].iloc[1].isdigit()
    assert wf['Service Due'].iloc[1] == pd.to_datetime('2026-03-01')
