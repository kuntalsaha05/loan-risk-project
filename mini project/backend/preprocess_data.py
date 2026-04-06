"""
preprocess_data.py - Clean and prepare raw loan data for modeling.

This module reads the raw CSV dataset, creates new risk features, fills missing values,
cleans columns, and writes a model-ready CSV file.
"""

from pathlib import Path
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
RAW_DATA_PATH = DATA_DIR / "lending_club_loan_two.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed_lending_club_loan.csv"
DATASET_DESCRIPTION_PATH = BASE_DIR / "report" / "DATASET_DESCRIPTION.md"


def load_dataset() -> pd.DataFrame:
    """Read the raw loan dataset from disk."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATA_PATH}")
    return pd.read_csv(RAW_DATA_PATH, low_memory=False)


def create_default_flag(df: pd.DataFrame) -> pd.Series:
    """Convert loan status into a binary default flag."""
    status_text = df["loan_status"].astype(str).str.lower()
    default_keywords = [
        "charged off",
        "default",
        "late",
        "does not meet the credit policy. status:charged off",
    ]
    return status_text.apply(lambda value: int(any(keyword in value for keyword in default_keywords)))


def create_default_stage(df: pd.DataFrame) -> pd.Series:
    """Convert loan status into broad default stage categories."""
    status_text = df["loan_status"].astype(str).str.lower()

    def map_stage(value: str) -> str:
        if "fully paid" in value:
            return "non_default"
        if "current" in value:
            return "active"
        if any(keyword in value for keyword in ["late", "grace"]):
            return "delinquent"
        if any(keyword in value for keyword in ["charged off", "default"]):
            return "default"
        return "other"

    return status_text.apply(map_stage)


def parse_issue_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Extract year and month from the issue date field."""
    df = df.copy()
    df["issue_d"] = pd.to_datetime(df["issue_d"], format="%b-%Y", errors="coerce")
    df["issue_year"] = df["issue_d"].dt.year
    df["issue_month"] = df["issue_d"].dt.month
    return df


def compute_credit_history_years(df: pd.DataFrame) -> pd.DataFrame:
    """Compute how many years the borrower has had credit history."""
    df = df.copy()
    df["earliest_cr_line"] = pd.to_datetime(
        df["earliest_cr_line"], format="%b-%Y", errors="coerce"
    )
    if "issue_d" in df.columns:
        history_years = (df["issue_d"] - df["earliest_cr_line"]).dt.days / 365.25
        df["credit_history_years"] = history_years.round(2)
    return df


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create additional features used for modeling and analysis."""
    df = df.copy()

    if "loan_status" in df.columns:
        df["default_flag"] = create_default_flag(df)
        df["default_stage"] = create_default_stage(df)

    if "issue_d" in df.columns:
        df = parse_issue_dates(df)

    if "earliest_cr_line" in df.columns:
        df = compute_credit_history_years(df)

    return df


def fill_numeric_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing numeric values with medians or defaults."""
    df = df.copy()
    fill_values = {
        "mort_acc": 0,
        "pub_rec_bankruptcies": 0,
        "revol_util": df["revol_util"].median() if "revol_util" in df.columns else None,
        "annual_inc": df["annual_inc"].median() if "annual_inc" in df.columns else None,
        "dti": df["dti"].median() if "dti" in df.columns else None,
    }

    for column, fill_value in fill_values.items():
        if column in df.columns and fill_value is not None:
            df[column] = df[column].fillna(fill_value)

    return df


def process_term_column(df: pd.DataFrame) -> pd.DataFrame:
    """Convert loan term from text like '36 months' into numeric value."""
    df = df.copy()
    if "term" in df.columns:
        extracted_term = df["term"].astype(str).str.extract(r"(\d+)")
        df["term"] = extracted_term[0].astype(float)
    return df


def fill_categorical_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace missing categorical fields with a default value."""
    df = df.copy()
    categorical_columns = [
        "grade",
        "sub_grade",
        "home_ownership",
        "verification_status",
        "purpose",
    ]
    for column in categorical_columns:
        if column in df.columns:
            df[column] = df[column].fillna("unknown")
    return df


def clip_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Limit extreme values in selected numeric features.

    Clipping reduces the effect of very large or small values on later modeling.
    """
    df = df.copy()
    for column in ["loan_amnt", "annual_inc", "dti"]:
        if column in df.columns:
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            df[column] = df[column].clip(lower=lower, upper=upper)
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Remove unneeded columns and keep only the selected final fields."""
    df = df.copy()

    if "emp_title" in df.columns or "title" in df.columns:
        df = df.drop(columns=[column for column in ["emp_title", "title"] if column in df.columns])

    df = fill_numeric_values(df)
    df = process_term_column(df)
    df = fill_categorical_values(df)
    df = clip_outliers(df)

    selected_columns = [
        "loan_amnt",
        "term",
        "int_rate",
        "installment",
        "grade",
        "sub_grade",
        "annual_inc",
        "verification_status",
        "issue_d",
        "purpose",
        "dti",
        "earliest_cr_line",
        "open_acc",
        "pub_rec",
        "revol_bal",
        "revol_util",
        "mort_acc",
        "pub_rec_bankruptcies",
        "issue_year",
        "issue_month",
        "credit_history_years",
        "loan_status",
        "default_flag",
        "default_stage",
    ]
    final_columns = [column for column in selected_columns if column in df.columns]
    return df[final_columns]


def generate_dataset_description(df: pd.DataFrame) -> None:
    """Write a short markdown summary of the processed dataset."""
    lines = [
        "# Dataset Description",
        "",
        "## Source File",
        f"- `{RAW_DATA_PATH.name}`",
        "",
        "## Shape",
        f"- Rows: {len(df)}",
        f"- Columns: {len(df.columns)}",
        "",
        "## Data Types",
        "- Structured data: CSV dataset",
        "- Quantitative data examples: loan amount, annual income, DTI",
        "- Nominal data examples: loan status, grade, purpose",
        "- Time-series related fields: issue date, earliest credit line",
        "",
        "## Current Project Features",
    ]

    for column in df.columns:
        lines.append(f"- `{column}`: {df[column].dtype}")

    DATASET_DESCRIPTION_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Main entry point for preprocessing and description generation."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = load_dataset()
    df = add_engineered_features(df)
    df = clean_dataset(df)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    generate_dataset_description(df)

    print(f"Processed dataset saved to: {PROCESSED_DATA_PATH}")
    print(f"Dataset description saved to: {DATASET_DESCRIPTION_PATH}")


if __name__ == "__main__":
    main()
