"""
Create sample data files for testing the OCSS Command Center
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def create_sample_establishment_report():
    """Create a sample establishment report"""
    
    # Generate sample data
    num_cases = 25
    workers = ['Sarah Johnson', 'Michael Chen', 'Jessica Brown', 'David Martinez', 'Amanda Wilson']
    statuses = ['Pending', 'In Progress', 'Completed', 'Under Review']
    
    data = {
        'Case_ID': [f'CASE-2026-{str(i).zfill(4)}' for i in range(1, num_cases + 1)],
        'Worker': [random.choice(workers) for _ in range(num_cases)],
        'Status': [random.choice(statuses) for _ in range(num_cases)],
        'Date_Filed': [(datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d') for _ in range(num_cases)],
        'Establishment': [random.choice(['Downtown Establishment', 'Midtown Enforcement', 'Uptown Collections']) for _ in range(num_cases)],
        'Case_Type': [random.choice(['Establishment', 'Modification', 'Review', 'Enforcement']) for _ in range(num_cases)],
        'Priority': [random.choice(['High', 'Medium', 'Low']) for _ in range(num_cases)],
        'Completion_Percentage': [random.randint(0, 100) for _ in range(num_cases)]
    }
    
    df = pd.DataFrame(data)
    return df

def create_sample_monthly_summary():
    """Create a sample monthly summary report"""
    
    months = pd.date_range(start='2025-09-01', periods=6, freq='M').strftime('%b %Y').tolist()
    
    data = {
        'Month': months,
        'Total_Cases': [45, 48, 52, 50, 58, 62],
        'Completed': [40, 42, 48, 45, 52, 55],
        'In_Progress': [3, 4, 3, 4, 5, 6],
        'Pending': [2, 2, 1, 1, 1, 1],
        'Completion_Rate': [88.9, 87.5, 92.3, 90.0, 89.7, 88.7],
        'Avg_Processing_Days': [14, 15, 12, 13, 14, 15]
    }
    
    df = pd.DataFrame(data)
    return df

def create_sample_cqi_alignment():
    """Create a sample CQI alignment report"""
    
    data = {
        'Metric': [
            'Report Submission Timeliness',
            'Data Quality Score',
            'Compliance Rate',
            'Documentation Completeness',
            'Process Adherence'
        ],
        'Target': [95.0, 98.0, 100.0, 95.0, 90.0],
        'Current': [94.2, 96.7, 98.5, 93.8, 91.2],
        'Previous_Month': [92.5, 95.2, 97.8, 92.0, 89.5],
        'Trend': ['↑', '↑', '↑', '↑', '↑'],
        'Status': ['On Track', 'On Track', 'On Track', 'Needs Improvement', 'On Track']
    }
    
    df = pd.DataFrame(data)
    return df

def save_all_samples():
    """Save all sample files"""
    
    # Create establishment report
    df_establishment = create_sample_establishment_report()
    df_establishment.to_excel('sample_data/sample_establishment_report.xlsx', index=False)
    df_establishment.to_csv('sample_data/sample_establishment_report.csv', index=False)
    print("✓ Created sample_establishment_report.xlsx and .csv")
    
    # Create monthly summary
    df_monthly = create_sample_monthly_summary()
    df_monthly.to_excel('sample_data/sample_monthly_summary.xlsx', index=False)
    df_monthly.to_csv('sample_data/sample_monthly_summary.csv', index=False)
    print("✓ Created sample_monthly_summary.xlsx and .csv")
    
    # Create CQI alignment
    df_cqi = create_sample_cqi_alignment()
    df_cqi.to_excel('sample_data/sample_cqi_alignment.xlsx', index=False)
    df_cqi.to_csv('sample_data/sample_cqi_alignment.csv', index=False)
    print("✓ Created sample_cqi_alignment.xlsx and .csv")
    
    print("\nSample data files created successfully!")
    print("Files are located in: sample_data/")

if __name__ == "__main__":
    save_all_samples()
