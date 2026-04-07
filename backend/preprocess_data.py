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


def print_heading(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def load_dataset() -> pd.DataFrame:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATA_PATH}")
    return pd.read_csv(RAW_DATA_PATH, low_memory=False)


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "loan_status" in df.columns:
        status_text = df["loan_status"].astype(str).str.lower()
        default_keywords = [
            "charged off",
            "default",
            "late",
            "does not meet the credit policy. status:charged off",
        ]
        df["default_flag"] = status_text.apply(
            lambda value: int(any(keyword in value for keyword in default_keywords))
        )

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

        df["default_stage"] = status_text.apply(map_stage)

    if "issue_d" in df.columns:
        df["issue_d"] = pd.to_datetime(df["issue_d"], format="%b-%Y", errors="coerce")
        df["issue_year"] = df["issue_d"].dt.year
        df["issue_month"] = df["issue_d"].dt.month

    if "earliest_cr_line" in df.columns:
        df["earliest_cr_line"] = pd.to_datetime(
            df["earliest_cr_line"], format="%b-%Y", errors="coerce"
        )
        if "issue_d" in df.columns:
            credit_length = (df["issue_d"] - df["earliest_cr_line"]).dt.days / 365.25
            df["credit_history_years"] = credit_length.round(2)

    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    drop_columns = [column for column in ["emp_title", "title"] if column in df.columns]
    if drop_columns:
        df = df.drop(columns=drop_columns)

    numeric_fill_defaults = {
        "mort_acc": 0,
        "pub_rec_bankruptcies": 0,
        "revol_util": df["revol_util"].median() if "revol_util" in df.columns else None,
        "annual_inc": df["annual_inc"].median() if "annual_inc" in df.columns else None,
        "dti": df["dti"].median() if "dti" in df.columns else None,
    }

    for column, fill_value in numeric_fill_defaults.items():
        if column in df.columns and fill_value is not None:
            df[column] = df[column].fillna(fill_value)

    if "term" in df.columns:
        extracted_term = df["term"].astype(str).str.extract(r"(\d+)")
        df["term"] = extracted_term[0].astype(float)

    for column in ["grade", "sub_grade", "home_ownership", "verification_status", "purpose"]:
        if column in df.columns:
            df[column] = df[column].fillna("unknown")

    for column in ["loan_amnt", "annual_inc", "dti"]:
        if column in df.columns:
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            df[column] = df[column].clip(lower=lower, upper=upper)

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
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print_heading("STEP 1: LOAD LOAN DATASET")
    df = load_dataset()
    print("Raw dataset loaded successfully")
    print("Raw shape:", df.shape)
    print("Raw columns:")
    print(df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nMissing values before cleaning:")
    print(df.isnull().sum().sort_values(ascending=False).head(15))

    print_heading("STEP 2: FEATURE ENGINEERING")
    df = add_engineered_features(df)
    print("Created new features:")
    print("- default_flag")
    print("- default_stage")
    print("- issue_year")
    print("- issue_month")
    print("- credit_history_years")
    print("\nDefault stage distribution:")
    print(df["default_stage"].value_counts(dropna=False))

    print_heading("STEP 3: DATA CLEANING AND REDUCTION")
    df = clean_dataset(df)
    print("Selected useful columns and handled missing values")
    print("Processed shape:", df.shape)
    print("\nProcessed data types:")
    print(df.dtypes)
    print("\nFirst 5 processed rows:")
    print(df.head())

    print_heading("STEP 4: SAVE OUTPUT FILES")
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    generate_dataset_description(df)
    print(f"Processed dataset saved to: {PROCESSED_DATA_PATH}")
    print(f"Dataset description saved to: {DATASET_DESCRIPTION_PATH}")


if __name__ == "__main__":
    main()
