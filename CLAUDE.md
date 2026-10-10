# CSV Cleanup — learning project

## Purpose

Clean a messy material list CSV and write a clean version.
Practice project only. All data is synthetic, never real company data.

## About me

I'm learning Python and pandas. Comment every function and explain new
concepts in 1–2 sentences when you use them. Prefer simple, readable code
over clever code.

## Setup and commands

- Python 3 with a virtual environment in `.venv`
- Activate it on my Mac: `source .venv/bin/activate`
- Run the script: `python clean_materials.py`
- Test the overdue logic with a fixed date: `python clean_materials.py --today 2026-12-01`

## The data

The input is `data/raw/materials_raw.csv`. It has these six columns, in this order:

- `material number`: the ID of the part, like `MAT-100324`
- `description`: what the part is, like "Hex bolt M8"
- `quantity`: how many I need, a whole number
- `unit`: what the quantity is counted in (kg, pcs, m, l)
- `due date`: the day I need the part
- `plant`: the site that needs it. It's a code like `1000`, `1010`, `2000` or `DE01`,
  so I always treat it as text, never as a number

## Cleaning rules I decided on

- Trim spaces in every column. Inside a description, several spaces become one.
- Material numbers are uppercase.
- Units are lowercase: `kg`, `pcs`, `m`, `l`.
- Quantities are whole numbers. A comma is a thousands separator, so `1,250` becomes `1250`.
  The raw file has commas only and no dots in quantities. A dot value like `1.250` is not
  supported: I don't know if it means 1250 or 1.25, so the script stops with an error
  instead of guessing. If real data ever has dots, I decide the rule first.
- Rows with a missing or non-numeric quantity (empty or `N/A`) are **kept**, with the
  quantity left blank. I don't drop them and I don't guess a value. The script counts them.
- Dates in the clean file are `YYYY-MM-DD`. The raw file has three formats:
  `YYYY-MM-DD` (already fine, most rows), `DD.MM.YYYY` (dots) and US style `MM/DD/YYYY`
  (slashes). A date that fits none of these three becomes blank.
- A duplicate is a row that is identical in every column **after** cleaning, so rows that
  only differ by spaces or upper/lower case count too. I keep the first one.
- Order of counting: missing quantities and missing dates are counted **before** duplicates
  are removed, so they describe the raw rows. Overdue rows are counted **after**, so they
  match "rows out". For the sample file, the missing counts are the same either way
  because no duplicate row has a gap.

## The output file

`data/clean/materials_clean.csv` has these columns, in this order. The names change from the
raw file: spaces become underscores and everything is lowercase.

`material_number, description, quantity, unit, due_date, plant, is_overdue`

- `quantity` is a whole number or blank.
- `due_date` is `YYYY-MM-DD` or blank.
- `plant` stays text.
- `is_overdue` is added as the last column: `True`, `False` or blank.

## Overdue logic

- `is_overdue` is `True` if the due date is before today, and `False` otherwise.
- A part that is due today is **not** overdue.
- If the due date is missing, `is_overdue` stays blank. Unknown is not the same as "not overdue".
- The result depends on the day I run the script. That's why `--today` exists for testing.

## How to check it worked

After running, the summary must show rows in, rows out, duplicates removed, missing
quantities, missing dates and overdue rows. For the sample file I expect
50 in, 46 out, 4 duplicates removed, 6 missing quantities and 1 missing date.

## Folder rules

- `data/raw/` = original files. Never modify these.
- `data/clean/` = script output.

## How we work

- Plan first, then code. Wait for my OK before writing code.
- Small steps: one change at a time, then let me run and check it.
- Ask before installing any new package.
- Synthetic sample data may be committed; real company data never. Never commit the
  `.venv` folder (use .gitignore).
