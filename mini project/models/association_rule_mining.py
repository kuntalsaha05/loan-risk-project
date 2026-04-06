"""
association_rule_mining.py - Discover frequent loan patterns that predict default.

This module converts numeric fields into categories, applies Apriori mining, and
filters rules that explain default or non-default outcomes.
"""

from pathlib import Path
import sys


try:
    import pandas as pd
    from mlxtend.frequent_patterns import apriori, association_rules
except ModuleNotFoundError:
    print(
        "Missing dependencies for association rule mining.\n"
        "Install project dependencies first, for example:\n"
        "pip install -r backend/requirements.txt"
    )
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "report"
RAW_PROCESSED_PATH = DATA_DIR / "processed_lending_club_loan.csv"
RULES_OUTPUT_PATH = DATA_DIR / "association_rules.csv"
REPORT_OUTPUT_PATH = REPORT_DIR / "ASSOCIATION_RULES.md"


def load_data() -> pd.DataFrame:
    """Load the cleaned dataset used for association rule mining."""
    if not RAW_PROCESSED_PATH.exists():
        raise FileNotFoundError(f"Processed dataset not found: {RAW_PROCESSED_PATH}")
    return pd.read_csv(RAW_PROCESSED_PATH, low_memory=False)


def bucket_numeric_feature(series: pd.Series, label: str) -> pd.Series:
    """Convert a numeric column into low/medium/high buckets."""
    low = series.quantile(0.33)
    high = series.quantile(0.67)

    def assign_bucket(value: float) -> str:
        if pd.isna(value):
            return f"{label}=unknown"
        if value <= low:
            return f"{label}=low"
        if value <= high:
            return f"{label}=medium"
        return f"{label}=high"

    return series.apply(assign_bucket)


def build_transaction_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Create a transaction-style dataset for Apriori mining."""
    transactions = pd.DataFrame(index=df.index)
    transactions["income_bucket"] = bucket_numeric_feature(df["annual_inc"], "income")
    transactions["loan_bucket"] = bucket_numeric_feature(df["loan_amnt"], "loan")
    transactions["dti_bucket"] = bucket_numeric_feature(df["dti"], "dti")
    transactions["interest_bucket"] = bucket_numeric_feature(df["int_rate"], "interest")
    transactions["credit_history_bucket"] = bucket_numeric_feature(
        df["credit_history_years"], "credit_history"
    )
    transactions["term_bucket"] = df["term"].apply(
        lambda value: "term=short" if value <= 36 else "term=long"
    )
    transactions["grade_bucket"] = df["grade"].astype(str).apply(lambda value: f"grade={value}")
    transactions["purpose_bucket"] = df["purpose"].astype(str).apply(
        lambda value: f"purpose={value}"
    )
    transactions["default_bucket"] = df["default_flag"].apply(
        lambda value: "default=yes" if value == 1 else "default=no"
    )
    return transactions


def encode_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    """One-hot encode transaction categories for frequent itemset mining."""
    encoded = pd.get_dummies(transactions)
    return encoded.astype(bool)


def mine_rules(encoded_transactions: pd.DataFrame) -> pd.DataFrame:
    """Mine association rules and keep only rules related to default outcomes."""
    frequent_itemsets = apriori(encoded_transactions, min_support=0.05, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)
    if rules.empty:
        return rules

    rules = rules.copy()
    rules["antecedents"] = rules["antecedents"].apply(lambda items: ", ".join(sorted(items)))
    rules["consequents"] = rules["consequents"].apply(lambda items: ", ".join(sorted(items)))

    filtered = rules[
        rules["consequents"].str.contains("default=yes|default=no", regex=True)
    ].sort_values(by=["lift", "confidence", "support"], ascending=False)

    return filtered[["antecedents", "consequents", "support", "confidence", "lift"]].head(20)


def write_report(rules: pd.DataFrame) -> None:
    """Write a markdown report summarizing the discovered association rules."""
    lines = [
        "# Association Rule Mining",
        "",
        "## Method",
        "- Used Apriori-based frequent itemset mining",
        "- Converted continuous fields into categorical buckets",
        "- Generated rules using support, confidence, and lift",
        "",
    ]

    if rules.empty:
        lines.extend([
            "## Result",
            "- No rules met the current support and confidence thresholds.",
        ])
    else:
        lines.extend([
            "## Top Rules",
            "",
            "| Antecedent | Consequent | Support | Confidence | Lift |",
            "| --- | --- | --- | --- | --- |",
        ])
        for _, row in rules.iterrows():
            lines.append(
                f"| {row['antecedents']} | {row['consequents']} | "
                f"{row['support']:.4f} | {row['confidence']:.4f} | {row['lift']:.4f} |"
            )

        lines.extend([
            "",
            "## Interpretation",
            "- Higher lift indicates a stronger relationship than random chance.",
            "- Rules ending in `default=yes` help identify risky borrower profiles.",
            "- Rules ending in `default=no` help identify safer borrower profiles.",
        ])

    REPORT_OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run the association rule mining workflow and save results."""
    df = load_data()
    transactions = build_transaction_frame(df)
    encoded_transactions = encode_transactions(transactions)
    rules = mine_rules(encoded_transactions)
    rules.to_csv(RULES_OUTPUT_PATH, index=False)
    write_report(rules)

    print(f"Association rules saved to: {RULES_OUTPUT_PATH}")
    print(f"Association rule report saved to: {REPORT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
