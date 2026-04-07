from pathlib import Path
import sys


# This file does the preprocessing step:
# 1. Read the raw loan CSV file.
# 2. Create default_flag and default_stage.
# 3. Clean missing values and outliers.
# 4. Save the cleaned dataset and a short dataset description.
try:
    import pandas as pd
except ModuleNotFoundError:
    print("pandas is not installed. Run: pip install -r backend/requirements.txt")
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "report"

RAW_DATA_FILE = DATA_DIR / "lending_club_loan_two.csv"
PROCESSED_DATA_FILE = DATA_DIR / "processed_lending_club_loan.csv"
DATASET_DESCRIPTION_FILE = REPORT_DIR / "DATASET_DESCRIPTION.md"


def print_heading(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def get_default_flag(loan_status):
    # 1 means risky/default-like, 0 means not default.
    loan_status = str(loan_status).lower()

    risky_words = ["charged off", "default", "late"]
    for word in risky_words:
        if word in loan_status:
            return 1

    return 0


def get_default_stage(loan_status):
    # Convert loan status text into simple stages for the report and model.
    loan_status = str(loan_status).lower()

    if "fully paid" in loan_status:
        return "non_default"

    if "current" in loan_status:
        return "active"

    if "late" in loan_status or "grace" in loan_status:
        return "delinquent"

    if "charged off" in loan_status or "default" in loan_status:
        return "default"

    return "other"


def load_data():
    if not RAW_DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATA_FILE}")

    data = pd.read_csv(RAW_DATA_FILE, low_memory=False)
    return data


def create_new_columns(data):
    data = data.copy()

    if "loan_status" in data.columns:
        data["default_flag"] = data["loan_status"].apply(get_default_flag)
        data["default_stage"] = data["loan_status"].apply(get_default_stage)

    if "issue_d" in data.columns:
        data["issue_d"] = pd.to_datetime(data["issue_d"], format="%b-%Y", errors="coerce")
        data["issue_year"] = data["issue_d"].dt.year
        data["issue_month"] = data["issue_d"].dt.month

    if "earliest_cr_line" in data.columns:
        data["earliest_cr_line"] = pd.to_datetime(
            data["earliest_cr_line"], format="%b-%Y", errors="coerce"
        )

    if "issue_d" in data.columns and "earliest_cr_line" in data.columns:
        credit_days = data["issue_d"] - data["earliest_cr_line"]
        data["credit_history_years"] = (credit_days.dt.days / 365.25).round(2)

    return data


def clean_data(data):
    data = data.copy()

    # Remove text columns that are too noisy for this simple project.
    columns_to_remove = ["emp_title", "title"]
    for column in columns_to_remove:
        if column in data.columns:
            data = data.drop(columns=[column])

    # Fill missing numeric values.
    if "mort_acc" in data.columns:
        data["mort_acc"] = data["mort_acc"].fillna(0)

    if "pub_rec_bankruptcies" in data.columns:
        data["pub_rec_bankruptcies"] = data["pub_rec_bankruptcies"].fillna(0)

    numeric_columns = ["revol_util", "annual_inc", "dti"]
    for column in numeric_columns:
        if column in data.columns:
            median_value = data[column].median()
            data[column] = data[column].fillna(median_value)

    # Convert term from text like "36 months" to number like 36.
    if "term" in data.columns:
        term_numbers = data["term"].astype(str).str.extract(r"(\d+)")
        data["term"] = term_numbers[0].astype(float)

    # Fill missing categorical values.
    text_columns = ["grade", "sub_grade", "verification_status", "purpose"]
    for column in text_columns:
        if column in data.columns:
            data[column] = data[column].fillna("unknown")

    # Clip extreme values using the IQR method.
    outlier_columns = ["loan_amnt", "annual_inc", "dti"]
    for column in outlier_columns:
        if column in data.columns:
            q1 = data[column].quantile(0.25)
            q3 = data[column].quantile(0.75)
            iqr = q3 - q1
            lower_limit = q1 - 1.5 * iqr
            upper_limit = q3 + 1.5 * iqr
            data[column] = data[column].clip(lower=lower_limit, upper=upper_limit)

    return data


def select_needed_columns(data):
    needed_columns = [
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

    final_columns = []
    for column in needed_columns:
        if column in data.columns:
            final_columns.append(column)

    return data[final_columns]


def save_dataset_description(data):
    lines = [
        "# Dataset Description",
        "",
        f"- Source file: `{RAW_DATA_FILE.name}`",
        f"- Rows: {len(data)}",
        f"- Columns: {len(data.columns)}",
        "",
        "## Data Types",
        "- Structured data: CSV file",
        "- Quantitative data: loan amount, annual income, DTI",
        "- Nominal data: loan status, grade, purpose",
        "- Time-related data: issue date, earliest credit line",
        "",
        "## Final Columns",
    ]

    for column in data.columns:
        lines.append(f"- `{column}`: {data[column].dtype}")

    DATASET_DESCRIPTION_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    print_heading("STEP 1: LOAD DATA")
    data = load_data()
    print("Raw data shape:", data.shape)

    print_heading("STEP 2: CREATE NEW COLUMNS")
    data = create_new_columns(data)
    print("Created: default_flag, default_stage, issue_year, issue_month")

    print_heading("STEP 3: CLEAN DATA")
    data = clean_data(data)
    data = select_needed_columns(data)
    print("Processed data shape:", data.shape)

    print_heading("STEP 4: SAVE FILES")
    data.to_csv(PROCESSED_DATA_FILE, index=False)
    save_dataset_description(data)
    print(f"Processed dataset saved to: {PROCESSED_DATA_FILE}")
    print(f"Dataset description saved to: {DATASET_DESCRIPTION_FILE}")


if __name__ == "__main__":
    main()
