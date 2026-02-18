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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReportProcessor:
    """Main class for processing establishment reports"""
    
    def __init__(self):
        self.supported_extensions = ['.xlsx', '.xls', '.csv']
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
    
    def read_excel_file(self, file_data: bytes, filename: str) -> pd.DataFrame:
        """
        Read Excel file from bytes data
        
        Args:
            file_data: File content as bytes
            filename: Original filename
            
        Returns:
            DataFrame containing the Excel data
        """
        try:
            file_extension = Path(filename).suffix.lower()
            
            if file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(io.BytesIO(file_data))
            elif file_extension == '.csv':
                df = pd.read_csv(io.BytesIO(file_data))
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            logger.info(f"Successfully read file: {filename}, shape: {df.shape}")
            return df
        
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
        Complete report processing pipeline
        
        Args:
            file_data: File content as bytes
            filename: Original filename
            
        Returns:
            Dictionary containing processed data and metadata
        """
        try:
            # Step 1: Read file
            df = self.read_excel_file(file_data, filename)
            
            # Step 2: Validate
            is_valid, errors = self.validate_dataframe(df)
            
            # Step 3: Clean
            df_clean = self.clean_dataframe(df)
            
            # Step 4: Generate metadata
            metadata = self.generate_metadata(df_clean, filename)
            
            result = {
                'success': True,
                'data': df_clean,
                'is_valid': is_valid,
                'validation_errors': errors,
                'metadata': metadata,
                'filename': filename,
                'processed_at': datetime.now().isoformat()
            }
            
            logger.info(f"Report processed successfully: {filename}")
            return result
        
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
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        output.seek(0)
        logger.info(f"DataFrame exported to Excel: {filename}")
        return output.getvalue()
    
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
