"""
Data Cleaning Script — Leads Processing Pipeline
Usage:
    python src/main.py leads.xlsx
    python src/main.py leads.xlsx --output leads_cleaned.xlsx
"""

import argparse
import sys
from pathlib import Path

# Allow running from repo root or from src/
sys.path.insert(0, str(Path(__file__).parent))

from excel_handler import backup, load, save
from normalizer import normalize


def process_file(input_path: str, output_path: str | None = None) -> dict:
    """
    Run the full cleaning pipeline on input_path.
    Returns a summary dict.
    """
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path is None:
        output_path = str(input_file.parent / f"{input_file.stem}_cleaned{input_file.suffix}")

    # Step 1: Backup
    backup_path = backup(input_path)

    # Step 2: Load
    df = load(input_path)

    # Step 3: Normalize + track changes
    df_clean, changes, yellow_cells = normalize(df)

    # Step 4: Save output with highlights + change log
    save(df_clean, changes, yellow_cells, output_path)

    return {
        "input": input_path,
        "backup": backup_path,
        "output": output_path,
        "total_rows": len(df_clean),
        "yellow_highlights": len(yellow_cells),
        "deleted_cells": len(changes),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean and normalize leads .xlsx file")
    parser.add_argument("input", help="Path to input .xlsx file")
    parser.add_argument("--output", help="Path to output .xlsx file (optional)")
    args = parser.parse_args()

    try:
        result = process_file(args.input, args.output)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"\n[OK] Backup saved:  {result['backup']}")
    print(f"[OK] Output saved:  {result['output']}")
    print(f"\nSummary:")
    print(f"  Total rows:        {result['total_rows']}")
    print(f"  Yellow highlights: {result['yellow_highlights']:>4}  (missing Website / E-Mail)")
    print(f"  Deleted data:      {result['deleted_cells']:>4}  (cells with content that were erased)")


if __name__ == "__main__":
    main()
