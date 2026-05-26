# B2B Leads Data Cleaning Pipeline

Automated data cleaning pipeline for German construction industry B2B leads — **step 5/7** in the end-to-end leads pipeline.

## What it does

- Normalizes company data to a fixed 12-column template
- Formats emails (lowercase, de-obfuscation) and phone numbers (international format)
- Fills missing fields with `n.a`, highlights missing Website/E-Mail in yellow
- Classifies companies by `type` and `service` via website scraping
- Finds senior contact persons (CEO, Managing Director, etc.) per company
- Backs up the original file before any changes

## Output template

```
Company Name | Street | City | Zip | Website | Phone | E-Mail | Contact Person | Position | Contact Email | Contact Phone | Note / Category
```

## Setup

**Requirements:** Python 3.8+

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py leads.xlsx
python src/main.py leads.xlsx --output leads_cleaned.xlsx
```

## Claude Code slash commands

| Command | Description | Status |
|---------|-------------|--------|
| `/clean` | Normalize + backup + highlight `.xlsx` file | ✅ |
| `/classify` | Enrich missing fields + classify type/service from website | ✅ |
| `/contact` | Find senior contact persons (1 row per person) | ✅ |
| `/report` | Statistics report | ⚠️ Needs update |
| `/researcher` | Research and summarize information on demand | ✅ |

## Architecture

| Module | Role |
|--------|------|
| `src/tags.py` | Source of truth: column order, types, services, highlight rules |
| `src/normalizer.py` | Pure transformation: email/phone formatting, change log |
| `src/excel_handler.py` | Excel I/O: backup, load, save with yellow highlights |
| `src/main.py` | Orchestrator CLI |

## Data flow

```
input.xlsx
  └─ backup copy (<stem>_backup_YYYYMMDD_HHMMSS.xlsx)
  └─ load() → DataFrame
  └─ normalize() → (cleaned_df, changes, yellow_cells)
  └─ save() → output_cleaned.xlsx
       ├─ Sheet "Data"         — 12 columns, n.a filled, yellow highlights
       └─ Sheet "Deleted Data" — log of erased real content (safety net)
```
