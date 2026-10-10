# CSV Cleanup

A small learning project: clean a messy material list (CSV) with Python and pandas.
All data is synthetic. No real company data is used.

## What it does

`clean_materials.py` reads `data/raw/materials_raw.csv`, fixes the problems below
and writes `data/clean/materials_clean.csv`.

| Problem in the raw file | What the script does |
|---|---|
| Extra spaces in any column | Trims them; collapses repeated spaces in descriptions |
| Lowercase material numbers (`mat-100184`) | Uppercases them |
| Mixed unit casing (`kg`, `KG`, `Kg`) | Lowercases all units |
| Missing or non-numeric quantities (`""`, `N/A`) | Leaves them blank and counts them (rows are kept) |
| Thousands separators (`1,250`) | Converts to `1250` |
| Mixed date formats | Parses `YYYY-MM-DD`, `DD.MM.YYYY` and `MM/DD/YYYY`, writes `YYYY-MM-DD` |
| Duplicate rows (including case/space-only duplicates) | Removes them, keeping the first |

It also adds an `is_overdue` column: `True` if the due date is before today,
`False` otherwise, and blank if the due date is missing.

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
```

## Usage

```
python clean_materials.py
```

To test the overdue logic against a fixed date instead of today:

```
python clean_materials.py --today 2026-12-01
```

Example output:

```
rows in:             50
rows out:            46
duplicates removed:  4
missing quantities:  6
missing dates:       1
overdue rows:        0 (as of 2026-10-10)
```

## Input format

The `data/` folder is not committed. To run the script, put a file at
`data/raw/materials_raw.csv` with these six columns in this order
(the header names are replaced by the script, but the order matters):

`material number, description, quantity, unit, due date, plant`

## Assumptions and limits

- Dates with slashes are read as US style (`MM/DD/YYYY`); dates with dots as `DD.MM.YYYY`.
  A date like `04/05/2026` is therefore April 5.
- A date that matches none of the three formats becomes blank and is counted as missing.
- Units are only lowercased, not checked against an allowed list.
- `is_overdue` depends on the day you run the script, so the output changes over time.

## Folders

- `data/raw/`: original input files. Never modified by the script.
- `data/clean/`: script output.
