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
    print(
        "Missing dependencies for model training.\n"
        "Install project dependencies first, for example:\n"
        "pip install -r backend/requirements.txt"
    )
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "report"
PROCESSED_DATA_PATH = DATA_DIR / "processed_lending_club_loan.csv"
METRICS_JSON_PATH = DATA_DIR / "classification_metrics.json"
REPORT_PATH = REPORT_DIR / "CLASSIFICATION_RESULTS.md"
MAX_SAMPLE_SIZE = 120000


def load_data() -> pd.DataFrame:
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(f"Processed dataset not found: {PROCESSED_DATA_PATH}")
    df = pd.read_csv(PROCESSED_DATA_PATH, low_memory=False)
    if len(df) > MAX_SAMPLE_SIZE:
        default_counts = df["default_flag"].value_counts(normalize=True)
        sampled_parts = []
        for class_value, class_fraction in default_counts.items():
            class_rows = df[df["default_flag"] == class_value]
            class_sample_size = max(1, int(round(MAX_SAMPLE_SIZE * class_fraction)))
            class_sample_size = min(class_sample_size, len(class_rows))
            sampled_parts.append(
                class_rows.sample(n=class_sample_size, random_state=42)
            )
        df = pd.concat(sampled_parts, ignore_index=True)
    return df.reset_index(drop=True)


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
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

    available_features = [column for column in feature_columns if column in df.columns]
    X = df[available_features].copy()
    y = df["default_flag"].copy()
    return X, y


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    categorical_columns = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numeric_columns = [column for column in X.columns if column not in categorical_columns]

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

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_columns),
            ("cat", categorical_pipeline, categorical_columns),
        ]
    )


def train_and_evaluate(X: pd.DataFrame, y: pd.Series) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor(X)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=150, max_depth=12, random_state=42, n_jobs=1
        ),
    }

    results = {}
    for model_name, estimator in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", estimator),
            ]
        )

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        results[model_name] = {
            "accuracy": round(accuracy_score(y_test, predictions), 4),
            "f1_score": round(f1_score(y_test, predictions, zero_division=0), 4),
            "classification_report": classification_report(
                y_test, predictions, zero_division=0
            ),
        }

    return results


def write_report(results: dict) -> None:
    lines = [
        "# Classification Results",
        "",
        "## Models Used",
        "- Logistic Regression",
        "- Decision Tree",
        "- Random Forest",
        "",
        "## Evaluation Summary",
        "",
        "| Model | Accuracy | F1 Score |",
        "| --- | --- | --- |",
    ]

    for model_name, metrics in results.items():
        lines.append(
            f"| {model_name} | {metrics['accuracy']:.4f} | {metrics['f1_score']:.4f} |"
        )

    best_model = max(results.items(), key=lambda item: item[1]["f1_score"])
    lines.extend(
        [
            "",
            "## Best Model",
            f"- Based on F1 score, the best model is `{best_model[0]}`.",
            "",
            "## Detailed Reports",
        ]
    )

    for model_name, metrics in results.items():
        lines.extend(
            [
                "",
                f"### {model_name}",
                "```text",
                metrics["classification_report"].rstrip(),
                "```",
            ]
        )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    df = load_data()
    X, y = prepare_features(df)
    results = train_and_evaluate(X, y)
    METRICS_JSON_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_report(results)
    print(f"Classification metrics saved to: {METRICS_JSON_PATH}")
    print(f"Classification report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
