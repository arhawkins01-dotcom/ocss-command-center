"""
Quality Assurance and Compliance Tracking System
Implements Ohio OAC/ORC/OCSE compliance checks and automated QA sampling
"""

import streamlit as st
import pandas as pd
import random
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
import hashlib


# ═══════════════════════════════════════════════════════════════════════════
# OHIO CHILD SUPPORT COMPLIANCE CRITERIA
# Based on Ohio Administrative Code (OAC), Ohio Revised Code (ORC), and OCSE
# ═══════════════════════════════════════════════════════════════════════════

OHIO_COMPLIANCE_CRITERIA = {
    'LOCATE': {
        'report_name': 'Locate Absent Parents',
        'regulatory_basis': 'Ohio OAC 5101:12-1-30, ORC 3125.25, OCSE-AT-06-02',
        'criteria': [
            {
                'id': 'LOC-01',
                'category': 'Database Searches',
                'requirement': 'All state databases checked (BMV, SVES, Work Number, ODRC)',
                'regulation': 'OCSE-AT-06-02 § 2.1',
                'weight': 20,
                'check_field': 'Comment',
                'check_logic': 'contains_any',
                'check_values': ['BMV', 'SVES', 'Work Number', 'ODRC', 'databases cleared'],
            },
            {
                'id': 'LOC-02',
                'category': 'CP Contact',
                'requirement': 'Custodial parent contacted for information (OAC 5101:12-1-30)',
                'regulation': 'Ohio OAC 5101:12-1-30(A)(1)',
                'weight': 15,
                'check_field': 'Comment',
                'check_logic': 'contains_any',
                'check_values': ['CP', 'contacted', 'custodial parent', 'spoke with'],
            },
            {
                'id': 'LOC-03',
                'category': 'Timeframes',
                'requirement': 'Cases in locate for 6+ months without SSN require closure (NAS)',
                'regulation': 'ORC 3125.25(B)',
                'weight': 20,
                'check_field': 'Results of Review',
                'check_logic': 'closure_timeframe',
                'check_values': ['Closed NAS', 'NAS'],
            },
            {
                'id': 'LOC-04',
                'category': 'SSN Cases',
                'requirement': 'Cases with SSN in locate 2+ years require closure (UNL)',
                'regulation': 'Ohio OAC 5101:12-1-30(D)',
                'weight': 20,
                'check_field': 'Results of Review',
                'check_logic': 'closure_timeframe',
                'check_values': ['Closed UNL', 'UNL'],
            },
            {
                'id': 'LOC-05',
                'category': 'Narration',
                'requirement': 'Case narrative documents all locate actions and sources',
                'regulation': 'OCSE-AT-06-02 § 3.2',
                'weight': 15,
                'check_field': 'Case Narrated',
                'check_logic': 'equals',
                'check_values': ['Yes', 'Y'],
            },
            {
                'id': 'LOC-06',
                'category': 'Interstate',
                'requirement': 'CLEAR/Interstate requests for out-of-state leads',
                'regulation': 'OCSE-AT-06-02 § 2.3',
                'weight': 10,
                'check_field': 'Comment',
                'check_logic': 'contains_any',
                'check_values': ['CLEAR', 'interstate', 'out-of-state', 'other state'],
            },
        ],
    },
    '56': {
        'report_name': '56RA Establishment Reports',
        'regulatory_basis': 'Ohio OAC 5101:12-45-03, ORC 3111.04, OCSE PIQ-06-02',
        'criteria': [
            {
                'id': 'EST-01',
                'category': 'Service Requirements',
                'requirement': 'Proper service documented (ADS, personal, certified mail)',
                'regulation': 'Ohio OAC 5101:12-45-03(C)',
                'weight': 20,
                'check_field': 'Action Taken/Status',
                'check_logic': 'contains_any',
                'check_values': ['ADS', 'Scheduled GT', 'Prepped ADS', 'personal service'],
            },
            {
                'id': 'EST-02',
                'category': 'Genetic Testing',
                'requirement': 'GT scheduled within 30 days of PCR filing (paternity cases)',
                'regulation': 'ORC 3111.04(A)(1)',
                'weight': 25,
                'check_field': 'Action Taken/Status',
                'check_logic': 'contains_any',
                'check_values': ['Scheduled GT', 'GT', 'Pending GTU', 'genetic testing'],
            },
            {
                'id': 'EST-03',
                'category': 'Admin Hearing',
                'requirement': 'Admin hearing process (AHU) for IV-D cases',
                'regulation': 'Ohio OAC 5101:12-45-05',
                'weight': 15,
                'check_field': 'Action Taken/Status',
                'check_logic': 'contains_any',
                'check_values': ['AHU', 'Admin Hearing', 'Pending AHU'],
            },
            {
                'id': 'EST-04',
                'category': 'Court Referral',
                'requirement': 'Timely court referral with complete documentation',
                'regulation': 'ORC 3111.04(B)',
                'weight': 15,
                'check_field': 'Action Taken/Status',
                'check_logic': 'contains_any',
                'check_values': ['Referred to Court', 'Court', 'PCR'],
            },
            {
                'id': 'EST-05',
                'category': 'COBO Requirements',
                'requirement': 'COBO (Change of Benefitted Obligor) letters sent to all parties',
                'regulation': 'Ohio OAC 5101:12-45-03(F)',
                'weight': 10,
                'check_field': 'Comment',
                'check_logic': 'contains_any',
                'check_values': ['COBO', 'sent COBO', 'letter'],
            },
            {
                'id': 'EST-06',
                'category': 'Narration',
                'requirement': 'Complete case narration with next steps documented',
                'regulation': 'OCSE PIQ-06-02 § 4.1',
                'weight': 15,
                'check_field': 'Case Narrated',
                'check_logic': 'equals',
                'check_values': ['Yes', 'Y'],
            },
        ],
    },
    'PS': {
        'report_name': 'Parenting & Support (P-S) Reports',
        'regulatory_basis': 'Ohio OAC 5101:12-45-10, ORC 3119.05, OCSE Action Transmittal 08-01',
        'criteria': [
            {
                'id': 'PS-01',
                'category': 'Client Contact',
                'requirement': 'Client contact attempted via multiple methods',
                'regulation': 'Ohio OAC 5101:12-45-10(A)',
                'weight': 20,
                'check_field': 'Action Taken/Status',
                'check_logic': 'contains_any',
                'check_values': ['CONTACT LETTER', 'contacted', 'phone', 'web portal', 'letter'],
            },
            {
                'id': 'PS-02',
                'category': 'Genetic Testing',
                'requirement': 'GT scheduled if paternity contested',
                'regulation': 'ORC 3111.04',
                'weight': 25,
                'check_field': 'Action Taken/Status',
                'check_logic': 'contains_any',
                'check_values': ['GT', 'genetic testing', 'paternity test'],
            },
            {
                'id': 'PS-03',
                'category': 'Service of Process',
                'requirement': 'Proper service via ADS or certified mail',
                'regulation': 'Ohio OAC 5101:12-45-10(C)',
                'weight': 15,
                'check_field': 'Action Taken/Status',
                'check_logic': 'contains_any',
                'check_values': ['ADS', 'service', 'certified mail'],
            },
            {
                'id': 'PS-04',
                'category': 'Court Referral',
                'requirement': 'Timely court referral when admin process unsuccessful',
                'regulation': 'Ohio OAC 5101:12-45-10(E)',
                'weight': 20,
                'check_field': 'Action Taken/Status',
                'check_logic': 'contains_any',
                'check_values': ['COURT REFERRAL', 'referred to court', 'court'],
            },
            {
                'id': 'PS-05',
                'category': 'Postal Verification',
                'requirement': 'Address verification via postal service when needed',
                'regulation': 'OCSE-AT-08-01 § 2.4',
                'weight': 10,
                'check_field': 'Action Taken/Status',
                'check_logic': 'contains_any',
                'check_values': ['POSTAL', 'postal verification', 'address verification'],
            },
            {
                'id': 'PS-06',
                'category': 'Narration',
                'requirement': 'Case narrative with follow-up dates documented',
                'regulation': 'OCSE-AT-08-01 § 3.1',
                'weight': 10,
                'check_field': 'Case Narrated',
                'check_logic': 'equals',
                'check_values': ['Yes', 'Y'],
            },
        ],
    },
    'CASE_CLOSURE': {
        'report_name': 'Case Closure Review',
        'regulatory_basis': 'Ohio OAC 5101:12-1-50, ORC 3121.89, OCSE-PIQ-10-03',
        'criteria': [
            {
                'id': 'CLO-01',
                'category': 'F&R Documentation',
                'requirement': 'All F&Rs (findings and recommendations) filed with court',
                'regulation': 'Ohio OAC 5101:12-1-50(A)',
                'weight': 20,
                'check_field': 'All F&Rs filed?',
                'check_logic': 'equals',
                'check_values': ['Y', 'Yes'],
            },
            {
                'id': 'CLO-02',
                'category': 'Support Termination',
                'requirement': 'Termination of support order when child(ren) emancipated',
                'regulation': 'ORC 3121.89',
                'weight': 15,
                'check_field': 'Termination of Support needed?',
                'check_logic': 'answered',
                'check_values': ['Y', 'N'],
            },
            {
                'id': 'CLO-03',
                'category': 'Child Status',
                'requirement': 'Verification that minor child still exists in case',
                'regulation': 'Ohio OAC 5101:12-1-50(B)(1)',
                'weight': 15,
                'check_field': 'Minor child still exists?',
                'check_logic': 'equals',
                'check_values': ['N', 'No'],
            },
            {
                'id': 'CLO-04',
                'category': 'SETS System',
                'requirement': 'SETS (Support Enforcement Tracking System) updated',
                'regulation': 'OCSE-PIQ-10-03 § 2.1',
                'weight': 15,
                'check_field': 'SETS updated?',
                'check_logic': 'equals',
                'check_values': ['Y', 'Yes'],
            },
            {
                'id': 'CLO-05',
                'category': 'Holds Release',
                'requirement': 'Unallocated holds on PHAS released properly',
                'regulation': 'Ohio OAC 5101:12-1-50(C)',
                'weight': 15,
                'check_field': 'Hold release request to Post app?',
                'check_logic': 'answered',
                'check_values': ['Y', 'N'],
            },
            {
                'id': 'CLO-06',
                'category': 'Closure Justification',
                'requirement': 'Closure proposal with documented justification',
                'regulation': 'Ohio OAC 5101:12-1-50(D)',
                'weight': 20,
                'check_field': 'Comments',
                'check_logic': 'not_empty_if_no_proposal',
                'check_values': [],
            },
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# QA SAMPLING LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def generate_qa_sample(
    report_data: pd.DataFrame,
    worker_name: str,
    report_id: str,
    sample_size: int = 5,
) -> List[int]:
    """
    Generate deterministic QA sample of case rows for a specific worker.
    
    Returns list of row indices to review.
    Uses report_id + worker_name as seed for reproducibility.
    """
    if report_data.empty:
        return []
    
    # Filter to completed rows for this worker
    worker_rows = report_data[
        (report_data['Assigned Worker'].astype(str).str.strip() == worker_name) &
        (report_data['Worker Status'].astype(str).str.strip() == 'Completed')
    ]
    
    if len(worker_rows) == 0:
        return []
    
    # Take all rows if fewer than sample_size
    if len(worker_rows) <= sample_size:
        return worker_rows.index.tolist()
    
    # Deterministic sampling based on report_id + worker_name
    seed_str = f"{report_id}_{worker_name}"
    seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed_hash)
    
    sampled_indices = rng.sample(worker_rows.index.tolist(), sample_size)
    return sorted(sampled_indices)


def get_qa_samples_for_report(
    report_dict: Dict,
    sample_size: int = 5,
) -> Dict[str, List[int]]:
    """
    Generate QA samples for all workers in a report.
    
    Returns: {worker_name: [list of row indices]}
    """
    report_data = report_dict.get('data')
    report_id = str(report_dict.get('report_id', ''))
    
    if not isinstance(report_data, pd.DataFrame) or report_data.empty:
        return {}
    
    if 'Assigned Worker' not in report_data.columns:
        return {}
    
    # Get unique workers with completed rows
    workers = report_data[
        report_data['Worker Status'].astype(str).str.strip() == 'Completed'
    ]['Assigned Worker'].astype(str).str.strip().unique()
    
    samples = {}
    for worker in workers:
        if not worker or worker in ['', 'nan']:
            continue
        sample_indices = generate_qa_sample(report_data, worker, report_id, sample_size)
        if sample_indices:
            samples[worker] = sample_indices
    
    return samples


# ═══════════════════════════════════════════════════════════════════════════
# COMPLIANCE CHECKING LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def check_compliance_criterion(
    row_data: pd.Series,
    criterion: Dict,
) -> Tuple[bool, str]:
    """
    Check if a case row meets a specific compliance criterion.
    
    Returns: (passes: bool, explanation: str)
    """
    check_field = criterion.get('check_field', '')
    check_logic = criterion.get('check_logic', '')
    check_values = criterion.get('check_values', [])
    
    if check_field not in row_data:
        return False, f"Field '{check_field}' not found"
    
    field_value = str(row_data.get(check_field, '')).strip().lower()
    
    if check_logic == 'contains_any':
        # Check if any of the check_values appear in the field
        for check_val in check_values:
            if str(check_val).lower() in field_value:
                return True, f"Found '{check_val}'"
        return False, f"None of {check_values} found in '{row_data.get(check_field)}'"
    
    elif check_logic == 'equals':
        # Check if field equals any of the check_values
        for check_val in check_values:
            if field_value == str(check_val).lower():
                return True, f"Equals '{check_val}'"
        return False, f"Does not equal {check_values}. Found: '{row_data.get(check_field)}'"
    
    elif check_logic == 'answered':
        # Check if field has any value (Y or N)
        if field_value in [str(v).lower() for v in check_values]:
            return True, f"Answered: '{row_data.get(check_field)}'"
        return False, f"Not answered or invalid. Found: '{row_data.get(check_field)}'"
    
    elif check_logic == 'not_empty_if_no_proposal':
        # Special logic for closure: comment required if closure not proposed
        proposal_field = row_data.get('Did you propose closure?', '')
        if str(proposal_field).strip().upper() in ['Y', 'YES']:
            return True, "Closure proposed - comment optional"
        # If not proposed, comment must exist
        if field_value and field_value not in ['', 'nan', 'none']:
            return True, "Comment provided for non-proposed closure"
        return False, "Closure not proposed but no comment provided"
    
    elif check_logic == 'closure_timeframe':
        # Check if appropriate closure code used
        # This is a simplified check - real implementation would need case age data
        for check_val in check_values:
            if str(check_val).lower() in field_value:
                return True, f"Appropriate closure: '{check_val}'"
        return False, f"Closure code not found. Expected one of: {check_values}"
    
    else:
        return False, f"Unknown check logic: {check_logic}"


def score_case_compliance(
    row_data: pd.Series,
    report_source: str,
) -> Dict[str, Any]:
    """
    Score a single case row against all compliance criteria for report type.
    
    Returns: {
        'total_score': float,
        'max_score': float,
        'percentage': float,
        'criteria_results': [{criterion, passed, explanation, weight, points_earned}]
    }
    """
    criteria_config = OHIO_COMPLIANCE_CRITERIA.get(report_source)
    if not criteria_config:
        return {
            'total_score': 0.0,
            'max_score': 0.0,
            'percentage': 0.0,
            'criteria_results': [],
            'error': f'Unknown report source: {report_source}'
        }
    
    criteria = criteria_config['criteria']
    results = []
    total_score = 0.0
    max_score = 0.0
    
    for criterion in criteria:
        weight = criterion.get('weight', 10)
        max_score += weight
        
        passed, explanation = check_compliance_criterion(row_data, criterion)
        points_earned = weight if passed else 0.0
        total_score += points_earned
        
        results.append({
            'criterion_id': criterion['id'],
            'category': criterion['category'],
            'requirement': criterion['requirement'],
            'regulation': criterion['regulation'],
            'weight': weight,
            'passed': passed,
            'points_earned': points_earned,
            'explanation': explanation,
        })
    
    percentage = (total_score / max_score * 100) if max_score > 0 else 0.0
    
    return {
        'total_score': total_score,
        'max_score': max_score,
        'percentage': round(percentage, 1),
        'criteria_results': results,
    }


# ═══════════════════════════════════════════════════════════════════════════
# QA DATA MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

def init_qa_storage():
    """Initialize QA storage in session state."""
    if 'qa_reviews' not in st.session_state:
        st.session_state.qa_reviews = {}
    if 'qa_samples' not in st.session_state:
        st.session_state.qa_samples = {}


def store_qa_review(
    report_id: str,
    worker_name: str,
    row_index: int,
    compliance_score: Dict,
    reviewer_name: str,
    reviewer_notes: str = '',
):
    """Store a QA review result."""
    init_qa_storage()
    
    review_key = f"{report_id}_{worker_name}_{row_index}"
    
    st.session_state.qa_reviews[review_key] = {
        'report_id': report_id,
        'worker_name': worker_name,
        'row_index': row_index,
        'compliance_score': compliance_score,
        'reviewer_name': reviewer_name,
        'reviewer_notes': reviewer_notes,
        'review_date': datetime.now().isoformat(),
    }


def get_qa_review(report_id: str, worker_name: str, row_index: int) -> Optional[Dict]:
    """Retrieve a QA review if it exists."""
    init_qa_storage()
    review_key = f"{report_id}_{worker_name}_{row_index}"
    return st.session_state.qa_reviews.get(review_key)


def generate_and_store_qa_samples(report_dict: Dict, sample_size: int = 5):
    """Generate QA samples for a report and store them."""
    init_qa_storage()
    
    report_id = str(report_dict.get('report_id', ''))
    if not report_id:
        return
    
    samples = get_qa_samples_for_report(report_dict, sample_size)
    if samples:
        st.session_state.qa_samples[report_id] = samples


def get_qa_samples(report_id: str) -> Dict[str, List[int]]:
    """Retrieve QA samples for a report."""
    init_qa_storage()
    return st.session_state.qa_samples.get(report_id, {})


# ═══════════════════════════════════════════════════════════════════════════
# QA METRICS AND REPORTING
# ═══════════════════════════════════════════════════════════════════════════

def calculate_worker_qa_metrics(worker_name: str) -> Dict[str, Any]:
    """Calculate QA metrics for a specific worker across all reports."""
    init_qa_storage()
    
    worker_reviews = [
        review for review in st.session_state.qa_reviews.values()
        if review['worker_name'] == worker_name
    ]
    
    if not worker_reviews:
        return {
            'cases_reviewed': 0,
            'avg_compliance': 0.0,
            'pass_rate': 0.0,
            'total_score': 0.0,
            'max_score': 0.0,
        }
    
    total_score = sum(r['compliance_score']['total_score'] for r in worker_reviews)
    max_score = sum(r['compliance_score']['max_score'] for r in worker_reviews)
    passing_threshold = 75.0
    
    passes = sum(1 for r in worker_reviews if r['compliance_score']['percentage'] >= passing_threshold)
    
    return {
        'cases_reviewed': len(worker_reviews),
        'avg_compliance': round(total_score / max_score * 100, 1) if max_score > 0 else 0.0,
        'pass_rate': round(passes / len(worker_reviews) * 100, 1) if worker_reviews else 0.0,
        'total_score': total_score,
        'max_score': max_score,
    }


def calculate_agency_qa_metrics(department: Optional[str] = None) -> Dict[str, Any]:
    """Calculate agency-wide or department-level QA metrics."""
    init_qa_storage()
    
    all_reviews = list(st.session_state.qa_reviews.values())
    
    # Filter by department if specified
    if department:
        # Would need to cross-reference with report ownership
        # For now, include all reviews
        pass
    
    if not all_reviews:
        return {
            'total_cases_reviewed': 0,
            'avg_compliance_score': 0.0,
            'pass_rate': 0.0,
            'workers_reviewed': 0,
            'criteria_breakdown': {},
        }
    
    total_score = sum(r['compliance_score']['total_score'] for r in all_reviews)
    max_score = sum(r['compliance_score']['max_score'] for r in all_reviews)
    passing_threshold = 75.0
    
    passes = sum(1 for r in all_reviews if r['compliance_score']['percentage'] >= passing_threshold)
    unique_workers = len(set(r['worker_name'] for r in all_reviews))
    
    # Category breakdown
    category_scores = {}
    for review in all_reviews:
        for criterion in review['compliance_score']['criteria_results']:
            category = criterion['category']
            if category not in category_scores:
                category_scores[category] = {'passed': 0, 'total': 0}
            category_scores[category]['total'] += 1
            if criterion['passed']:
                category_scores[category]['passed'] += 1
    
    criteria_breakdown = {
        cat: round(scores['passed'] / scores['total'] * 100, 1) if scores['total'] > 0 else 0.0
        for cat, scores in category_scores.items()
    }
    
    return {
        'total_cases_reviewed': len(all_reviews),
        'avg_compliance_score': round(total_score / max_score * 100, 1) if max_score > 0 else 0.0,
        'pass_rate': round(passes / len(all_reviews) * 100, 1) if all_reviews else 0.0,
        'workers_reviewed': unique_workers,
        'criteria_breakdown': criteria_breakdown,
    }


def get_compliance_issues_by_category(report_source: str) -> List[str]:
    """Get list of common compliance issues for a report type."""
    init_qa_storage()
    
    issues = []
    for review in st.session_state.qa_reviews.values():
        if review['compliance_score'].get('error'):
            continue
        
        for criterion in review['compliance_score']['criteria_results']:
            if not criterion['passed']:
                issues.append(f"{criterion['category']}: {criterion['requirement']}")
    
    # Return unique issues sorted by frequency
    from collections import Counter
    issue_counts = Counter(issues)
    return [issue for issue, count in issue_counts.most_common(10)]


# ═══════════════════════════════════════════════════════════════════════════
# AUTO-TRIGGER QA SAMPLING
# ═══════════════════════════════════════════════════════════════════════════

def auto_qa_sampling_on_submit(report_dict: Dict):
    """
    Automatically trigger QA sampling when a report is submitted for review.
    Call this function when worker clicks "Submit Caseload as Complete".
    """
    report_status = str(report_dict.get('status', '')).lower()
    
    # Only sample when moving to "Submitted for Review" status
    if 'submitted' in report_status or 'review' in report_status:
        generate_and_store_qa_samples(report_dict, sample_size=5)


# ═══════════════════════════════════════════════════════════════════════════
# SUPERVISOR QA VALIDATION & SUMMARY TRACKING
# Per-Worker QA Results with Full Case Details
# ═══════════════════════════════════════════════════════════════════════════

def init_supervisor_qa_storage():
    """Initialize supervisor QA validation storage."""
    if 'supervisor_qa_validations' not in st.session_state:
        st.session_state.supervisor_qa_validations = {}
    if 'worker_qa_summaries' not in st.session_state:
        st.session_state.worker_qa_summaries = {}


def store_supervisor_qa_validation(
    report_id: str,
    worker_name: str,
    supervisor_name: str,
    validation_status: str,
    validation_notes: str = '',
    validation_date: Optional[str] = None,
) -> None:
    """
    Store supervisor's validation of worker's QA findings.
    
    validation_status: 'Approved', 'Challenge', or 'Needs Review'
    Stores per-worker validation metadata for supervisor summary reports.
    """
    init_supervisor_qa_storage()
    
    validation_key = f"{report_id}_{worker_name}"
    validation_date = validation_date or datetime.now().isoformat()
    
    st.session_state.supervisor_qa_validations[validation_key] = {
        'report_id': report_id,
        'worker_name': worker_name,
        'supervisor_name': supervisor_name,
        'validation_status': validation_status,  # Approved | Challenge | Needs Review
        'validation_notes': validation_notes,
        'validation_date': validation_date,
    }


def get_supervisor_qa_validation(report_id: str, worker_name: str) -> Optional[Dict]:
    """Retrieve supervisor's validation for a worker's QA results."""
    init_supervisor_qa_storage()
    validation_key = f"{report_id}_{worker_name}"
    return st.session_state.supervisor_qa_validations.get(validation_key)


def get_worker_qa_summary(
    report_id: str,
    worker_name: str,
    report_data: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Generate comprehensive QA summary for a specific worker in a report.
    
    Returns:
        {
            'worker_name': str,
            'report_id': str,
            'total_completed': int,
            'total_sampled': int,
            'avg_compliance': float,
            'pass_rate': float,
            'cases': [
                {
                    'case_number': str,
                    'case_type': str,
                    'compliance_score': float,
                    'status': str (Passed/Failed),
                    'actions_taken': str,
                    'comments': str,
                    'reviewed': bool,
                    'reviewer': str,
                }
            ],
            'supervisor_validation': Optional[Dict],
        }
    """
    init_qa_storage()
    init_supervisor_qa_storage()
    
    # Filter to completed rows for this worker
    worker_completed = report_data[
        (report_data['Assigned Worker'].astype(str).str.strip() == worker_name) &
        (report_data['Worker Status'].astype(str).str.strip() == 'Completed')
    ]
    
    total_completed = len(worker_completed)
    
    # Get QA samples for this worker
    qa_samples = get_qa_samples(report_id)
    worker_sample_indices = qa_samples.get(worker_name, [])
    total_sampled = len(worker_sample_indices)
    
    # Get all QA reviews for this worker
    worker_reviews = [
        review for review in st.session_state.qa_reviews.values()
        if review['report_id'] == report_id and review['worker_name'] == worker_name
    ]
    
    # Build case-level details
    cases = []
    total_compliance = 0.0
    max_compliance = 0.0
    passed_count = 0
    
    for idx in worker_sample_indices:
        if idx in report_data.index:
            row = report_data.loc[idx]
            case_number = str(row.get('Case Number', row.get('Case Row ID', f'Row {idx}')))
            
            # Get QA review if exists
            review = next((r for r in worker_reviews if r['row_index'] == idx), None)
            
            # Extract actions taken based on report type
            actions_taken = row.get('Action Taken/Status', '')
            if not actions_taken:
                actions_taken = row.get('Results of Review', '')
            
            case_detail = {
                'case_number': case_number,
                'case_type': str(row.get('Case Type', row.get('Case Mode', 'N/A'))),
                'date_processed': str(row.get('Date Action Taken', row.get('Date Case Reviewed ', ''))),
                'actions_taken': str(actions_taken),
                'comments': str(row.get('Comment', row.get('Comments', ''))),
                'qa_flag': str(row.get('QA Flag', '')),
                'reviewed': review is not None,
                'reviewer': review['reviewer_name'] if review else '',
                'review_date': review['review_date'] if review else '',
            }
            
            if review:
                compliance_pct = review['compliance_score'].get('percentage', 0.0)
                case_detail['compliance_score'] = compliance_pct
                case_detail['status'] = 'Passed' if compliance_pct >= 75.0 else 'Failed'
                total_compliance += compliance_pct
                max_compliance += 100.0
                if compliance_pct >= 75.0:
                    passed_count += 1
            else:
                case_detail['compliance_score'] = None
                case_detail['status'] = 'Pending Review'
            
            cases.append(case_detail)
    
    # Calculate aggregated metrics
    avg_compliance = (total_compliance / max_compliance * 100) if max_compliance > 0 else 0.0
    pass_rate = (passed_count / len(worker_reviews) * 100) if len(worker_reviews) > 0 else 0.0
    
    # Get supervisor validation if exists
    supervisor_validation = get_supervisor_qa_validation(report_id, worker_name)
    
    return {
        'worker_name': worker_name,
        'report_id': report_id,
        'total_completed': total_completed,
        'total_sampled': total_sampled,
        'cases_reviewed': len(worker_reviews),
        'avg_compliance': round(avg_compliance, 1),
        'pass_rate': round(pass_rate, 1),
        'cases': cases,
        'supervisor_validation': supervisor_validation,
    }


def generate_supervisor_qa_summary_dataframe(
    report_id: str,
    report_data: pd.DataFrame,
    qa_samples: Dict[str, List[int]],
) -> pd.DataFrame:
    """
    Generate a comprehensive summary dataframe for supervisor review.
    One row per QA case showing all worker completion details.
    """
    init_qa_storage()
    
    summary_rows = []
    
    for worker_name, sample_indices in qa_samples.items():
        for idx in sample_indices:
            if idx in report_data.index:
                row = report_data.loc[idx]
                
                # Get QA review
                qa_review = get_qa_review(report_id, worker_name, idx)
                
                summary_rows.append({
                    'Report ID': report_id,
                    'Worker': worker_name,
                    'Case Number': str(row.get('Case Number', row.get('Case Row ID', ''))),
                    'Case Type': str(row.get('Case Type', row.get('Case Mode', ''))),
                    'Actions Taken': str(row.get('Action Taken/Status', row.get('Results of Review', ''))),
                    'Comments': str(row.get('Comment', row.get('Comments', ''))),
                    'QA Flag': str(row.get('QA Flag', '')),
                    'Compliance %': qa_review['compliance_score']['percentage'] if qa_review else 'Pending',
                    'Status': 'Passed' if (qa_review and qa_review['compliance_score']['percentage'] >= 75.0) else ('Failed' if qa_review else 'Pending'),
                    'Reviewed By': qa_review['reviewer_name'] if qa_review else '',
                    'Review Date': qa_review['review_date'][:10] if qa_review else '',
                })
    
    if summary_rows:
        return pd.DataFrame(summary_rows)
    else:
        return pd.DataFrame()
