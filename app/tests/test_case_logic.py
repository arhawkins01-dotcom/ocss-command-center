import os
import sys

import pandas as pd

# Ensure app modules are importable in this test layout.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from case_logic import (
    normalize_case_data,
    build_case_relationship_model,
    classify_deadline,
    summarize_deadlines,
    aggregate_caseload_accountability,
    merge_operational_reports,
    search_cases,
    generate_operational_summary,
    calculate_operational_health_score,
    create_audit_entry,
)


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "SETS Number": " 10-200-300 ",
                "P Number": "P-100",
                "Case Number": "C-1",
                "Party Name": "Alice Doe",
                "Party Role": "CP",
                "Participant Name": "Alice Doe",
                "Unit": "Unit 15",
                "Support Officer": "Worker A",
                "Supervisor": "Sup 1",
                "Caseload": "181001",
                "Service Due": "2026-03-10",
                "Date Action Taken": "",
                "Action Status": "Awaiting Service",
                "Case Narrated": "Yes",
            },
            {
                "SETS Number": "10200300",
                "P Number": "P-100",
                "Case Number": "C-1",
                "Party Name": "Bob Doe",
                "Party Role": "NCP",
                "Participant Name": "Bob Doe",
                "Unit": "Unit 15",
                "Support Officer": "Worker A",
                "Supervisor": "Sup 1",
                "Caseload": "181001",
                "Service Due": "2026-03-01",
                "Date Action Taken": "2026-03-02",
                "Action Status": "Action Completed",
                "Case Narrated": "No",
            },
            {
                "SETS Number": "",
                "P Number": "P-200",
                "Case Number": "C-2",
                "Party Name": "Carla Roe",
                "Party Role": "CP",
                "Participant Name": "Carla Roe",
                "Unit": "Unit 17",
                "Support Officer": "Worker B",
                "Supervisor": "Sup 2",
                "Caseload": "181002",
                "Service Due": "2026-02-20",
                "Date Action Taken": "",
                "Action Status": "Awaiting Review",
                "Case Narrated": "Yes",
            },
        ]
    )


def test_normalize_case_data_and_relationships():
    clean = normalize_case_data(_sample_df())
    assert not clean.empty
    assert "case_key" in clean.columns
    assert clean["sets_number_norm"].iloc[0] == "10200300"

    model = build_case_relationship_model(_sample_df())
    assert set(model.keys()) == {"cases", "case_parties", "participant_cases"}
    assert len(model["cases"]) >= 2
    assert (model["case_parties"]["party_name"] == "Alice Doe").any()


def test_deadline_classification_and_summary():
    c1 = classify_deadline("2026-03-08", today=pd.Timestamp("2026-03-07"))
    c2 = classify_deadline("2026-03-20", today=pd.Timestamp("2026-03-07"))
    c3 = classify_deadline("2026-03-01", today=pd.Timestamp("2026-03-07"))

    assert c1.label == "Approaching Deadline"
    assert c2.label == "On Track"
    assert c3.label == "Overdue"

    summary = summarize_deadlines(_sample_df(), today=pd.Timestamp("2026-03-07"))
    assert summary["total"] == 3
    assert summary["overdue"] == 2


def test_accountability_merge_search_and_summary():
    df = _sample_df()
    accountability = aggregate_caseload_accountability(df)
    assert not accountability.empty
    assert "narration_completion_rate" in accountability.columns

    newer = pd.DataFrame(
        [
            {
                "Case Number": "C-2",
                "P Number": "P-200",
                "Service Due": "2026-02-20",
                "Date Action Taken": "2026-03-07",
                "Action Status": "Action Completed",
                "Case Narrated": "Yes",
            }
        ]
    )

    merged = merge_operational_reports([df, newer])
    assert not merged.empty
    assert (merged["case_key"].str.contains("P:P200") | merged["case_key"].str.contains("CASE:C2")).any()

    searched = search_cases(df, participant_name="Carla")
    assert len(searched) == 1
    assert searched.iloc[0]["participant_name"] == "Carla Roe"

    summary = generate_operational_summary(df, today=pd.Timestamp("2026-03-07"))
    assert summary["total_cases_monitored"] == 2
    assert "narration_completion_percentage" in summary

    health = calculate_operational_health_score(df)
    assert not health.empty
    assert "health_score" in health.columns


def test_create_audit_entry_shape():
    entry = create_audit_entry(
        action="report_upload",
        dataset="establishment_report",
        actor="it_admin",
        details={"rows": 42},
        when=pd.Timestamp("2026-03-07T12:00:00"),
    )

    assert entry["action"] == "report_upload"
    assert entry["dataset"] == "establishment_report"
    assert entry["actor"] == "it_admin"
    assert entry["details"]["rows"] == 42
    assert entry["timestamp"].startswith("2026-03-07T12:00:00")
