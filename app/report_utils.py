"""
OCSS Command Center - Report Utilities Module
Provides enhanced functionality for data persistence, export, and validation
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import io


def save_session_data(data: Dict, filename: str = "session_backup.json") -> bool:
    """
    Save session state data to a JSON file for persistence
    
    Args:
        data: Dictionary of session data to save
        filename: Name of the file to save to
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)
        
        # Convert datetime objects to strings for JSON serialization
        serializable_data = _make_serializable(data)
        
        with open(filepath, 'w') as f:
            json.dump(serializable_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving session data: {e}")
        return False


def load_session_data(filename: str = "session_backup.json") -> Optional[Dict]:
    """
    Load session state data from a JSON file
    
    Args:
        filename: Name of the file to load from
        
    Returns:
        Dictionary of loaded data, or None if file doesn't exist or error occurs
    """
    try:
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading session data: {e}")
        return None


def export_to_excel(df: pd.DataFrame, sheet_name: str = "Sheet1") -> bytes:
    """
    Export a DataFrame to Excel format (XLSX) as bytes
    
    Args:
        df: DataFrame to export
        sheet_name: Name for the Excel sheet
        
    Returns:
        Bytes of the Excel file
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output.getvalue()


def export_multiple_sheets_to_excel(data_dict: Dict[str, pd.DataFrame]) -> bytes:
    """
    Export multiple DataFrames to a single Excel file with multiple sheets
    
    Args:
        data_dict: Dictionary mapping sheet names to DataFrames
        
    Returns:
        Bytes of the Excel file
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in data_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output.getvalue()


def validate_report_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate report data and return validation results
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dictionary with validation results including:
        - is_valid: Overall validation status
        - errors: List of error messages
        - warnings: List of warning messages
        - stats: Basic statistics about the data
    """
    errors = []
    warnings = []
    
    # Check if DataFrame is empty
    if df.empty:
        errors.append("DataFrame is empty")
        
    # Check for null values
    null_counts = df.isnull().sum()
    if null_counts.any():
        for col, count in null_counts[null_counts > 0].items():
            warnings.append(f"Column '{col}' has {count} null values")
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        warnings.append(f"Found {duplicates} duplicate rows")
    
    # Basic stats
    stats = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'null_values': int(df.isnull().sum().sum()),
        'duplicate_rows': duplicates
    }
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'stats': stats
    }


def search_dataframe(df: pd.DataFrame, search_term: str, 
                     columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Search for a term across specified columns in a DataFrame
    
    Args:
        df: DataFrame to search
        search_term: Term to search for (case-insensitive)
        columns: List of column names to search in (None = all columns)
        
    Returns:
        Filtered DataFrame with matching rows
    """
    if df.empty or not search_term:
        return df
    
    search_term = search_term.lower()
    
    if columns is None:
        columns = df.columns.tolist()
    
    # Filter to only string columns that exist
    search_columns = [col for col in columns if col in df.columns 
                     and df[col].dtype == 'object']
    
    if not search_columns:
        return df
    
    # Create a mask for rows that match the search term
    mask = pd.Series([False] * len(df))
    for col in search_columns:
        mask |= df[col].astype(str).str.lower().str.contains(search_term, na=False)
    
    return df[mask]


def format_audit_log_entry(actor: str, action: str, details: Dict) -> Dict:
    """
    Format an audit log entry with timestamp and standard structure
    
    Args:
        actor: User performing the action
        action: Action being performed
        details: Additional details about the action
        
    Returns:
        Formatted audit log entry dictionary
    """
    return {
        'timestamp': datetime.now().isoformat(),
        'actor': actor,
        'action': action,
        'details': details
    }


def write_audit_log(entry: Dict, log_file: str = "audit_log.jsonl") -> bool:
    """
    Append an audit log entry to the audit log file
    
    Args:
        entry: Audit log entry dictionary
        log_file: Path to the audit log file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, log_file)
        
        with open(filepath, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        return True
    except Exception as e:
        print(f"Error writing audit log: {e}")
        return False


def read_audit_log(log_file: str = "audit_log.jsonl", limit: int = 100) -> List[Dict]:
    """
    Read audit log entries from the audit log file
    
    Args:
        log_file: Path to the audit log file
        limit: Maximum number of entries to return (most recent first)
        
    Returns:
        List of audit log entry dictionaries
    """
    try:
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        filepath = os.path.join(data_dir, log_file)
        
        if not os.path.exists(filepath):
            return []
        
        entries = []
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        
        # Return most recent first
        return entries[-limit:][::-1]
    except Exception as e:
        print(f"Error reading audit log: {e}")
        return []


def _make_serializable(obj: Any) -> Any:
    """
    Convert objects to JSON-serializable format
    
    Args:
        obj: Object to convert
        
    Returns:
        JSON-serializable version of the object
    """
    if isinstance(obj, dict):
        return {key: _make_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, (datetime, pd.Timestamp)):
        return obj.isoformat()
    elif isinstance(obj, (pd.DataFrame, pd.Series)):
        return obj.to_dict()
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    else:
        return str(obj)


def get_caseload_summary(reports_by_caseload: Dict[str, List]) -> pd.DataFrame:
    """
    Generate a summary DataFrame of caseload statistics
    
    Args:
        reports_by_caseload: Dictionary mapping caseload IDs to report lists
        
    Returns:
        DataFrame with caseload summary statistics
    """
    summary_data = []
    for caseload_id, reports in reports_by_caseload.items():
        summary_data.append({
            'Caseload ID': caseload_id,
            'Total Reports': len(reports),
            'Status Summary': f"{len(reports)} reports"
        })
    
    return pd.DataFrame(summary_data)


def validate_caseload_id(caseload_id: str) -> bool:
    """
    Validate that a caseload ID follows the expected format
    
    Args:
        caseload_id: Caseload ID to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Expecting format like '181000', '181001', etc.
    if not caseload_id:
        return False
    
    # Check if it's a 6-digit number starting with '181'
    if len(caseload_id) == 6 and caseload_id.startswith('181') and caseload_id.isdigit():
        return True
    
    return False
