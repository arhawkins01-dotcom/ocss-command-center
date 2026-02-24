"""
Report processing utilities for OCSS Command Center
Handles Excel/CSV file processing, validation, and data manipulation
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import io
import json
import logging
import re
import hashlib

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


EXCEL_PARITY_REPORT_SOURCES = ('56', 'PS', 'LOCATE')


def _as_clean_str(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ''
    return str(value).strip()


def _upper_clean(value: Any) -> str:
    text = _as_clean_str(value)
    return text.upper() if text else ''


def _parse_date_series(series: pd.Series) -> pd.Series:
    if series is None:
        return pd.Series(dtype='datetime64[ns]')
    parsed = pd.to_datetime(series, errors='coerce')
    return parsed.dt.normalize()


def _parse_case_narrated_series(series: pd.Series) -> pd.Series:
    # Returns pandas BooleanDtype series with <NA> for blanks/unrecognized.
    if series is None:
        return pd.Series(pd.array([], dtype='boolean'))
    values = series.astype(str).str.strip().str.lower()
    truthy = {'y', 'yes', 'true', '1'}
    falsy = {'n', 'no', 'false', '0'}
    out = []
    for item in values.tolist():
        if not item or item == 'nan' or item == 'none':
            out.append(pd.NA)
        elif item in truthy:
            out.append(True)
        elif item in falsy:
            out.append(False)
        else:
            out.append(pd.NA)
    return pd.Series(pd.array(out, dtype='boolean'))


def detect_report_source(df: Optional[pd.DataFrame]) -> str:
    """Detect the report source (56 / PS / LOCATE) based on header signature."""
    if df is None or df.empty:
        return 'UNKNOWN'

    header_keys = {_normalize_header_key(col) for col in df.columns}

    if 'setsnumber' in header_keys and 'servicedue' in header_keys:
        return '56'
    if 'resultsofreview' in header_keys or 'caseclosurecode' in header_keys:
        return 'LOCATE'
    if {'casenumber', 'casetype', 'casemode'}.issubset(header_keys):
        return 'PS'
    return 'UNKNOWN'


def _first_matching_column(df: pd.DataFrame, normalized_candidates: List[str]) -> Optional[str]:
    if df is None or df.empty:
        return None
    by_key: Dict[str, str] = {}
    for col in df.columns:
        key = _normalize_header_key(col)
        if key and key not in by_key:
            by_key[key] = col
    for cand in normalized_candidates:
        if cand in by_key:
            return by_key[cand]
    return None


def map_dataframe_to_canonical(
    df: Optional[pd.DataFrame],
    fallback_caseload: str,
    source_filename: str = '',
    sheet_name: str = '',
    ingestion_id: str = '',
    imported_at: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Map an uploaded report dataframe into the canonical model.

    Returns a dict containing:
    - report_source
    - canonical_df
    - qa_summary
    - unknown_columns
    """
    imported_at = imported_at or datetime.now()
    if df is None:
        df = pd.DataFrame()

    report_source = detect_report_source(df)
    working = df.copy() if isinstance(df, pd.DataFrame) else pd.DataFrame()

    # Resolve source columns
    sets_col = _first_matching_column(working, ['setsnumber', 'sets'])
    case_col = _first_matching_column(working, ['casenumber', 'caseid'])
    caseload_col = _first_matching_column(working, ['caseload', 'caseloadnumber'])
    mode_col = _first_matching_column(working, ['mode', 'casemode'])
    type_col = _first_matching_column(working, ['type', 'casetype'])
    service_due_col = _first_matching_column(working, ['servicedue'])
    action_date_col = _first_matching_column(working, ['dateactiontaken', 'datecasereviewed', 'reviewdate'])
    status_col = _first_matching_column(working, ['actiontakenstatus', 'actiontaken', 'status', 'resultsofreview', 'reviewresult'])
    closure_col = _first_matching_column(working, ['caseclosurecode', 'closurecode'])
    narrated_col = _first_matching_column(working, ['casenarrated', 'narrated'])
    comment_col = _first_matching_column(working, ['comment', 'comments'])

    # Build canonical dataframe
    canonical = pd.DataFrame(index=working.index.copy()) if not working.empty else pd.DataFrame()

    if report_source == '56' and sets_col:
        canonical['case_number'] = working[sets_col].astype(str)
    elif case_col:
        canonical['case_number'] = working[case_col].astype(str)
    else:
        canonical['case_number'] = ''

    if caseload_col:
        canonical['caseload'] = working[caseload_col].apply(normalize_caseload_number)
    else:
        canonical['caseload'] = normalize_caseload_number(fallback_caseload)

    canonical['case_mode'] = working[mode_col].astype(str).fillna('').str.strip().str.upper() if mode_col else ''
    canonical['case_type'] = working[type_col].astype(str).fillna('').str.strip().str.upper() if type_col else ''

    canonical['service_due_date'] = _parse_date_series(working[service_due_col]) if service_due_col else pd.NaT
    canonical['action_taken_date'] = _parse_date_series(working[action_date_col]) if action_date_col else pd.NaT

    if status_col:
        canonical['action_taken_status'] = working[status_col].astype(str).fillna('').astype(str)
    else:
        canonical['action_taken_status'] = ''

    if closure_col:
        canonical['case_closure_code'] = working[closure_col].astype(str).fillna('')
    else:
        canonical['case_closure_code'] = ''

    canonical['case_narrated'] = _parse_case_narrated_series(working[narrated_col]) if narrated_col else pd.Series(pd.array([pd.NA] * len(canonical), dtype='boolean'))
    canonical['comment'] = working[comment_col].astype(str).fillna('') if comment_col else ''
    canonical['report_source'] = report_source
    canonical['activity_date'] = canonical['action_taken_date']
    if 'service_due_date' in canonical.columns:
        canonical['activity_date'] = canonical['activity_date'].fillna(canonical['service_due_date'])

    canonical['ingestion_id'] = str(ingestion_id or '')
    canonical['source_filename'] = str(source_filename or '')
    canonical['sheet_name'] = str(sheet_name or '')
    canonical['imported_at'] = imported_at.isoformat()

    # QA summary
    qa = {
        'report_source': report_source,
        'rows_raw': int(len(working)),
        'rows_canonical': int(len(canonical)),
        'missing_case_number': 0,
        'invalid_service_due_date': 0,
        'invalid_action_taken_date': 0,
        'invalid_case_narrated': 0,
        'duplicate_rows': 0,
    }

    if not canonical.empty:
        case_blank = canonical['case_number'].astype(str).str.strip().eq('')
        qa['missing_case_number'] = int(case_blank.sum())

        if service_due_col:
            raw = working[service_due_col].astype(str).str.strip()
            bad = raw.ne('') & canonical['service_due_date'].isna()
            qa['invalid_service_due_date'] = int(bad.sum())

        if action_date_col:
            raw = working[action_date_col].astype(str).str.strip()
            bad = raw.ne('') & canonical['action_taken_date'].isna()
            qa['invalid_action_taken_date'] = int(bad.sum())

        if narrated_col:
            raw = working[narrated_col].astype(str).str.strip().str.lower()
            allowed = {'', 'nan', 'none', 'y', 'yes', 'true', '1', 'n', 'no', 'false', '0'}
            qa['invalid_case_narrated'] = int((~raw.isin(list(allowed))).sum())

        dup_key_cols = ['report_source', 'case_number', 'caseload', 'service_due_date', 'action_taken_date', 'action_taken_status']
        for col in dup_key_cols:
            if col not in canonical.columns:
                canonical[col] = ''
        qa['duplicate_rows'] = int(canonical.duplicated(subset=dup_key_cols, keep=False).sum())

    used_cols = {c for c in [sets_col, case_col, caseload_col, mode_col, type_col, service_due_col, action_date_col, status_col, closure_col, narrated_col, comment_col] if c}
    unknown_columns = [c for c in (working.columns.tolist() if not working.empty else []) if c not in used_cols]

    return {
        'report_source': report_source,
        'canonical_df': canonical,
        'qa_summary': qa,
        'unknown_columns': unknown_columns,
    }


def apply_excel_parity_flags(canonical_df: Optional[pd.DataFrame]) -> pd.DataFrame:
    if canonical_df is None:
        return pd.DataFrame()
    df = canonical_df.copy()

    def _ensure_series(col_name: str, default: Any = '') -> pd.Series:
        val = df.get(col_name, default)
        if isinstance(val, pd.Series):
            # Ensure consistent string dtype for textual columns
            try:
                return val.astype(str).fillna('')
            except Exception:
                return val.fillna('').astype(str)
        # scalar -> broadcast to series
        return pd.Series([str(val) if val is not None else ''] * len(df), index=df.index)
    if df.empty:
        return df

    def _blank(col: str) -> pd.Series:
        if col not in df.columns:
            return pd.Series([True] * len(df), index=df.index)
        return df[col].astype(str).str.strip().eq('')

    df['flag_MISSING_CASE_NUMBER'] = _blank('case_number')

    # case_narrated is boolean with <NA>. Missing or False -> fail.
    if 'case_narrated' in df.columns:
        narrated = df['case_narrated']
        missing_or_false = narrated.isna() | (narrated == False)  # noqa: E712
        df['flag_NARRATION_MISSING'] = missing_or_false
    else:
        df['flag_NARRATION_MISSING'] = True

    df['flag_MISSING_ACTIVITY_DATE'] = df.get('activity_date', pd.Series([pd.NaT] * len(df), index=df.index)).isna()

    service = df.get('service_due_date')
    action = df.get('action_taken_date')
    if service is not None and action is not None:
        try:
            delta_days = (pd.to_datetime(action, errors='coerce') - pd.to_datetime(service, errors='coerce')).dt.days
            df['flag_MISSED_90_DAY_TIMEFRAME'] = delta_days > 90
        except Exception:
            df['flag_MISSED_90_DAY_TIMEFRAME'] = False
    else:
        df['flag_MISSED_90_DAY_TIMEFRAME'] = False

    is_locate = df.get('report_source', '').astype(str).eq('LOCATE')
    df['flag_LOCATE_REVIEW_REQUIRED'] = is_locate & _blank('action_taken_status')
    df['flag_LOCATE_CLOSURE_CODE_MISSING'] = is_locate & _blank('case_closure_code')

    rule_order = [
        'MISSING_CASE_NUMBER',
        'NARRATION_MISSING',
        'MISSED_90_DAY_TIMEFRAME',
        'MISSING_ACTIVITY_DATE',
        'LOCATE_REVIEW_REQUIRED',
        'LOCATE_CLOSURE_CODE_MISSING',
    ]

    def _severity_for_row(row: pd.Series) -> str:
        if bool(row.get('flag_MISSING_CASE_NUMBER')) or bool(row.get('flag_NARRATION_MISSING')) or bool(row.get('flag_MISSED_90_DAY_TIMEFRAME')):
            return 'FAIL'
        if bool(row.get('flag_MISSING_ACTIVITY_DATE')) or bool(row.get('flag_LOCATE_REVIEW_REQUIRED')):
            return 'WARN'
        if bool(row.get('flag_LOCATE_CLOSURE_CODE_MISSING')):
            return 'INFO'
        return 'OK'

    def _reasons_for_row(row: pd.Series) -> str:
        reasons = []
        for rid in rule_order:
            if bool(row.get(f'flag_{rid}', False)):
                reasons.append(rid)
        return ','.join(reasons)

    df['flag_severity'] = df.apply(_severity_for_row, axis=1)
    df['flag_reasons'] = df.apply(_reasons_for_row, axis=1)
    return df


def canonical_to_workflow_dataframe(canonical_df: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Convert canonical rows into the workflow-friendly shape used by the current UI."""
    if canonical_df is None or canonical_df.empty:
        out = pd.DataFrame(columns=COMMON_SUPPORT_REPORT_HEADERS + ['Worker Status', 'Assigned Worker', 'Last Updated'])
        return out

    df = canonical_df.copy()
    out = pd.DataFrame(index=df.index.copy())

    def _ensure_series(col_name: str, default: Any = '') -> pd.Series:
        val = df.get(col_name, default)
        if isinstance(val, pd.Series):
            try:
                return val.astype(str).fillna('')
            except Exception:
                return val.fillna('').astype(str)
        return pd.Series([str(val) if val is not None else ''] * len(df), index=df.index)

    # Normalize and prepopulate commonly used fields for the UI/editor
    def _digits_only(s: Any) -> str:
        return ''.join(ch for ch in str(s) if ch.isdigit())

    report_source = ''
    try:
        report_source = str(df.get('report_source', '').astype(str).dropna().iloc[0]).strip().upper()
    except Exception:
        report_source = ''

    # Case number: prefer digits-only. For 56/SETS ensure 10-digit format when possible.
    raw_case = _ensure_series('case_number', '')
    case_nums = raw_case.map(_digits_only)
    if report_source == '56':
        # try to extract or pad to 10 digits when reasonable
        def _fmt_56(v: str) -> str:
            if len(v) == 10:
                return v
            if len(v) > 10:
                # take last 10 digits (common when prefixes exist)
                return v[-10:]
            return v
        case_nums = case_nums.map(_fmt_56)

    out['Case Number'] = case_nums.astype(str)

    # Caseload: normalize numeric form; present short 4-digit when possible (strip leading 18)
    raw_caseload = _ensure_series('caseload', '')
    caseload_digits = raw_caseload.map(_digits_only)
    def _short_caseload(v: str) -> str:
        if v.startswith('18') and len(v) == 6:
            return v[-4:]
        if len(v) == 4:
            return v
        return v
    out['Caseload'] = caseload_digits.map(_short_caseload).astype(str)

    # Case Type: normalize to uppercase and validate common codes
    raw_type = _ensure_series('case_type', '')
    out['Case Type'] = raw_type.str.strip().str.upper()

    # Case Mode: normalize to single-letter S/P when present
    raw_mode = _ensure_series('case_mode', '')
    def _fmt_mode(v: str) -> str:
        v = v.strip().upper()
        if not v:
            return ''
        if v and v[0] in ('S', 'P'):
            return v[0]
        return v
    out['Case Mode'] = raw_mode.map(_fmt_mode)

    # Keep legacy naming even when the source is 56/PS.
    out['Date Case Reviewed'] = df.get('action_taken_date', pd.NaT)
    out['Results of Review'] = _ensure_series('action_taken_status', '').astype(str)
    out['Case Closure Code'] = _ensure_series('case_closure_code', '').astype(str)

    if 'case_narrated' in df.columns:
        narrated = df['case_narrated']
        out['Case Narrated'] = narrated.map(lambda v: 'Yes' if v is True else ('No' if v is False else ''))
    else:
        out['Case Narrated'] = ''

    out['Comment'] = _ensure_series('comment', '').astype(str)

    # Add parity-friendly extra columns (safe to ignore by UI).
    out['Report Source'] = _ensure_series('report_source', '').astype(str)
    out['Service Due'] = df.get('service_due_date', pd.NaT)
    out['Date Action Taken'] = df.get('action_taken_date', pd.NaT)
    out['Action Taken/Status'] = _ensure_series('action_taken_status', '').astype(str)
    out['Activity Date'] = df.get('activity_date', pd.NaT)
    out['Flags'] = _ensure_series('flag_reasons', '').astype(str)
    out['Flag Severity'] = _ensure_series('flag_severity', '').astype(str)
    out['Ingestion ID'] = _ensure_series('ingestion_id', '').astype(str)
    out['Source File'] = _ensure_series('source_filename', '').astype(str)
    out['Sheet Name'] = _ensure_series('sheet_name', '').astype(str)
    out['Imported At'] = _ensure_series('imported_at', '').astype(str)

    # Workflow columns
    if 'Worker Status' not in out.columns:
        out['Worker Status'] = 'Not Started'
    if 'Assigned Worker' not in out.columns:
        out['Assigned Worker'] = ''
    if 'Last Updated' not in out.columns:
        out['Last Updated'] = ''

    return out


COMMON_SUPPORT_REPORT_HEADERS = [
    'Case Number',
    'Caseload',
    'Case Type',
    'Case Mode',
    'Date Case Reviewed',
    'Results of Review',
    'Case Closure Code',
    'Case Narrated',
    'Comment'
]

SUPPORT_REPORT_HEADER_ALIASES = {
    'casenumber': 'Case Number',
    'caseid': 'Case Number',
    'caseload': 'Caseload',
    'caseloadnumber': 'Caseload',
    'casetype': 'Case Type',
    'casemode': 'Case Mode',
    'datecasereviewed': 'Date Case Reviewed',
    'reviewdate': 'Date Case Reviewed',
    'resultsofreview': 'Results of Review',
    'reviewresult': 'Results of Review',
    'caseclosurecode': 'Case Closure Code',
    'closurecode': 'Case Closure Code',
    'casenarrated': 'Case Narrated',
    'narrated': 'Case Narrated',
    'comment': 'Comment',
    'comments': 'Comment'
}


def normalize_caseload_number(raw_value: Any) -> str:
    digits = ''.join(ch for ch in str(raw_value) if ch.isdigit())
    if not digits:
        return ''
    if len(digits) == 4 and digits.startswith('1'):
        return f"18{digits}"
    if len(digits) == 6 and digits.startswith('18'):
        return digits
    return digits


def extract_caseload_numbers_from_headers(df: Optional[pd.DataFrame]) -> List[str]:
    if df is None:
        return []
    pattern = re.compile(r'(18\d{4}|1\d{3})')
    found = []
    for column_name in df.columns:
        matches = pattern.findall(str(column_name))
        for match in matches:
            normalized = normalize_caseload_number(match)
            if normalized and normalized not in found:
                found.append(normalized)
    return found


def _normalize_header_key(header_name: str) -> str:
    return ''.join(ch for ch in str(header_name).lower() if ch.isalnum())


def count_recognized_support_headers(df: Optional[pd.DataFrame]) -> int:
    if df is None or df.empty:
        return 0
    recognized = set()
    for column in df.columns:
        normalized = _normalize_header_key(column)
        canonical = SUPPORT_REPORT_HEADER_ALIASES.get(normalized)
        if canonical:
            recognized.add(canonical)
    return len(recognized)


def normalize_support_report_dataframe(df: Optional[pd.DataFrame], fallback_caseload: str):
    if df is None:
        return pd.DataFrame(), 0, COMMON_SUPPORT_REPORT_HEADERS.copy()

    normalized_df = df.copy()
    rename_map = {}
    already_mapped = set()
    for column in normalized_df.columns:
        normalized = _normalize_header_key(column)
        canonical = SUPPORT_REPORT_HEADER_ALIASES.get(normalized)
        if canonical and canonical not in already_mapped:
            rename_map[column] = canonical
            already_mapped.add(canonical)

    if rename_map:
        normalized_df = normalized_df.rename(columns=rename_map)

    recognized_count = len(already_mapped)

    if 'Caseload' not in normalized_df.columns:
        normalized_df['Caseload'] = normalize_caseload_number(fallback_caseload)
    else:
        normalized_df['Caseload'] = normalized_df['Caseload'].apply(normalize_caseload_number)
        normalized_df['Caseload'] = normalized_df['Caseload'].replace('', normalize_caseload_number(fallback_caseload))

    if 'Case Number' in normalized_df.columns:
        normalized_df['Case Number'] = normalized_df['Case Number'].astype(str)

    for text_col in ['Results of Review', 'Case Closure Code', 'Case Narrated', 'Comment']:
        if text_col not in normalized_df.columns:
            normalized_df[text_col] = ''

    if 'Date Case Reviewed' not in normalized_df.columns:
        normalized_df['Date Case Reviewed'] = ''

    if 'Worker Status' not in normalized_df.columns:
        normalized_df['Worker Status'] = 'Not Started'
    if 'Assigned Worker' not in normalized_df.columns:
        normalized_df['Assigned Worker'] = ''
    if 'Last Updated' not in normalized_df.columns:
        normalized_df['Last Updated'] = ''

    missing_headers = [header for header in COMMON_SUPPORT_REPORT_HEADERS if header not in normalized_df.columns]

    ordered_cols = [col for col in COMMON_SUPPORT_REPORT_HEADERS if col in normalized_df.columns]
    workflow_cols = [col for col in ['Worker Status', 'Assigned Worker', 'Last Updated'] if col in normalized_df.columns]
    other_cols = [col for col in normalized_df.columns if col not in ordered_cols + workflow_cols]
    normalized_df = normalized_df[ordered_cols + other_cols + workflow_cols]

    return normalized_df, recognized_count, missing_headers


class SupportReportIngestionService:
    """Comprehensive support report ingestion and routing pipeline."""

    def __init__(self, processor: Optional['ReportProcessor'] = None):
        self.processor = processor or ReportProcessor()

    def read_uploaded_file(self, uploaded_file: Any) -> Dict[str, Any]:
        if uploaded_file is None:
            return {'success': False, 'error': 'No file uploaded.'}

        filename = getattr(uploaded_file, 'name', '') or 'uploaded_report'
        if not self.processor.validate_file_extension(filename):
            return {
                'success': False,
                'filename': filename,
                'error': f"Unsupported file format for {filename}. Upload .xlsx, .xls, or .csv."
            }

        try:
            file_data = uploaded_file.getvalue()
            result = self.processor.process_report(file_data=file_data, filename=filename)
            if not result.get('success'):
                return result

            # result['caseload_data'] is a list of {'caseload','sheet_name','df'}
            caseload_data = result.get('caseload_data', [])
            if caseload_data and isinstance(caseload_data[0], (tuple, list)):
                caseload_data = [{'caseload': c, 'sheet_name': '', 'df': df} for c, df in caseload_data]

            all_caseloads = [item.get('caseload') for item in caseload_data if isinstance(item, dict)]
            preview = {
                str(item.get('caseload')): (item.get('df').shape if isinstance(item.get('df'), pd.DataFrame) else (0, 0))
                for item in caseload_data
                if isinstance(item, dict)
            }
            return {
                'success': True,
                'filename': filename,
                'caseload_data': caseload_data,
                'all_caseloads': all_caseloads,
                'preview': preview,
                'metadata': result.get('metadata', {}),
            }
        except Exception as exc:
            logger.error(f"Ingestion read failure for {filename}: {exc}")
            return {
                'success': False,
                'filename': filename,
                'error': str(exc)
            }

    def analyze_dataframe(self, df: pd.DataFrame, fallback_caseload: str) -> Dict[str, Any]:
        normalized_df, recognized_headers, missing_headers = normalize_support_report_dataframe(df, fallback_caseload)
        detected_caseloads = extract_caseload_numbers_from_headers(df)

        canonical_result = map_dataframe_to_canonical(df, fallback_caseload=fallback_caseload)
        canonical_flagged = apply_excel_parity_flags(canonical_result.get('canonical_df'))
        return {
            'normalized_df': normalized_df,
            'recognized_headers': recognized_headers,
            'missing_headers': missing_headers,
            'detected_caseloads': detected_caseloads
            ,
            'report_source': canonical_result.get('report_source', 'UNKNOWN'),
            'qa_summary': canonical_result.get('qa_summary', {}),
            'unknown_columns': canonical_result.get('unknown_columns', []),
            'canonical_df': canonical_flagged,
        }

    @staticmethod
    def build_period_key(report_frequency: str, period_year: int, period_value: str) -> str:
        frequency_map = {
            'Monthly': 'M',
            'Quarterly': 'Q',
            'Bi-Annual': 'H'
        }
        token = frequency_map.get(report_frequency, 'U')
        return f"{int(period_year)}-{token}-{str(period_value).strip()}"

    @staticmethod
    def compute_dataframe_hash(df: pd.DataFrame) -> str:
        if df is None or df.empty:
            return ''
        try:
            hash_series = pd.util.hash_pandas_object(df.fillna(''), index=True)
            digest = hashlib.sha256(hash_series.values.tobytes()).hexdigest()
            return digest
        except Exception:
            fallback_payload = df.fillna('').astype(str).to_csv(index=False)
            return hashlib.sha256(fallback_payload.encode('utf-8')).hexdigest()

    def find_duplicate_candidates(
        self,
        registry_rows: List[Dict[str, Any]],
        report_type: str,
        owning_department: str,
        report_frequency: str,
        period_key: str,
        caseloads: List[str],
        dataframe_hash: str
    ) -> List[Dict[str, Any]]:
        duplicates = []
        target_caseloads = set(caseloads or [])
        normalized_department = str(owning_department or '').strip()
        for row in registry_rows:
            row_department = str(row.get('owning_department', '')).strip()
            same_department = True if not normalized_department else row_department == normalized_department
            same_schedule = (
                row.get('report_type') == report_type and
                same_department and
                row.get('report_frequency') == report_frequency and
                row.get('period_key') == period_key and
                row.get('caseload') in target_caseloads
            )
            same_hash = dataframe_hash and row.get('dataframe_hash') == dataframe_hash
            if same_schedule or same_hash:
                duplicates.append(row)
        return duplicates

    def build_ingestion_records(
        self,
        source_filename: str,
        uploader_role: str,
        normalized_df: pd.DataFrame,
        resolved_caseload: str,
        assigned_worker_choice: str,
        recognized_headers: int,
        missing_headers: List[str],
        existing_reports_by_caseload: Dict[str, List[Dict[str, Any]]],
        caseload_owner_resolver,
        report_type: str = 'General',
        owning_department: str = '',
        report_frequency: str = 'Monthly',
        period_label: str = '',
        period_key: str = '',
        ingestion_id: str = '',
        sheet_name: str = '',
        duplicate_detected: bool = False,
        duplicate_count: int = 0
    ) -> Dict[str, Any]:
        source_df = normalized_df.copy() if isinstance(normalized_df, pd.DataFrame) else pd.DataFrame()
        resolved_default = normalize_caseload_number(resolved_caseload)

        imported_at = datetime.now()
        canonical_result = map_dataframe_to_canonical(
            source_df,
            fallback_caseload=resolved_default,
            source_filename=source_filename,
            sheet_name=sheet_name,
            ingestion_id=ingestion_id,
            imported_at=imported_at,
        )
        canonical_all = apply_excel_parity_flags(canonical_result.get('canonical_df'))
        if canonical_all is None or canonical_all.empty:
            canonical_all = pd.DataFrame({'caseload': [resolved_default]})
            canonical_all = apply_excel_parity_flags(canonical_all)
            if 'caseload' in canonical_all.columns:
                canonical_all['caseload'] = canonical_all['caseload'].apply(normalize_caseload_number)
            canonical_all['report_source'] = canonical_result.get('report_source', 'UNKNOWN')
            canonical_all['ingestion_id'] = ingestion_id
            canonical_all['source_filename'] = source_filename
            canonical_all['imported_at'] = imported_at.isoformat()

        caseload_groups = []
        if 'caseload' in canonical_all.columns:
            for caseload_value in canonical_all['caseload'].dropna().astype(str).tolist():
                normalized_value = normalize_caseload_number(caseload_value)
                if normalized_value and normalized_value not in caseload_groups:
                    caseload_groups.append(normalized_value)
        if not caseload_groups:
            caseload_groups = [resolved_default]

        created_reports = []
        uploaded_rows = []
        audit_rows = []
        generated_counts: Dict[str, int] = {}

        for caseload_value in caseload_groups:
            existing_reports_by_caseload.setdefault(caseload_value, [])
            if 'caseload' in canonical_all.columns:
                caseload_canonical = canonical_all[canonical_all['caseload'].astype(str) == str(caseload_value)].copy()
            else:
                caseload_canonical = canonical_all.copy()

            caseload_df = canonical_to_workflow_dataframe(caseload_canonical)
            caseload_df, _, _ = normalize_support_report_dataframe(caseload_df, caseload_value)

            owner_unit, owner_person = caseload_owner_resolver(caseload_value)
            if assigned_worker_choice == '(Auto Assign by Caseload)':
                final_assigned_worker = owner_person
                route_method = 'Caseload Auto-Assignment'
                route_reason = 'Routed to caseload owner' if owner_person else 'No caseload owner found; queued as unassigned'
            elif assigned_worker_choice == '(Unassigned)':
                final_assigned_worker = None
                route_method = 'Manual/Unassigned Selection'
                route_reason = 'Uploader explicitly set report as unassigned'
            else:
                final_assigned_worker = assigned_worker_choice
                route_method = 'Manual/Unassigned Selection'
                route_reason = f'Uploader manually routed report to {assigned_worker_choice}'

            if not caseload_df.empty:
                caseload_df['Caseload'] = caseload_value
                caseload_df['Assigned Worker'] = final_assigned_worker or ''

            generated_counts.setdefault(caseload_value, 0)
            generated_counts[caseload_value] += 1
            report_id = f"RPT-{caseload_value}-{len(existing_reports_by_caseload[caseload_value]) + generated_counts[caseload_value]:03d}"
            report_entry = {
                'filename': source_filename,
                'timestamp': datetime.now(),
                'status': 'Ready for Processing',
                'report_id': report_id,
                'caseload': caseload_value,
                'ingestion_id': ingestion_id,
                'report_type': report_type,
                'owning_department': owning_department,
                'report_frequency': report_frequency,
                'period_label': period_label,
                'period_key': period_key,
                'duplicate_detected': duplicate_detected,
                'duplicate_count': duplicate_count,
                'data': caseload_df,
                'canonical_data': caseload_canonical,
                'qa_summary': canonical_result.get('qa_summary', {}),
                'uploaded_by': uploader_role,
                'assigned_worker': final_assigned_worker,
                'recognized_headers': recognized_headers,
                'missing_headers': missing_headers,
                'route_method': route_method,
                'route_reason': route_reason,
                'caseload_owner_unit': owner_unit,
                'caseload_owner': owner_person
            }

            uploaded_rows.append({
                'filename': source_filename,
                'timestamp': datetime.now(),
                'status': 'Completed',
                'caseload': caseload_value,
                'ingestion_id': ingestion_id,
                'report_type': report_type,
                'owning_department': owning_department,
                'report_frequency': report_frequency,
                'period_label': period_label,
                'period_key': period_key,
                'duplicate_detected': duplicate_detected,
                'assigned_worker': final_assigned_worker,
                'recognized_headers': recognized_headers,
                'uploaded_by': uploader_role
            })

            audit_rows.append({
                'timestamp': datetime.now().isoformat(),
                'uploaded_by': uploader_role,
                'filename': source_filename,
                'report_id': report_id,
                'caseload': caseload_value,
                'assigned_worker': final_assigned_worker or 'Unassigned',
                'route_method': route_method,
                'route_reason': route_reason,
                'ingestion_id': ingestion_id,
                'report_type': report_type,
                'owning_department': owning_department,
                'report_frequency': report_frequency,
                'period_key': period_key,
                'duplicate_detected': duplicate_detected,
                'duplicate_count': duplicate_count
            })

            created_reports.append(report_entry)

        return {
            'success': True,
            'created_reports': created_reports,
            'uploaded_rows': uploaded_rows,
            'audit_rows': audit_rows,
            'caseload_groups': caseload_groups
        }


class ReportProcessor:
    """Main class for processing establishment reports"""
    
    def __init__(self):
        # Excel support disabled: only CSV uploads allowed
        self.supported_extensions = ['.csv']
        self.required_columns = ['Case_ID', 'Worker', 'Status']
        
    def validate_file_extension(self, filename: str) -> bool:
        """
        Validate if the uploaded file has a supported extension
        
        Args:
            filename: Name of the file to validate
            
        Returns:
            True if extension is supported, False otherwise
        """
        file_extension = Path(filename).suffix.lower()
        return file_extension in self.supported_extensions
    

    def read_excel_file(self, file_data: bytes, filename: str) -> Dict[str, pd.DataFrame]:
        """
        Read Excel file from bytes data, supporting multiple sheets.
        Returns a dict of {sheet_name: DataFrame} for Excel, or {'Data': DataFrame} for CSV.
        """
        try:
            file_extension = Path(filename).suffix.lower()
            # Only CSV upload/processing is supported now
            if file_extension == '.csv':
                df = pd.read_csv(io.BytesIO(file_data))
                logger.info(f"Successfully read CSV file: {filename}, shape: {df.shape}")
                return {'Data': df}
            raise ValueError(f"Unsupported file format: {file_extension}. Excel support has been disabled; upload CSV files only.")
        except Exception as e:
            logger.error(f"Error reading file {filename}: {str(e)}")
            raise
    
    def validate_dataframe(self, df: pd.DataFrame, 
                          required_columns: Optional[List[str]] = None) -> Tuple[bool, List[str]]:
        """
        Validate DataFrame structure and content
        
        Args:
            df: DataFrame to validate
            required_columns: List of required column names (optional)
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if DataFrame is empty
        if df.empty:
            errors.append("DataFrame is empty")
            return False, errors
        
        # Check required columns
        columns_to_check = required_columns or self.required_columns
        missing_columns = [col for col in columns_to_check if col not in df.columns]
        
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Check for excessive null values
        for col in df.columns:
            null_percentage = (df[col].isnull().sum() / len(df)) * 100
            if null_percentage > 50:
                errors.append(f"Column '{col}' has {null_percentage:.1f}% null values")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and normalize DataFrame data
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        # Strip whitespace from string columns
        for col in df_clean.select_dtypes(include=['object']).columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
        
        # Replace common null representations
        df_clean.replace(['', 'nan', 'None', 'N/A', 'null'], np.nan, inplace=True)
        
        # Remove completely empty rows
        df_clean.dropna(how='all', inplace=True)
        
        logger.info(f"DataFrame cleaned. Original shape: {df.shape}, New shape: {df_clean.shape}")
        return df_clean
    

    def process_report(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """
        Complete report processing pipeline for multi-sheet Excel or CSV.
        Returns a dict with a list of (caseload, DataFrame) pairs and metadata.
        """
        try:
            # Step 1: Read all sheets
            sheets = self.read_excel_file(file_data, filename)
            caseload_data = []
            caseload_data_legacy = []
            all_metadata = {}
            for sheet_name, df in sheets.items():
                if df is None or df.empty:
                    continue
                df_clean = self.clean_dataframe(df)
                caseload_col = None
                for col in df_clean.columns:
                    if _normalize_header_key(col) in ('caseload', 'caseloadnumber'):
                        caseload_col = col
                        break
                if caseload_col:
                    # Multiple caseloads in this sheet
                    for caseload_value in sorted(df_clean[caseload_col].dropna().unique()):
                        caseload_df = df_clean[df_clean[caseload_col] == caseload_value].copy()
                        caseload_str = normalize_caseload_number(caseload_value)
                        if not caseload_str:
                            continue
                        meta = self.generate_metadata(caseload_df, filename)
                        all_metadata[f"{sheet_name}|{caseload_str}"] = meta
                        caseload_data.append({'caseload': caseload_str, 'sheet_name': sheet_name, 'df': caseload_df})
                        caseload_data_legacy.append((caseload_str, caseload_df))
                else:
                    # No caseload column: use sheet name as caseload
                    caseload_str = normalize_caseload_number(sheet_name)
                    if not caseload_str:
                        caseload_str = sheet_name.strip()
                    meta = self.generate_metadata(df_clean, filename)
                    all_metadata[f"{sheet_name}|{caseload_str}"] = meta
                    caseload_data.append({'caseload': caseload_str, 'sheet_name': sheet_name, 'df': df_clean})
                    caseload_data_legacy.append((caseload_str, df_clean))
            if not caseload_data:
                return {
                    'success': False,
                    'error': 'No valid data found in any sheet.',
                    'filename': filename,
                    'processed_at': datetime.now().isoformat()
                }
            return {
                'success': True,
                'caseload_data': caseload_data,
                'caseload_data_legacy': caseload_data_legacy,
                'metadata': all_metadata,
                'filename': filename,
                'processed_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error processing report {filename}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename,
                'processed_at': datetime.now().isoformat()
            }
    
    def generate_metadata(self, df: pd.DataFrame, filename: str) -> Dict[str, Any]:
        """
        Generate metadata about the DataFrame
        
        Args:
            df: DataFrame to analyze
            filename: Original filename
            
        Returns:
            Dictionary containing metadata
        """
        metadata = {
            'filename': filename,
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'null_counts': df.isnull().sum().to_dict(),
            'generated_at': datetime.now().isoformat()
        }
        return metadata


class ReportExporter:
    """Handle exporting reports to various formats"""
    
    @staticmethod
    def to_excel(df: pd.DataFrame, filename: str = 'export.xlsx') -> bytes:
        """
        Export DataFrame to Excel format
        
        Args:
            df: DataFrame to export
            filename: Output filename
            
        Returns:
            Bytes content of Excel file
        """
        logger.error("Excel export requested but Excel support is disabled.")
        raise NotImplementedError("Excel export is disabled. Please export to CSV or JSON instead.")
    
    @staticmethod
    def to_csv(df: pd.DataFrame) -> str:
        """
        Export DataFrame to CSV format
        
        Args:
            df: DataFrame to export
            
        Returns:
            CSV string content
        """
        csv_string = df.to_csv(index=False)
        logger.info("DataFrame exported to CSV")
        return csv_string
    
    @staticmethod
    def to_json(df: pd.DataFrame) -> str:
        """
        Export DataFrame to JSON format
        
        Args:
            df: DataFrame to export
            
        Returns:
            JSON string content
        """
        json_string = df.to_json(orient='records', date_format='iso', indent=2)
        logger.info("DataFrame exported to JSON")
        return json_string


class DataValidator:
    """Validate data against business rules"""
    
    @staticmethod
    def validate_case_id(case_id: str) -> bool:
        """Validate Case ID format"""
        if not case_id or pd.isna(case_id):
            return False
        return len(str(case_id).strip()) > 0
    
    @staticmethod
    def validate_status(status: str, valid_statuses: List[str] = None) -> bool:
        """Validate status values"""
        if valid_statuses is None:
            valid_statuses = ['Pending', 'In Progress', 'Completed', 'Approved', 'Rejected']
        
        if not status or pd.isna(status):
            return False
        
        return str(status).strip() in valid_statuses
    
    @staticmethod
    def validate_date(date_value: Any) -> bool:
        """Validate date values"""
        if pd.isna(date_value):
            return False
        
        try:
            pd.to_datetime(date_value)
            return True
        except:
            return False
    
    @staticmethod
    def validate_numeric(value: Any, min_value: float = None, max_value: float = None) -> bool:
        """Validate numeric values with optional range"""
        try:
            num_value = float(value)
            if min_value is not None and num_value < min_value:
                return False
            if max_value is not None and num_value > max_value:
                return False
            return True
        except:
            return False


class AuditLogger:
    """Handle audit logging for system actions"""
    
    def __init__(self, log_file: Path = None):
        if log_file is None:
            log_file = Path("audit_log.jsonl")
        self.log_file = log_file
    
    def log_action(self, action: str, user: str, details: Dict[str, Any] = None):
        """
        Log an audit action
        
        Args:
            action: Action performed
            user: User who performed the action
            details: Additional details about the action
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'user': user,
            'details': details or {}
        }
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            logger.info(f"Audit log entry created: {action} by {user}")
        except Exception as e:
            logger.error(f"Error writing audit log: {str(e)}")
    
    def read_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Read recent audit logs
        
        Args:
            limit: Maximum number of logs to return
            
        Returns:
            List of log entries
        """
        logs = []
        
        if not self.log_file.exists():
            return logs
        
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    logs.append(json.loads(line.strip()))
            
            # Return most recent logs first
            return logs[-limit:][::-1]
        except Exception as e:
            logger.error(f"Error reading audit logs: {str(e)}")
            return []


def format_number(value: float, decimals: int = 2) -> str:
    """Format number with thousands separator"""
    return f"{value:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"


def calculate_completion_rate(completed: int, total: int) -> float:
    """Calculate completion rate percentage"""
    if total == 0:
        return 0.0
    return (completed / total) * 100


def generate_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate summary statistics for a DataFrame
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary of summary statistics
    """
    return {
        'total_records': len(df),
        'columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
        'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
        'text_columns': df.select_dtypes(include=['object']).columns.tolist(),
        'null_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    }


# Initialize default instances
report_processor = ReportProcessor()
report_exporter = ReportExporter()
data_validator = DataValidator()
audit_logger = AuditLogger()


if __name__ == "__main__":
    # Test the utilities
    print("OCSS Report Utils - Test Mode")
    print("=" * 50)
    
    # Create sample data
    sample_data = pd.DataFrame({
        'Case_ID': ['C001', 'C002', 'C003'],
        'Worker': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'Status': ['Completed', 'In Progress', 'Pending'],
        'Date_Filed': ['2025-01-15', '2025-01-16', '2025-01-17']
    })
    
    print("Sample DataFrame:")
    print(sample_data)
    print("\nValidation:", report_processor.validate_dataframe(sample_data))
    print("\nSummary Stats:", generate_summary_stats(sample_data))
