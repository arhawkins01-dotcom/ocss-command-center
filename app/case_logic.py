from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import Any, Dict, Iterable, Mapping

import pandas as pd


ID_COLUMN_ALIASES: Dict[str, str] = {
    "sets": "sets_number",
    "setsnumber": "sets_number",
    "sets_number": "sets_number",
    "administrativecasenumber": "administrative_case_number",
    "administrative_case_number": "administrative_case_number",
    "pnumber": "administrative_case_number",
    "p_number": "administrative_case_number",
    "casenumber": "case_number",
    "case_number": "case_number",
    "participantname": "participant_name",
    "participant_name": "participant_name",
    "caseparty": "party_name",
    "partyname": "party_name",
    "party_name": "party_name",
    "partyrole": "party_role",
    "party_role": "party_role",
    "caseload": "caseload",
    "supportofficer": "support_officer",
    "support_officer": "support_officer",
    "supervisor": "supervisor",
    "unit": "unit",
    "servicedue": "service_due",
    "service_due": "service_due",
    "dateactiontaken": "date_action_taken",
    "date_action_taken": "date_action_taken",
    "actionstatus": "action_status",
    "action_status": "action_status",
    "casenarrated": "case_narrated",
    "case_narrated": "case_narrated",
}


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    return str(value).strip()


def normalize_identifier(value: Any) -> str:
    """Normalize identifier text for stable matching across messy uploads."""
    raw = _to_text(value).upper()
    if not raw:
        return ""
    return "".join(ch for ch in raw if ch.isalnum())


def _canonical_col_name(column_name: str) -> str:
    key = normalize_identifier(column_name).lower()
    return ID_COLUMN_ALIASES.get(key, key)


def _coerce_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce").dt.normalize()


def normalize_case_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize uploaded report data into analytics-ready shape."""
    if df is None or df.empty:
        return pd.DataFrame()

    normalized = df.copy()
    normalized.columns = [_canonical_col_name(c) for c in normalized.columns]

    for col in [
        "sets_number",
        "administrative_case_number",
        "case_number",
        "party_name",
        "participant_name",
        "party_role",
        "caseload",
        "support_officer",
        "supervisor",
        "unit",
        "action_status",
        "case_narrated",
    ]:
        if col not in normalized.columns:
            normalized[col] = ""
        normalized[col] = normalized[col].map(_to_text)

    for col in ["service_due", "date_action_taken"]:
        if col not in normalized.columns:
            normalized[col] = pd.NaT
        normalized[col] = _coerce_date(normalized[col])

    normalized["sets_number_norm"] = normalized["sets_number"].map(normalize_identifier)
    normalized["administrative_case_number_norm"] = normalized["administrative_case_number"].map(normalize_identifier)
    normalized["case_number_norm"] = normalized["case_number"].map(normalize_identifier)

    normalized["case_key"] = normalized.apply(build_case_key, axis=1)

    # Remove duplicates while preserving the row with the most recent action date.
    normalized["_dedupe_sort"] = normalized["date_action_taken"].fillna(pd.Timestamp.min)
    normalized = (
        normalized.sort_values("_dedupe_sort", ascending=False)
        .drop_duplicates(subset=["case_key", "party_name", "participant_name"], keep="first")
        .drop(columns=["_dedupe_sort"])
    )

    return normalized.reset_index(drop=True)


def build_case_key(row: Mapping[str, Any]) -> str:
    """Build a single cross-report case key from available identifiers."""
    sets_value = normalize_identifier(row.get("sets_number") or row.get("sets_number_norm"))
    admin_value = normalize_identifier(
        row.get("administrative_case_number") or row.get("administrative_case_number_norm")
    )
    case_value = normalize_identifier(row.get("case_number") or row.get("case_number_norm"))

    if sets_value:
        return f"SETS:{sets_value}"
    if admin_value:
        return f"P:{admin_value}"
    if case_value:
        return f"CASE:{case_value}"
    return "UNIDENTIFIED"


@dataclass(frozen=True)
class DeadlineClassification:
    label: str
    days_remaining: int | None


def classify_deadline(service_due: Any, today: date | datetime | None = None) -> DeadlineClassification:
    if today is None:
        today_dt = pd.Timestamp.now().normalize()
    else:
        today_dt = pd.Timestamp(today).normalize()

    due = pd.to_datetime(service_due, errors="coerce")
    if pd.isna(due):
        return DeadlineClassification(label="No Deadline", days_remaining=None)

    due = pd.Timestamp(due).normalize()
    days_remaining = int((due - today_dt).days)

    if days_remaining < 0:
        return DeadlineClassification(label="Overdue", days_remaining=days_remaining)
    if days_remaining <= 7:
        return DeadlineClassification(label="Approaching Deadline", days_remaining=days_remaining)
    return DeadlineClassification(label="On Track", days_remaining=days_remaining)


def derive_case_status(row: Mapping[str, Any], today: date | datetime | None = None) -> str:
    """Infer government workflow status from service, action, and due-date fields."""
    action_status = _to_text(row.get("action_status")).lower()
    action_date = pd.to_datetime(row.get("date_action_taken"), errors="coerce")
    due_state = classify_deadline(row.get("service_due"), today=today)

    if "closed" in action_status or "closure" in action_status:
        return "Closed"
    if pd.notna(action_date) or "complete" in action_status:
        return "Action Completed"
    if "genetic" in action_status or "gt" in action_status:
        return "Awaiting Genetic Testing"
    if "review" in action_status:
        return "Awaiting Review"
    if due_state.label in {"On Track", "Approaching Deadline", "Overdue"}:
        return "Awaiting Service"
    return "Pending Action"


def infer_workflow_stage(row: Mapping[str, Any]) -> str:
    action_status = _to_text(row.get("action_status")).lower()
    if "closed" in action_status or "maintenance" in action_status:
        return "Case Maintenance"
    if "genetic" in action_status or "gt" in action_status:
        return "Genetic Testing"
    if _to_text(row.get("order_number")) or "support order" in action_status:
        return "Support Order Establishment"
    if pd.notna(pd.to_datetime(row.get("service_due"), errors="coerce")):
        return "Service Process"
    return "Intake"


def build_case_relationship_model(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Build case-party-participant relationship tables from uploaded data."""
    clean = normalize_case_data(df)
    if clean.empty:
        empty = pd.DataFrame()
        return {"cases": empty, "case_parties": empty, "participant_cases": empty}

    clean["workflow_stage"] = clean.apply(infer_workflow_stage, axis=1)
    clean["derived_status"] = clean.apply(derive_case_status, axis=1)

    cases = (
        clean.groupby("case_key", as_index=False)
        .agg(
            sets_number=("sets_number", "first"),
            administrative_case_number=("administrative_case_number", "first"),
            case_number=("case_number", "first"),
            unit=("unit", "first"),
            support_officer=("support_officer", "first"),
            supervisor=("supervisor", "first"),
            current_status=("derived_status", "first"),
            workflow_stage=("workflow_stage", "first"),
        )
    )

    case_parties = clean[[
        "case_key",
        "party_name",
        "party_role",
        "participant_name",
    ]].copy()
    case_parties = case_parties[(case_parties["party_name"] != "") | (case_parties["participant_name"] != "")]
    case_parties = case_parties.drop_duplicates().reset_index(drop=True)

    participant_cases = (
        case_parties.assign(participant=case_parties["participant_name"].where(case_parties["participant_name"] != "", case_parties["party_name"]))
        .groupby("participant", as_index=False)
        .agg(
            case_count=("case_key", "nunique"),
            case_keys=("case_key", lambda vals: sorted(set(vals))),
        )
    )

    return {
        "cases": cases,
        "case_parties": case_parties,
        "participant_cases": participant_cases,
    }


def add_deadline_flags(df: pd.DataFrame, today: date | datetime | None = None) -> pd.DataFrame:
    clean = normalize_case_data(df)
    if clean.empty:
        return clean

    classifications = clean["service_due"].map(lambda due: classify_deadline(due, today=today))
    clean["deadline_status"] = classifications.map(lambda c: c.label)
    clean["days_remaining"] = classifications.map(lambda c: c.days_remaining)
    return clean


def summarize_deadlines(df: pd.DataFrame, today: date | datetime | None = None) -> Dict[str, int]:
    flagged = add_deadline_flags(df, today=today)
    if flagged.empty:
        return {
            "total": 0,
            "on_track": 0,
            "approaching_deadline": 0,
            "overdue": 0,
        }

    status_counts = flagged["deadline_status"].value_counts()
    return {
        "total": int(len(flagged)),
        "on_track": int(status_counts.get("On Track", 0)),
        "approaching_deadline": int(status_counts.get("Approaching Deadline", 0)),
        "overdue": int(status_counts.get("Overdue", 0)),
    }


def aggregate_caseload_accountability(df: pd.DataFrame) -> pd.DataFrame:
    clean = add_deadline_flags(df)
    if clean.empty:
        return pd.DataFrame(
            columns=[
                "unit",
                "supervisor",
                "support_officer",
                "total_caseload",
                "overdue_cases",
                "narration_completion_rate",
                "action_completion_rate",
            ]
        )

    clean["narrated_flag"] = clean["case_narrated"].str.lower().eq("yes")
    clean["action_completed_flag"] = clean.apply(
        lambda r: derive_case_status(r) == "Action Completed",
        axis=1,
    )

    group_cols = ["unit", "supervisor", "support_officer"]
    grouped = clean.groupby(group_cols, as_index=False).agg(
        total_caseload=("case_key", "nunique"),
        overdue_cases=("deadline_status", lambda values: int((pd.Series(values) == "Overdue").sum())),
        narration_completion_rate=("narrated_flag", lambda vals: round(float(pd.Series(vals).mean() * 100), 1) if len(vals) else 0.0),
        action_completion_rate=("action_completed_flag", lambda vals: round(float(pd.Series(vals).mean() * 100), 1) if len(vals) else 0.0),
    )
    return grouped.sort_values(["unit", "supervisor", "support_officer"]).reset_index(drop=True)


def merge_operational_reports(report_frames: Iterable[pd.DataFrame]) -> pd.DataFrame:
    """Merge multiple report datasets and keep most recent action per case."""
    normalized_frames = [normalize_case_data(df) for df in report_frames if df is not None and not df.empty]
    if not normalized_frames:
        return pd.DataFrame()

    merged = pd.concat(normalized_frames, ignore_index=True)
    merged["_sort_dt"] = merged["date_action_taken"].fillna(pd.Timestamp.min)
    merged = merged.sort_values("_sort_dt", ascending=False).drop_duplicates(subset=["case_key"], keep="first")
    merged = merged.drop(columns=["_sort_dt"])
    merged["derived_status"] = merged.apply(derive_case_status, axis=1)
    merged["workflow_stage"] = merged.apply(infer_workflow_stage, axis=1)
    return merged.reset_index(drop=True)


def search_cases(
    df: pd.DataFrame,
    *,
    query: str = "",
    case_number: str = "",
    sets_number: str = "",
    participant_name: str = "",
    caseload: str = "",
    support_officer: str = "",
) -> pd.DataFrame:
    """Fast flexible search across common government case-management fields."""
    clean = normalize_case_data(df)
    if clean.empty:
        return clean

    mask = pd.Series([True] * len(clean), index=clean.index)

    if query.strip():
        term = query.strip().lower()
        blob = (
            clean["case_number"].str.lower()
            + " "
            + clean["sets_number"].str.lower()
            + " "
            + clean["administrative_case_number"].str.lower()
            + " "
            + clean["participant_name"].str.lower()
            + " "
            + clean["party_name"].str.lower()
            + " "
            + clean["caseload"].str.lower()
            + " "
            + clean["support_officer"].str.lower()
        )
        mask &= blob.str.contains(term, na=False)

    if case_number.strip():
        key = normalize_identifier(case_number)
        mask &= clean["case_number_norm"].eq(key)

    if sets_number.strip():
        key = normalize_identifier(sets_number)
        mask &= clean["sets_number_norm"].eq(key)

    if participant_name.strip():
        term = participant_name.strip().lower()
        mask &= (
            clean["participant_name"].str.lower().str.contains(term, na=False)
            | clean["party_name"].str.lower().str.contains(term, na=False)
        )

    if caseload.strip():
        term = caseload.strip().lower()
        mask &= clean["caseload"].str.lower().eq(term)

    if support_officer.strip():
        term = support_officer.strip().lower()
        mask &= clean["support_officer"].str.lower().eq(term)

    result = clean[mask].copy()
    if result.empty:
        return result

    keep_cols = [
        "case_key",
        "sets_number",
        "administrative_case_number",
        "case_number",
        "participant_name",
        "party_name",
        "party_role",
        "unit",
        "caseload",
        "support_officer",
        "supervisor",
        "service_due",
        "date_action_taken",
        "action_status",
    ]
    available = [c for c in keep_cols if c in result.columns]
    return result[available].reset_index(drop=True)


def generate_operational_summary(df: pd.DataFrame, today: date | datetime | None = None) -> Dict[str, float]:
    flagged = add_deadline_flags(df, today=today)
    if flagged.empty:
        return {
            "total_cases_monitored": 0,
            "cases_requiring_action": 0,
            "overdue_cases": 0,
            "cases_awaiting_review": 0,
            "narration_completion_percentage": 0.0,
        }

    statuses = flagged.apply(derive_case_status, axis=1)
    awaiting_review = int((statuses == "Awaiting Review").sum())
    requiring_action = int(statuses.isin(["Pending Action", "Awaiting Service", "Awaiting Genetic Testing", "Awaiting Review"]).sum())
    overdue = int((flagged["deadline_status"] == "Overdue").sum())
    narration_rate = round(float(flagged["case_narrated"].str.lower().eq("yes").mean() * 100), 1) if len(flagged) else 0.0

    return {
        "total_cases_monitored": int(flagged["case_key"].nunique()),
        "cases_requiring_action": requiring_action,
        "overdue_cases": overdue,
        "cases_awaiting_review": awaiting_review,
        "narration_completion_percentage": narration_rate,
    }


def calculate_operational_health_score(df: pd.DataFrame, group_by: str = "unit") -> pd.DataFrame:
    """Compute leadership-friendly health score per unit/team."""
    accountability = aggregate_caseload_accountability(df)
    if accountability.empty or group_by not in accountability.columns:
        return pd.DataFrame(columns=[group_by, "health_score"])

    grouped = accountability.groupby(group_by, as_index=False).agg(
        total_caseload=("total_caseload", "sum"),
        overdue_cases=("overdue_cases", "sum"),
        narration_completion_rate=("narration_completion_rate", "mean"),
        action_completion_rate=("action_completion_rate", "mean"),
    )

    grouped["overdue_rate"] = grouped.apply(
        lambda r: (float(r["overdue_cases"]) / float(r["total_caseload"]) * 100.0) if float(r["total_caseload"]) > 0 else 0.0,
        axis=1,
    )

    # Weighted score: emphasizes action/narration completion while penalizing overdue risk.
    grouped["health_score"] = grouped.apply(
        lambda r: round(
            max(
                0.0,
                min(
                    100.0,
                    (0.45 * float(r["action_completion_rate"]))
                    + (0.35 * float(r["narration_completion_rate"]))
                    + (0.20 * (100.0 - float(r["overdue_rate"]))),
                ),
            ),
            1,
        ),
        axis=1,
    )

    return grouped[[group_by, "health_score", "total_caseload", "overdue_cases"]].sort_values(
        by=["health_score", group_by], ascending=[False, True]
    ).reset_index(drop=True)


def create_audit_entry(
    *,
    action: str,
    dataset: str,
    actor: str = "system",
    details: Mapping[str, Any] | None = None,
    when: datetime | None = None,
) -> Dict[str, Any]:
    """Create an audit-ready event record for uploads, processing, and updates."""
    ts = (when or datetime.utcnow()).isoformat(timespec="seconds") + "Z"
    return {
        "timestamp": ts,
        "action": _to_text(action),
        "dataset": _to_text(dataset),
        "actor": _to_text(actor) or "system",
        "details": dict(details or {}),
    }


def append_audit_entry(audit_log: list[Dict[str, Any]] | None, entry: Mapping[str, Any]) -> list[Dict[str, Any]]:
    log = list(audit_log or [])
    log.append(dict(entry))
    return log
