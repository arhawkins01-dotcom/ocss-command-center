"""Report engine skeleton for the OCSS Command Center.

Responsibilities:
- Load/normalize report datasets
- Filter cases by caseload assignment
- Provide APIs to fetch assigned queues
- Apply decisions from `action_logic` and update case state

This is intentionally lightweight: concrete ingestion and persistence should be implemented
by the application layer (Streamlit, Flask, CLI) that imports these functions.
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class Case:
    report_id: str
    report_type: str
    payload: Dict[str, Any]
    assigned_to: Optional[str] = None
    status: str = "unassigned"
    narration: Optional[str] = None


def load_sample_cases() -> List[Case]:
    """Return a tiny in-memory sample list for demos and tests.

    In production this should read from the ingestion layer (DB, CSV, message queue).
    """
    return [
        Case(report_id="sample-1", report_type="56RA", payload={}),
        Case(report_id="sample-2", report_type="Locate", payload={}),
        Case(report_id="sample-3", report_type="P-S", payload={}),
    ]


def assign_cases(cases: List[Case], caseload_config: Dict[str, List[str]]) -> List[Case]:
    """Naive assignment: if a case lacks `assigned_to`, mark as `unassigned`.

    Real logic should use `caseload_config` to map cases to users/roles.
    """
    # This is a placeholder: do not persist here.
    for i, c in enumerate(cases):
        if c.assigned_to is None:
            c.assigned_to = None
            c.status = c.status or "unassigned"
    return cases


def get_assigned_queue(user: str, cases: List[Case]) -> List[Case]:
    return [c for c in cases if c.assigned_to == user]


def process_case(case: Case) -> Case:
    """Apply decision logic for a single case and return the updated case object."""
    from .action_logic import decide_next_action

    decision = decide_next_action(case)
    case.status = decision.get("status", case.status)
    case.narration = decision.get("narration", case.narration)
    return case
