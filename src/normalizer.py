import re

import pandas as pd
import phonenumbers
from typing import Any

from tags import COLUMNS, NA_VALUE, HIGHLIGHT_COLUMNS


def _normalize_email(val: str) -> str:
    val = val.lower()
    val = re.sub(r'\[\s*@\s*\]|\(\s*@\s*\)', '@', val)
    val = re.sub(r'\[\s*\.\s*\]|\(\s*\.\s*\)', '.', val)
    val = re.sub(r'\s+', '', val)
    return val


def _normalize_phone(val: str) -> str:
    try:
        parsed = phonenumbers.parse(val, "DE")
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except phonenumbers.NumberParseException:
        pass
    return val


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    return str(value).strip() == ""


def normalize(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict], list[tuple[int, str]]]:
    """
    Normalize a DataFrame to match the standard template.

    Returns:
        df_out:      Normalized DataFrame with COLUMNS in correct order.
        changes:     List of dicts describing every cell modification.
        yellow_cells: List of (row_index, column_name) to highlight yellow.
    """
    changes: list[dict] = []
    yellow_cells: list[tuple[int, str]] = []

    # Add any missing columns filled with empty string
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""

    # Reorder columns (keep only template columns)
    df = df[COLUMNS].copy()

    for idx in df.index:
        company_name = str(df.at[idx, "Company Name"]).strip() or NA_VALUE

        for col in COLUMNS:
            raw = df.at[idx, col]
            old_val = str(raw).strip() if not _is_empty(raw) else ""

            # Determine new value
            if _is_empty(raw):
                new_val = NA_VALUE
            else:
                new_val = str(raw).strip()
                if col in ("E-Mail", "Contact Email"):
                    new_val = _normalize_email(new_val)
                elif col in ("Phone", "Contact Phone"):
                    new_val = _normalize_phone(new_val)

            # Record only if real content was erased (safety net for data loss)
            if old_val not in ("", NA_VALUE) and new_val == NA_VALUE:
                changes.append({
                    "row": idx + 2,  # 1-indexed + header row
                    "company_name": company_name,
                    "field": col,
                    "old_value": old_val if old_val else "(empty)",
                    "new_value": new_val,
                    "highlighted": "no",
                })

            df.at[idx, col] = new_val

        # Flag cells for yellow highlight
        for col in HIGHLIGHT_COLUMNS:
            if df.at[idx, col] == NA_VALUE:
                yellow_cells.append((idx, col))
                # Update the highlighted flag in the last change entry for this cell
                for change in reversed(changes):
                    if change["row"] == idx + 2 and change["field"] == col:
                        change["highlighted"] = "yes"
                        break

    return df, changes, yellow_cells
