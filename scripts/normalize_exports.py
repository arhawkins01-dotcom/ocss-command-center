"""
Normalize CSV exports by coercing all columns to strings and trimming whitespace.

Usage:
    python scripts/normalize_exports.py exports/

This reads CSV files in the given directory and rewrites them with all columns
cast to string, replacing NaN with empty string. Helpful for preparing exports
for viewers or for preventing mixed-type serialization warnings.
"""
import sys
import os
import pandas as pd


def normalize_file(path: str) -> None:
    df = pd.read_csv(path)
    for col in df.columns:
        try:
            df[col] = df[col].where(pd.notna(df[col]), "")
            df[col] = df[col].astype(str).str.strip()
        except Exception:
            df[col] = df[col].astype(str)
    df.to_csv(path, index=False)


def main(directory: str) -> None:
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        sys.exit(1)
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    if not files:
        print("No CSV files found in", directory)
        return
    for f in files:
        p = os.path.join(directory, f)
        try:
            normalize_file(p)
            print("Normalized:", p)
        except Exception as e:
            print("Failed:", p, e)


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'exports'
    main(target)
