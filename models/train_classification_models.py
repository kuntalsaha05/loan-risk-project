from pathlib import Path
import json
import sys

try:
    import pandas as pd
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, classification_report, f1_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.tree import DecisionTreeClassifier
except ModuleNotFoundError:
    print("Required ML libraries are missing. Run: pip install -r backend/requirements.txt")
    sys.exit(1)


# 1. Set file paths.
base_dir = Path(__file__).resolve().parents[1]
data_dir = base_dir / "data"
report_dir = base_dir / "report"

processed_file = data_dir / "processed_lending_club_loan.csv"
metrics_file = data_dir / "classification_metrics.json"
report_file = report_dir / "CLASSIFICATION_RESULTS.md"


# 2. Load the processed dataset.
df = pd.read_csv(processed_file, low_memory=False)
print("Dataset loaded:")
print(df.shape)


# 3. Take a sample to make training faster.
max_sample_size = 120000
if len(df) > max_sample_size:
    df = df.sample(n=max_sample_size, random_state=42)

print("\nDataset shape after sampling:")
print(df.shape)


# 4. Select input features and target column.
feature_columns = [
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "sub_grade",
    "annual_inc",
    "verification_status",
    "purpose",
    "dti",
    "open_acc",
    "pub_rec",
    "revol_bal",
    "revol_util",
    "mort_acc",
    "pub_rec_bankruptcies",
    "issue_year",
    "issue_month",
    "credit_history_years",
]

available_features = []
for column in feature_columns:
    if column in df.columns:
        available_features.append(column)

X = df[available_features]
y = df["default_flag"]

print("\nFeature columns:")
print(available_features)
print("\nTarget distribution:")
print(y.value_counts(normalize=True))


# 5. Split the data into training and testing data.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# 6. Prepare numeric and categorical columns.
categorical_columns = X.select_dtypes(include=["object", "string"]).columns.tolist()
numeric_columns = []
for column in X.columns:
    if column not in categorical_columns:
        numeric_columns.append(column)

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, numeric_columns),
        ("cat", categorical_pipeline, categorical_columns),
    ]
)


# 7. Create the three classification models.
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=42),
    "Random Forest": RandomForestClassifier(
        n_estimators=150, max_depth=12, random_state=42, n_jobs=1
    ),
}


# 8. Train and evaluate each model.
results = {}
for model_name, model in models.items():
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, zero_division=0)
    report = classification_report(y_test, predictions, zero_division=0)

    results[model_name] = {
        "accuracy": round(accuracy, 4),
        "f1_score": round(f1, 4),
        "classification_report": report,
    }

print("\nModel comparison:")
print(pd.DataFrame(results).T[["accuracy", "f1_score"]])


# 9. Save the metrics as JSON.
metrics_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
print(f"\nClassification metrics saved to: {metrics_file}")


# 10. Save the report as Markdown.
lines = [
    "# Classification Results",
    "",
    "| Model | Accuracy | F1 Score |",
    "| --- | --- | --- |",
]

for model_name, metrics in results.items():
    lines.append(
        f"| {model_name} | {metrics['accuracy']:.4f} | {metrics['f1_score']:.4f} |"
    )

lines.append("")
lines.append("## Detailed Reports")

for model_name, metrics in results.items():
    lines.append("")
    lines.append(f"### {model_name}")
    lines.append("```text")
    lines.append(metrics["classification_report"].rstrip())
    lines.append("```")

report_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Classification report saved to: {report_file}")
