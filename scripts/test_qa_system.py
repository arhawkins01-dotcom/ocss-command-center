"""
QA System Integration Test
Validates core QA functionality without running full Streamlit app
"""

import sys
sys.path.insert(0, '/workspaces/ocss-command-center/app')

import pandas as pd
from qa_compliance import (
    OHIO_COMPLIANCE_CRITERIA,
    generate_qa_sample,
    score_case_compliance,
    calculate_worker_qa_metrics,
    calculate_agency_qa_metrics,
)


def test_compliance_criteria():
    """Test that all report types have compliance criteria."""
    print("Testing compliance criteria...")
    
    report_types = ['LOCATE', '56', 'PS', 'CASE_CLOSURE']
    for rt in report_types:
        assert rt in OHIO_COMPLIANCE_CRITERIA, f"Missing criteria for {rt}"
        criteria = OHIO_COMPLIANCE_CRITERIA[rt]
        assert 'report_name' in criteria
        assert 'regulatory_basis' in criteria
        assert 'criteria' in criteria
        assert len(criteria['criteria']) > 0
        
        # Verify criteria structure
        for c in criteria['criteria']:
            assert 'id' in c
            assert 'category' in c
            assert 'requirement' in c
            assert 'regulation' in c
            assert 'weight' in c
        
        print(f"  ✅ {rt}: {len(criteria['criteria'])} criteria defined")
    
    print("✅ All compliance criteria valid\n")


def test_qa_sampling():
    """Test QA sampling logic."""
    print("Testing QA sampling...")
    
    # Create sample data
    test_data = pd.DataFrame({
        'Assigned Worker': ['Alice'] * 10 + ['Bob'] * 10,
        'Worker Status': ['Completed'] * 18 + ['In Progress'] * 2,
        'Case Number': [f'CASE-{i:03d}' for i in range(1, 21)],
    })
    
    # Test Alice (10 completed cases)
    alice_sample = generate_qa_sample(test_data, 'Alice', 'RPT-001', sample_size=5)
    assert len(alice_sample) == 5, f"Expected 5 samples, got {len(alice_sample)}"
    print(f"  ✅ Alice: sampled 5 of 10 completed cases: {alice_sample}")
    
    # Test Bob (8 completed cases)
    bob_sample = generate_qa_sample(test_data, 'Bob', 'RPT-001', sample_size=5)
    assert len(bob_sample) == 5, f"Expected 5 samples, got {len(bob_sample)}"
    print(f"  ✅ Bob: sampled 5 of 8 completed cases: {bob_sample}")
    
    # Test deterministic sampling (same seed should produce same results)
    alice_sample2 = generate_qa_sample(test_data, 'Alice', 'RPT-001', sample_size=5)
    assert alice_sample == alice_sample2, "Sampling should be deterministic"
    print(f"  ✅ Deterministic: same seed produces same sample")
    
    # Test small dataset (< 5 cases)
    small_data = pd.DataFrame({
        'Assigned Worker': ['Charlie'] * 3,
        'Worker Status': ['Completed'] * 3,
        'Case Number': ['CASE-A', 'CASE-B', 'CASE-C'],
    })
    charlie_sample = generate_qa_sample(small_data, 'Charlie', 'RPT-002', sample_size=5)
    assert len(charlie_sample) == 3, "Should sample all cases when < 5 available"
    print(f"  ✅ Charlie: sampled all 3 cases (< 5 available)")
    
    print("✅ QA sampling logic working correctly\n")


def test_compliance_scoring():
    """Test compliance scoring for each report type."""
    print("Testing compliance scoring...")
    
    # Test LOCATE report
    locate_case = pd.Series({
        'Comment': 'Cleared BMV, SVES, Work Number, ODRC. Contacted CP.',
        'Results of Review': 'Closed UNL',
        'Case Narrated': 'Yes',
        'Date Case Reviewed': '2026-03-01',
        'Case Closure Code': 'UNL',
    })
    locate_score = score_case_compliance(locate_case, 'LOCATE')
    assert 'percentage' in locate_score
    assert 'criteria_results' in locate_score
    print(f"  ✅ LOCATE: {locate_score['percentage']}% ({locate_score['total_score']}/{locate_score['max_score']} pts)")
    
    # Test 56RA report
    est_case = pd.Series({
        'Action Taken/Status': 'Scheduled GT',
        'Case Narrated': 'Yes',
        'Comment': 'GT scheduled for next Tuesday.',
        'Date Action Taken': '2026-03-01',
    })
    est_score = score_case_compliance(est_case, '56')
    assert est_score['percentage'] > 0
    print(f"  ✅ 56RA: {est_score['percentage']}% ({est_score['total_score']}/{est_score['max_score']} pts)")
    
    # Test P-S report
    ps_case = pd.Series({
        'Action Taken/Status': 'CONTACT LETTER',
        'Case Narrated': 'Yes',
        'Comment': 'Sent contact letter via certified mail.',
    })
    ps_score = score_case_compliance(ps_case, 'PS')
    assert ps_score['percentage'] > 0
    print(f"  ✅ P-S: {ps_score['percentage']}% ({ps_score['total_score']}/{ps_score['max_score']} pts)")
    
    # Test Case Closure
    closure_case = pd.Series({
        'All F&Rs filed?': 'Y',
        'Termination of Support needed?': 'N',
        'Minor child still exists?': 'N',
        'SETS updated?': 'Y',
        'Unallocated Hold on PHAS?': 'N',
        'Hold release request to Post app?': 'N',
        'Did you propose closure?': 'Y',
        'Initials': 'JD',
        'Comments': 'All requirements met for closure.',
    })
    closure_score = score_case_compliance(closure_case, 'CASE_CLOSURE')
    assert closure_score['percentage'] > 0
    print(f"  ✅ CASE_CLOSURE: {closure_score['percentage']}% ({closure_score['total_score']}/{closure_score['max_score']} pts)")
    
    print("✅ Compliance scoring working for all report types\n")


def test_metrics_calculations():
    """Test QA metrics calculations."""
    print("Testing metrics calculations...")
    
    # Mock session state (would normally be st.session_state)
    mock_reviews = {
        'RPT001_Alice_5': {
            'worker_name': 'Alice',
            'compliance_score': {
                'percentage': 92.0,
                'total_score': 92.0,
                'max_score': 100.0,
            }
        },
        'RPT001_Alice_8': {
            'worker_name': 'Alice',
            'compliance_score': {
                'percentage': 87.0,
                'total_score': 87.0,
                'max_score': 100.0,
            }
        },
        'RPT001_Bob_3': {
            'worker_name': 'Bob',
            'compliance_score': {
                'percentage': 65.0,
                'total_score': 65.0,
                'max_score': 100.0,
            }
        },
    }
    
    # Inject into module's internal state (for testing only)
    import streamlit as st
    if not hasattr(st, 'session_state'):
        # Create mock session state for testing
        class MockSessionState(dict):
            def __getattr__(self, key):
                return self.get(key)
            def __setattr__(self, key, value):
                self[key] = value
        st.session_state = MockSessionState()
    
    st.session_state.qa_reviews = mock_reviews
    st.session_state.qa_samples = {}
    
    # Test worker metrics
    alice_metrics = calculate_worker_qa_metrics('Alice')
    assert alice_metrics['cases_reviewed'] == 2
    assert alice_metrics['avg_compliance'] == 89.5  # (92 + 87) / 2
    print(f"  ✅ Alice metrics: {alice_metrics['cases_reviewed']} cases, {alice_metrics['avg_compliance']}% avg")
    
    bob_metrics = calculate_worker_qa_metrics('Bob')
    assert bob_metrics['cases_reviewed'] == 1
    assert bob_metrics['avg_compliance'] == 65.0
    print(f"  ✅ Bob metrics: {bob_metrics['cases_reviewed']} cases, {bob_metrics['avg_compliance']}% avg")
    
    # Test agency metrics
    agency_metrics = calculate_agency_qa_metrics()
    assert agency_metrics['total_cases_reviewed'] == 3
    expected_avg = (92 + 87 + 65) / 3  # 81.33
    assert abs(agency_metrics['avg_compliance_score'] - expected_avg) < 0.1
    print(f"  ✅ Agency metrics: {agency_metrics['total_cases_reviewed']} cases, {agency_metrics['avg_compliance_score']}% avg")
    
    print("✅ Metrics calculations working correctly\n")


def main():
    """Run all QA system tests."""
    print("=" * 70)
    print("QA SYSTEM INTEGRATION TEST")
    print("=" * 70)
    print()
    
    try:
        test_compliance_criteria()
        test_qa_sampling()
        test_compliance_scoring()
        test_metrics_calculations()
        
        print("=" * 70)
        print("✅ ALL TESTS PASSED - QA SYSTEM READY FOR PRODUCTION")
        print("=" * 70)
        return 0
    
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
