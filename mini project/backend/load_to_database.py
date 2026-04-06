"""
load_to_database.py - Extract, transform, and load processed loan data into SQLite.

This module moves the cleaned CSV data into a local SQLite database table.
"""

from pathlib import Path
import sqlite3
import sys


try:
    import pandas as pd
except ModuleNotFoundError:
    print(
        "Missing dependency: pandas.\n"
        "Install project dependencies first, for example:\n"
        "pip install -r backend/requirements.txt"
    )
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_PATH = DATA_DIR / "processed_lending_club_loan.csv"
DB_PATH = DATA_DIR / "loan_risk.db"
ETL_REPORT_PATH = BASE_DIR / "report" / "ETL_PROCESS.md"


def extract_data() -> pd.DataFrame:
    """Load the cleaned dataset from disk."""
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(f"Processed dataset not found: {PROCESSED_DATA_PATH}")
    return pd.read_csv(PROCESSED_DATA_PATH, low_memory=False)


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare data for database storage by normalizing date fields."""
    df = df.copy()

    if "issue_d" in df.columns:
        df["issue_d"] = pd.to_datetime(df["issue_d"], errors="coerce").dt.strftime("%Y-%m-%d")

    if "earliest_cr_line" in df.columns:
        df["earliest_cr_line"] = pd.to_datetime(df["earliest_cr_line"], errors="coerce").dt.strftime("%Y-%m-%d")

    return df


def load_data(df: pd.DataFrame) -> None:
    """Write the transformed dataset into the SQLite database."""
    with sqlite3.connect(DB_PATH) as connection:
        df.to_sql("loan_records", connection, if_exists="replace", index=False)


def write_etl_report(row_count: int, column_count: int) -> None:
    """Write a short markdown report describing the ETL process."""
    lines = [
        "# ETL Process",
        "",
        "## Extract",
        "- Source file: `data/processed_lending_club_loan.csv`",
        f"- Records extracted: {row_count}",
        "",
        "## Transform",
        "- Parsed and standardized date fields for database storage",
        "- Preserved engineered fields such as `default_flag` and `default_stage`",
        "- Kept cleaned and selected features from preprocessing",
        "",
        "## Load",
        "- Target database: `data/loan_risk.db`",
        "- Target table: `loan_records`",
        f"- Columns loaded: {column_count}",
        "",
        "## ETL Summary",
        "- Extract: processed CSV loaded from the data folder",
        "- Transform: final formatting and date normalization for storage",
        "- Load: records inserted into SQLite for analytics and later dashboard use",
    ]
    ETL_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run the ETL sequence and save the report."""
    df = extract_data()
    transformed_df = transform_data(df)
    load_data(transformed_df)
    write_etl_report(len(transformed_df), len(transformed_df.columns))

    print(f"Database created at: {DB_PATH}")
    print("Table loaded: loan_records")
    print(f"ETL report saved to: {ETL_REPORT_PATH}")


if __name__ == "__main__":
    main()
