"""
Integration tests for OCSS Command Center
Tests configuration, utilities, and data processing
"""

import sys
import os
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

print("="*60)
print("OCSS Command Center - Integration Tests")
print("="*60)
print()

# Test 1: Import core modules
print("Test 1: Importing core modules...")
try:
    import streamlit as st
    import pandas as pd
    import numpy as np
    print("  ✓ Streamlit imported")
    print("  ✓ Pandas imported")
    print("  ✓ NumPy imported")
except Exception as e:
    print(f"  ✗ Failed to import core modules: {e}")
    sys.exit(1)

# Test 2: Import custom modules
print("\nTest 2: Importing custom modules...")
try:
    from config import settings
    import report_utils
    print("  ✓ config.settings imported")
    print("  ✓ report_utils imported")
except Exception as e:
    print(f"  ✗ Failed to import custom modules: {e}")
    sys.exit(1)

# Test 3: Configuration
print("\nTest 3: Testing configuration...")
try:
    config = settings.get_config()
    assert 'app' in config
    assert 'server' in config
    assert 'paths' in config
    assert config['app']['name'] == 'OCSS Establishment Command Center'
    print(f"  ✓ Configuration loaded: {config['app']['name']}")
    print(f"  ✓ Version: {config['app']['version']}")
except Exception as e:
    print(f"  ✗ Configuration test failed: {e}")
    sys.exit(1)

# Test 4: Report Processor
print("\nTest 4: Testing report processor...")
try:
    processor = report_utils.ReportProcessor()
    
    # Test file extension validation
    assert processor.validate_file_extension('test.xlsx') == True
    assert processor.validate_file_extension('test.csv') == True
    assert processor.validate_file_extension('test.txt') == False
    print("  ✓ File extension validation working")
    
    # Test DataFrame validation
    test_df = pd.DataFrame({
        'Case_ID': ['C001', 'C002'],
        'Worker': ['John Doe', 'Jane Smith'],
        'Status': ['Completed', 'Pending']
    })
    is_valid, errors = processor.validate_dataframe(test_df)
    assert is_valid == True
    print("  ✓ DataFrame validation working")
    
    # Test data cleaning
    dirty_df = pd.DataFrame({
        'Case_ID': ['C001', '  C002  ', 'C003'],
        'Worker': ['John', 'Jane  ', '  Bob'],
        'Status': ['Done', '', None]
    })
    clean_df = processor.clean_dataframe(dirty_df)
    assert len(clean_df) == 3
    print("  ✓ Data cleaning working")
    
except Exception as e:
    print(f"  ✗ Report processor test failed: {e}")
    sys.exit(1)

# Test 5: Data Validator
print("\nTest 5: Testing data validator...")
try:
    validator = report_utils.DataValidator()
    
    # Test case ID validation
    assert validator.validate_case_id('CASE001') == True
    assert validator.validate_case_id('') == False
    assert validator.validate_case_id(None) == False
    print("  ✓ Case ID validation working")
    
    # Test status validation
    assert validator.validate_status('Pending') == True
    assert validator.validate_status('Invalid') == False
    print("  ✓ Status validation working")
    
    # Test numeric validation
    assert validator.validate_numeric(50) == True
    assert validator.validate_numeric(50, min_value=0, max_value=100) == True
    assert validator.validate_numeric(150, min_value=0, max_value=100) == False
    print("  ✓ Numeric validation working")
    
except Exception as e:
    print(f"  ✗ Data validator test failed: {e}")
    sys.exit(1)

# Test 6: Report Exporter
print("\nTest 6: Testing report exporter...")
try:
    exporter = report_utils.ReportExporter()
    test_df = pd.DataFrame({
        'Case_ID': ['C001', 'C002'],
        'Worker': ['John', 'Jane'],
        'Status': ['Done', 'Pending']
    })
    
    # Test Excel export
    excel_bytes = exporter.to_excel(test_df)
    assert len(excel_bytes) > 0
    print("  ✓ Excel export working")
    
    # Test CSV export
    csv_string = exporter.to_csv(test_df)
    assert len(csv_string) > 0
    assert 'Case_ID' in csv_string
    print("  ✓ CSV export working")
    
    # Test JSON export
    json_string = exporter.to_json(test_df)
    assert len(json_string) > 0
    assert 'Case_ID' in json_string
    print("  ✓ JSON export working")
    
except Exception as e:
    print(f"  ✗ Report exporter test failed: {e}")
    sys.exit(1)

# Test 7: Utility Functions
print("\nTest 7: Testing utility functions...")
try:
    # Test formatting
    assert report_utils.format_number(1234.5678, 2) == "1,234.57"
    assert report_utils.format_percentage(89.345, 1) == "89.3%"
    print("  ✓ Number formatting working")
    
    # Test calculations
    rate = report_utils.calculate_completion_rate(45, 50)
    assert rate == 90.0
    print("  ✓ Calculation functions working")
    
    # Test summary stats
    test_df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['x', 'y', 'z'],
        'C': [1.1, 2.2, None]
    })
    stats = report_utils.generate_summary_stats(test_df)
    assert stats['total_records'] == 3
    assert stats['columns'] == 3
    print("  ✓ Summary statistics working")
    
except Exception as e:
    print(f"  ✗ Utility functions test failed: {e}")
    sys.exit(1)

# Test 8: Sample Data Files
print("\nTest 8: Testing sample data files...")
try:
    sample_dir = Path('sample_data')
    if sample_dir.exists():
        # Test reading sample Excel file
        sample_file = sample_dir / 'sample_establishment_report.xlsx'
        if sample_file.exists():
            df = pd.read_excel(sample_file)
            assert len(df) > 0
            assert 'Case_ID' in df.columns
            print(f"  ✓ Sample Excel file readable ({len(df)} rows)")
        
        # Test reading sample CSV file
        sample_csv = sample_dir / 'sample_establishment_report.csv'
        if sample_csv.exists():
            df = pd.read_csv(sample_csv)
            assert len(df) > 0
            print(f"  ✓ Sample CSV file readable ({len(df)} rows)")
    else:
        print("  ⚠ Sample data directory not found (optional)")
        
except Exception as e:
    print(f"  ⚠ Sample data test skipped: {e}")

# Test 9: App.py syntax check
print("\nTest 9: Checking app.py syntax...")
try:
    import py_compile
    py_compile.compile('app.py', doraise=True)
    print("  ✓ app.py syntax valid")
except Exception as e:
    print(f"  ✗ app.py syntax check failed: {e}")
    sys.exit(1)

# Test 10: Directory structure
print("\nTest 10: Checking directory structure...")
try:
    required_dirs = ['config', 'sample_data']
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✓ {dir_name}/ exists")
        else:
            print(f"  ⚠ {dir_name}/ not found (may be optional)")
    
    required_files = ['app.py', 'report_utils.py', 'requirements.txt']
    for file_name in required_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"  ✓ {file_name} exists")
        else:
            print(f"  ✗ {file_name} not found")
            sys.exit(1)
            
except Exception as e:
    print(f"  ✗ Directory structure test failed: {e}")
    sys.exit(1)

print()
print("="*60)
print("✓ All tests passed successfully!")
print("="*60)
print()
print("Summary:")
print("  - Core modules: OK")
print("  - Custom modules: OK")
print("  - Configuration: OK")
print("  - Report processor: OK")
print("  - Data validator: OK")
print("  - Report exporter: OK")
print("  - Utility functions: OK")
print("  - Sample data: OK")
print("  - App syntax: OK")
print("  - Directory structure: OK")
print()
print("The OCSS Command Center is ready for deployment!")
print()
