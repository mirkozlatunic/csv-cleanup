from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

RAW = Path("data/raw/materials_raw.csv")
CLEAN = Path("data/clean/materials_clean.csv")

COLUMNS = ["material_number", "description", "quantity", "unit", "due_date", "plant"]
DATE_FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y"]  # ISO, German, US


def parse_dates(series: pd.Series) -> pd.Series:
    """Turn text dates in mixed formats into real dates.

    Each format in DATE_FORMATS is tried in turn; a date that matches none
    becomes NaT ("not a time", pandas' empty date). combine_first fills only
    the slots that are still empty, so an earlier match is never overwritten.
    """
    parsed = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")
    for fmt in DATE_FORMATS:
        parsed = parsed.combine_first(pd.to_datetime(series, format=fmt, errors="coerce"))
    return parsed


def clean(df: pd.DataFrame, today: pd.Timestamp) -> pd.DataFrame:
    """Return a cleaned copy of the raw material table.

    Fixes spaces, casing, units, quantities and dates, and adds an
    is_overdue column (True if due before `today`, blank if the date is missing).
    """
    df = df.copy()
    df.columns = COLUMNS
    df = df.apply(lambda col: col.str.strip())
    df["description"] = df["description"].str.replace(r"\s+", " ", regex=True)
    df["material_number"] = df["material_number"].str.upper()
    df["unit"] = df["unit"].str.lower()
    df["quantity"] = pd.to_numeric(
        df["quantity"].str.replace(",", "", regex=False), errors="coerce"
    ).astype("Int64")
    due = parse_dates(df["due_date"])
    df["due_date"] = due.dt.strftime("%Y-%m-%d")
    # Overdue = due before today; unknown (missing date) stays blank, not False
    df["is_overdue"] = (due < today).astype("boolean").mask(due.isna())
    return df


def main(today: pd.Timestamp | None = None) -> None:
    """Read the raw CSV, clean it, remove duplicates, write the result and print a summary."""
    if today is None:
        today = pd.Timestamp.today().normalize()

    raw = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    df = clean(raw, today)

    missing_qty = int(df["quantity"].isna().sum())
    missing_dates = int(df["due_date"].isna().sum())

    out = df.drop_duplicates()
    CLEAN.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(CLEAN, index=False)

    print(f"rows in:             {len(raw)}")
    print(f"rows out:            {len(out)}")
    print(f"duplicates removed:  {len(df) - len(out)}")
    print(f"missing quantities:  {missing_qty}")
    print(f"missing dates:       {missing_dates}")
    print(f"overdue rows:        {int(out['is_overdue'].sum())} (as of {today.date()})")


if __name__ == "__main__":
    # argparse reads options typed after the script name, e.g. --today 2026-12-01
    parser = argparse.ArgumentParser()
    parser.add_argument("--today", type=pd.Timestamp, help="override today's date (YYYY-MM-DD)")
    main(parser.parse_args().today)
