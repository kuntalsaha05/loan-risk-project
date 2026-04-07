from pathlib import Path
import sqlite3
import sys

try:
    import pandas as pd
except ModuleNotFoundError:
    print("pandas is not installed. Run: pip install -r backend/requirements.txt")
    sys.exit(1)


# 1. Set file paths.
base_dir = Path(__file__).resolve().parents[1]
data_dir = base_dir / "data"
report_dir = base_dir / "report"

processed_file = data_dir / "processed_lending_club_loan.csv"
database_file = data_dir / "loan_risk.db"
etl_report_file = report_dir / "ETL_PROCESS.md"


# 2. Extract: load the processed CSV file.
if not processed_file.exists():
    raise FileNotFoundError(f"Processed dataset not found: {processed_file}")

df = pd.read_csv(processed_file, low_memory=False)
print("Processed dataset loaded:")
print(df.shape)
print(df.head())


# 3. Transform: convert date columns to simple YYYY-MM-DD text.
if "issue_d" in df.columns:
    df["issue_d"] = pd.to_datetime(df["issue_d"], errors="coerce").dt.strftime("%Y-%m-%d")

if "earliest_cr_line" in df.columns:
    df["earliest_cr_line"] = pd.to_datetime(
        df["earliest_cr_line"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")

print("\nDate columns formatted for database storage.")


# 4. Load: save the data into a SQLite database table.
connection = sqlite3.connect(database_file)
df.to_sql("loan_records", connection, if_exists="replace", index=False)
connection.close()

print(f"\nDatabase created at: {database_file}")
print("Table name: loan_records")


# 5. Save a short ETL report.
etl_lines = [
    "# ETL Process",
    "",
    "## Extract",
    "- Loaded `processed_lending_club_loan.csv` from the data folder.",
    f"- Records extracted: {len(df)}",
    "",
    "## Transform",
    "- Converted date fields into YYYY-MM-DD format.",
    "- Kept the cleaned columns from preprocessing.",
    "",
    "## Load",
    "- Loaded the data into SQLite database `loan_risk.db`.",
    "- Table name: `loan_records`.",
]

etl_report_file.write_text("\n".join(etl_lines), encoding="utf-8")
print(f"ETL report saved to: {etl_report_file}")
