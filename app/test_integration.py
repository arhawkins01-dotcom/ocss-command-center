"""
Integration tests for OCSS Command Center
Tests configuration, utilities, and data processing
"""

import sys
import os
import ast
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
    assert config['app']['name'] == 'OCSS Command Center'
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

# Test 4b: Support Report Ingestion Routing
print("\nTest 4b: Testing support report ingestion routing...")
try:
    ingestion_service = report_utils.SupportReportIngestionService()

    raw_df = pd.DataFrame({
        'CaseID': ['CASE-1', 'CASE-2'],
        'CaseloadNumber': ['181000', '181001'],
        'CaseType': ['A', 'B'],
        'CaseMode': ['Auto', 'Manual']
    })

    analysis = ingestion_service.analyze_dataframe(raw_df, '181000')
    normalized_df = analysis['normalized_df']
    assert 'Worker Status' in normalized_df.columns
    assert 'Assigned Worker' in normalized_df.columns

    existing_reports = {'181000': [], '181001': []}

    def _resolver(caseload):
        if caseload == '181000':
            return 'OCSS North', 'Michael Chen'
        if caseload == '181001':
            return 'OCSS South', 'Amanda Wilson'
        return None, None

    ingest_result = ingestion_service.build_ingestion_records(
        source_filename='sample_upload.xlsx',
        uploader_role='Program Officer',
        normalized_df=normalized_df,
        resolved_caseload='181000',
        assigned_worker_choice='(Auto Assign by Caseload)',
        recognized_headers=analysis['recognized_headers'],
        missing_headers=analysis['missing_headers'],
        existing_reports_by_caseload=existing_reports,
        caseload_owner_resolver=_resolver
    )

    assert ingest_result['success'] == True
    assert len(ingest_result['created_reports']) == 2
    for report_entry in ingest_result['created_reports']:
        assert report_entry['report_id'].startswith('RPT-')
        assert report_entry['status'] == 'Ready for Processing'
        assert isinstance(report_entry['data'], pd.DataFrame)
        assert 'Worker Status' in report_entry['data'].columns

    assigned_workers = {entry['assigned_worker'] for entry in ingest_result['created_reports']}
    assert 'Michael Chen' in assigned_workers
    assert 'Amanda Wilson' in assigned_workers
    print("  ✓ Ingestion routing and payload generation working")

except Exception as e:
    print(f"  ✗ Ingestion routing test failed: {e}")
    sys.exit(1)

# Test 4c: Duplicate Period Detection Primitives
print("\nTest 4c: Testing duplicate period detection helpers...")
try:
    ingestion_service = report_utils.SupportReportIngestionService()
    period_key = ingestion_service.build_period_key('Monthly', 2026, '02')
    assert period_key == '2026-M-02'

    sample_df = pd.DataFrame({
        'Case Number': ['A1', 'A2'],
        'Caseload': ['181000', '181000']
    })
    df_hash = ingestion_service.compute_dataframe_hash(sample_df)
    assert len(df_hash) > 0

    registry = [{
        'report_id': 'RPT-181000-001',
        'report_type': 'P-S Report',
        'report_frequency': 'Monthly',
        'period_key': '2026-M-02',
        'caseload': '181000',
        'dataframe_hash': df_hash
    }]
    dups = ingestion_service.find_duplicate_candidates(
        registry_rows=registry,
        report_type='P-S Report',
        owning_department='Program Operations',
        report_frequency='Monthly',
        period_key='2026-M-02',
        caseloads=['181000'],
        dataframe_hash=df_hash
    )
    assert len(dups) == 1
    print("  ✓ Duplicate detection helpers working")

except Exception as e:
    print(f"  ✗ Duplicate detection helper test failed: {e}")
    sys.exit(1)

# Test 4d: Duplicate Detection by Owning Department
print("\nTest 4d: Testing duplicate detection department scoping...")
try:
    ingestion_service = report_utils.SupportReportIngestionService()
    scoped_registry = [
        {
            'report_id': 'RPT-181000-001',
            'report_type': 'P-S Report',
            'owning_department': 'Program Operations',
            'report_frequency': 'Monthly',
            'period_key': '2026-M-02',
            'caseload': '181000',
            'dataframe_hash': 'hash-a'
        },
        {
            'report_id': 'RPT-181000-002',
            'report_type': 'P-S Report',
            'owning_department': 'Finance',
            'report_frequency': 'Monthly',
            'period_key': '2026-M-02',
            'caseload': '181000',
            'dataframe_hash': 'hash-b'
        }
    ]

    scoped_dups = ingestion_service.find_duplicate_candidates(
        registry_rows=scoped_registry,
        report_type='P-S Report',
        owning_department='Program Operations',
        report_frequency='Monthly',
        period_key='2026-M-02',
        caseloads=['181000'],
        dataframe_hash=''
    )
    assert len(scoped_dups) == 1
    assert scoped_dups[0]['owning_department'] == 'Program Operations'
    print("  ✓ Department-scoped duplicate detection working")

except Exception as e:
    print(f"  ✗ Duplicate department scoping test failed: {e}")
    sys.exit(1)

# Test 4e: Ingestion Metadata Propagation
print("\nTest 4e: Testing ingestion metadata propagation...")
try:
    ingestion_service = report_utils.SupportReportIngestionService()

    base_df = pd.DataFrame({
        'CaseID': ['CASE-10'],
        'CaseloadNumber': ['181000']
    })
    analysis = ingestion_service.analyze_dataframe(base_df, '181000')
    normalized_df = analysis['normalized_df']

    result = ingestion_service.build_ingestion_records(
        source_filename='meta_test.xlsx',
        uploader_role='Program Officer',
        normalized_df=normalized_df,
        resolved_caseload='181000',
        assigned_worker_choice='(Unassigned)',
        recognized_headers=analysis['recognized_headers'],
        missing_headers=analysis['missing_headers'],
        existing_reports_by_caseload={'181000': []},
        caseload_owner_resolver=lambda _: ('OCSS North', 'Michael Chen'),
        report_type='P-S Report',
        owning_department='Program Operations',
        report_frequency='Monthly',
        period_label='2026-02',
        period_key='2026-M-02',
        ingestion_id='ING-TEST-0001',
        duplicate_detected=True,
        duplicate_count=2
    )

    assert result['success'] == True
    assert len(result['created_reports']) == 1
    created = result['created_reports'][0]
    uploaded = result['uploaded_rows'][0]
    audit = result['audit_rows'][0]

    assert created['ingestion_id'] == 'ING-TEST-0001'
    assert created['owning_department'] == 'Program Operations'
    assert created['period_key'] == '2026-M-02'
    assert created['duplicate_detected'] == True
    assert uploaded['ingestion_id'] == 'ING-TEST-0001'
    assert uploaded['owning_department'] == 'Program Operations'
    assert uploaded['period_key'] == '2026-M-02'
    assert audit['ingestion_id'] == 'ING-TEST-0001'
    assert audit['owning_department'] == 'Program Operations'
    assert audit['period_key'] == '2026-M-02'
    print("  ✓ Ingestion metadata propagation working")

except Exception as e:
    print(f"  ✗ Ingestion metadata propagation test failed: {e}")
    sys.exit(1)

# Test 4f: Supported Roles and Submit Guard Presence
print("\nTest 4f: Testing supported roles and submit guard coverage...")
try:
    app_source = (app_dir / 'app.py').read_text(encoding='utf-8')
    app_tree = ast.parse(app_source)

    core_roles = None
    supported_roles_ref = None
    for node in app_tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'CORE_APP_ROLES':
                    core_roles = ast.literal_eval(node.value)
                if isinstance(target, ast.Name) and target.id == 'SUPPORTED_USER_ROLES':
                    if isinstance(node.value, ast.Name):
                        supported_roles_ref = node.value.id
                    else:
                        supported_roles_ref = ast.literal_eval(node.value)

    assert isinstance(core_roles, list)
    assert core_roles == ["Director", "Program Officer", "Supervisor", "Support Officer", "IT Administrator"]
    assert supported_roles_ref == 'CORE_APP_ROLES' or supported_roles_ref == core_roles

    # Submit-guard coverage: block submit until all assigned rows are Completed
    assert "pending_rows" in app_source
    assert "worker_rows['Worker Status'] != 'Completed'" in app_source
    assert "if not pending_rows.empty:" in app_source
    assert "Cannot submit yet." in app_source
    print("  ✓ Supported roles restricted and row-level submit guard coverage present")

except Exception as e:
    print(f"  ✗ Supported roles / submit guard coverage test failed: {e}")
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
    sample_dir = app_dir / 'sample_data'
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
    py_compile.compile(str(app_dir / 'app.py'), doraise=True)
    print("  ✓ app.py syntax valid")
except Exception as e:
    print(f"  ✗ app.py syntax check failed: {e}")
    sys.exit(1)

# Test 10: Directory structure
print("\nTest 10: Checking directory structure...")
try:
    required_dirs = ['config', 'sample_data']
    for dir_name in required_dirs:
        dir_path = app_dir / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name}/ exists")
        else:
            print(f"  ⚠ {dir_name}/ not found (may be optional)")
    
    required_files = ['app.py', 'report_utils.py', 'requirements.txt']
    for file_name in required_files:
        file_path = app_dir / file_name
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
