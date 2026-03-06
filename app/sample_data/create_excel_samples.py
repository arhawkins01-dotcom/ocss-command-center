"""
Sample Data Generator for OCSS Command Center
Creates demo establishment reports for testing (LOCATE, 56RA, P-S reports)
"""

import pandas as pd
from pathlib import Path
import os

def generate_sample_reports():
    """Generate Excel files from CSV sample data"""
    
    sample_dir = Path(__file__).parent
    
    # List of CSV files to convert to Excel
    csv_files = [
        "sample_locate_report.csv",
        "sample_56ra_report.csv", 
        "sample_ps_report.csv"
    ]
    
    for csv_file in csv_files:
        csv_path = sample_dir / csv_file
        
        if not csv_path.exists():
            print(f"❌ File not found: {csv_file}")
            continue
        
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            
            # Create Excel file
            excel_file = csv_file.replace(".csv", ".xlsx")
            excel_path = sample_dir / excel_file
            
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Report Data")
                
                # Auto-adjust column widths
                worksheet = writer.sheets["Report Data"]
                for idx, col in enumerate(df.columns, 1):
                    max_length = max(
                        df[col].astype(str).map(len).max(),
                        len(str(col))
                    ) + 2
                    worksheet.column_dimensions[chr(64 + idx)].width = min(max_length, 50)
            
            print(f"✅ Created: {excel_file} ({len(df)} rows)")
            
        except Exception as e:
            print(f"❌ Error processing {csv_file}: {e}")
    
    print("\n📊 Sample Data Generation Complete!")
    print(f"📁 Location: {sample_dir}/")
    print("\nAvailable Demo Files:")
    print("  • sample_locate_report.csv/xlsx")
    print("  • sample_56ra_report.csv/xlsx")
    print("  • sample_ps_report.csv/xlsx")


if __name__ == "__main__":
    generate_sample_reports()
