from pathlib import Path
import sys

try:
    import pandas as pd
    from mlxtend.frequent_patterns import apriori, association_rules
except ModuleNotFoundError:
    print("Required association rule libraries are missing. Run: pip install -r backend/requirements.txt")
    sys.exit(1)


# 1. Set file paths.
base_dir = Path(__file__).resolve().parents[1]
data_dir = base_dir / "data"
report_dir = base_dir / "report"

processed_file = data_dir / "processed_lending_club_loan.csv"
rules_file = data_dir / "association_rules.csv"
report_file = report_dir / "ASSOCIATION_RULES.md"


# 2. Load the processed dataset.
df = pd.read_csv(processed_file, low_memory=False)
print("Dataset loaded:")
print(df.shape)


# 3. Convert numeric columns into low, medium, and high buckets.
transactions = pd.DataFrame(index=df.index)

bucket_columns = {
    "income": "annual_inc",
    "loan": "loan_amnt",
    "dti": "dti",
    "interest": "int_rate",
    "credit_history": "credit_history_years",
}

for bucket_name, column_name in bucket_columns.items():
    low_value = df[column_name].quantile(0.33)
    high_value = df[column_name].quantile(0.67)
    bucket_values = []

    for value in df[column_name]:
        if pd.isna(value):
            bucket_values.append(f"{bucket_name}=unknown")
        elif value <= low_value:
            bucket_values.append(f"{bucket_name}=low")
        elif value <= high_value:
            bucket_values.append(f"{bucket_name}=medium")
        else:
            bucket_values.append(f"{bucket_name}=high")

    transactions[f"{bucket_name}_bucket"] = bucket_values


# 4. Convert other useful columns into transaction items.
term_items = []
for value in df["term"]:
    if value <= 36:
        term_items.append("term=short")
    else:
        term_items.append("term=long")
transactions["term_bucket"] = term_items

grade_items = []
for value in df["grade"].astype(str):
    grade_items.append(f"grade={value}")
transactions["grade_bucket"] = grade_items

purpose_items = []
for value in df["purpose"].astype(str):
    purpose_items.append(f"purpose={value}")
transactions["purpose_bucket"] = purpose_items

default_items = []
for value in df["default_flag"]:
    if value == 1:
        default_items.append("default=yes")
    else:
        default_items.append("default=no")
transactions["default_bucket"] = default_items

print("\nTransaction data sample:")
print(transactions.head())


# 5. One-hot encode the transactions for Apriori.
encoded_transactions = pd.get_dummies(transactions).astype(bool)
print("\nEncoded transaction shape:")
print(encoded_transactions.shape)


# 6. Apply Apriori and generate association rules.
frequent_itemsets = apriori(encoded_transactions, min_support=0.05, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)

print("\nNumber of rules found:")
print(len(rules))


# 7. Keep rules related to default prediction.
if not rules.empty:
    antecedent_text = []
    consequent_text = []

    for items in rules["antecedents"]:
        antecedent_text.append(", ".join(sorted(items)))

    for items in rules["consequents"]:
        consequent_text.append(", ".join(sorted(items)))

    rules["antecedents"] = antecedent_text
    rules["consequents"] = consequent_text

    default_rules = rules[
        rules["consequents"].str.contains("default=yes|default=no", regex=True)
    ]
    default_rules = default_rules.sort_values(
        by=["lift", "confidence", "support"], ascending=False
    )
    final_rules = default_rules[
        ["antecedents", "consequents", "support", "confidence", "lift"]
    ].head(20)
else:
    final_rules = rules

print("\nTop association rules:")
print(final_rules)


# 8. Save association rules.
final_rules.to_csv(rules_file, index=False)
print(f"\nAssociation rules saved to: {rules_file}")


# 9. Save association rule report.
lines = [
    "# Association Rule Mining",
    "",
    "## Method",
    "- Used Apriori algorithm.",
    "- Converted numeric values into low, medium, and high buckets.",
    "- Used support, confidence, and lift to evaluate rules.",
    "",
]

if final_rules.empty:
    lines.append("No rules were found with the selected support and confidence values.")
else:
    lines.append("| Antecedent | Consequent | Support | Confidence | Lift |")
    lines.append("| --- | --- | --- | --- | --- |")

    for _, row in final_rules.iterrows():
        lines.append(
            f"| {row['antecedents']} | {row['consequents']} | "
            f"{row['support']:.4f} | {row['confidence']:.4f} | {row['lift']:.4f} |"
        )

report_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Association rule report saved to: {report_file}")
