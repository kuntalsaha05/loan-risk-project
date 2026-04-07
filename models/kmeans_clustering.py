from pathlib import Path
import json
import sys


try:
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
except ModuleNotFoundError:
    print(
        "Missing dependencies for clustering.\n"
        "Install project dependencies first, for example:\n"
        "pip install -r backend/requirements.txt"
    )
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "report"
PROCESSED_DATA_PATH = DATA_DIR / "processed_lending_club_loan.csv"
CLUSTERED_DATA_PATH = DATA_DIR / "clustered_loan_data.csv"
CLUSTER_SUMMARY_PATH = DATA_DIR / "cluster_summary.json"
REPORT_PATH = REPORT_DIR / "CLUSTERING_RESULTS.md"
MAX_SAMPLE_SIZE = 120000


def print_heading(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def load_data() -> pd.DataFrame:
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(f"Processed dataset not found: {PROCESSED_DATA_PATH}")
    df = pd.read_csv(PROCESSED_DATA_PATH, low_memory=False)
    if len(df) > MAX_SAMPLE_SIZE:
        df = df.sample(n=MAX_SAMPLE_SIZE, random_state=42)
    return df.reset_index(drop=True)


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    selected_features = [
        "loan_amnt",
        "int_rate",
        "annual_inc",
        "dti",
        "revol_util",
        "credit_history_years",
    ]
    available_features = [column for column in selected_features if column in df.columns]
    return df[available_features].copy()


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("kmeans", KMeans(n_clusters=3, random_state=42, n_init=10)),
        ]
    )


def map_risk_labels(
    feature_df: pd.DataFrame, original_df: pd.DataFrame, labels: pd.Series
) -> tuple[pd.Series, dict]:
    summary = (
        feature_df.assign(cluster_id=labels, default_flag=original_df["default_flag"].values)
        .groupby("cluster_id")
        .agg(
            default_rate=("default_flag", "mean"),
            avg_int_rate=("int_rate", "mean"),
            avg_dti=("dti", "mean"),
        )
        .reset_index()
    )

    summary["risk_score"] = (
        summary["default_rate"] * 0.5
        + summary["avg_int_rate"] / summary["avg_int_rate"].max() * 0.3
        + summary["avg_dti"] / summary["avg_dti"].max() * 0.2
    )
    summary = summary.sort_values("risk_score").reset_index(drop=True)

    risk_names = ["low_risk", "medium_risk", "high_risk"]
    label_mapping = {
        int(row["cluster_id"]): risk_names[index]
        for index, row in summary.iterrows()
    }

    return labels.map(label_mapping), label_mapping


def build_cluster_summary(df: pd.DataFrame, risk_labels: pd.Series) -> dict:
    cluster_df = df.copy()
    cluster_df["risk_cluster"] = risk_labels

    summary = (
        cluster_df.groupby("risk_cluster")
        .agg(
            records=("risk_cluster", "size"),
            avg_loan_amnt=("loan_amnt", "mean"),
            avg_int_rate=("int_rate", "mean"),
            avg_annual_inc=("annual_inc", "mean"),
            avg_dti=("dti", "mean"),
            default_rate=("default_flag", "mean"),
        )
        .round(4)
    )
    return summary.reset_index().to_dict(orient="records")


def write_report(summary_records: list[dict]) -> None:
    lines = [
        "# K-Means Clustering Results",
        "",
        "## Method",
        "- Used K-Means clustering with 3 clusters",
        "- Clustered borrowers into low, medium, and high risk groups",
        "- Used numeric loan and borrower risk features after preprocessing",
        "",
        "## Cluster Summary",
        "",
        "| Risk Cluster | Records | Avg Loan Amount | Avg Interest Rate | Avg Annual Income | Avg DTI | Default Rate |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for record in summary_records:
        lines.append(
            f"| {record['risk_cluster']} | {record['records']} | "
            f"{record['avg_loan_amnt']:.2f} | {record['avg_int_rate']:.2f} | "
            f"{record['avg_annual_inc']:.2f} | {record['avg_dti']:.2f} | "
            f"{record['default_rate']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "- Default rate is computed after clustering and is used only for interpretation.",
            "- Higher DTI and interest rates generally indicate stronger repayment risk.",
            "- These clusters can support segmentation, dashboards, and model explanations.",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    print_heading("STEP 1: LOAD PROCESSED DATA")
    df = load_data()
    print("Clustering dataset loaded")
    print("Shape after sampling:", df.shape)

    print_heading("STEP 2: SELECT CLUSTERING FEATURES")
    feature_df = prepare_features(df)
    print("K-Means input features:")
    print(feature_df.columns.tolist())
    print(feature_df.head())
    print("\nNote: default_flag is NOT used as a clustering input.")

    print_heading("STEP 3: APPLY K-MEANS CLUSTERING")
    pipeline = build_pipeline()
    cluster_ids = pd.Series(pipeline.fit_predict(feature_df), index=df.index)
    risk_labels, label_mapping = map_risk_labels(feature_df, df, cluster_ids)
    print("Cluster label mapping:")
    print(label_mapping)

    print_heading("STEP 4: CREATE CLUSTERED DATASET")
    result_df = df.copy()
    result_df["cluster_id"] = cluster_ids
    result_df["risk_cluster"] = risk_labels
    result_df.to_csv(CLUSTERED_DATA_PATH, index=False)

    summary_records = build_cluster_summary(df, risk_labels)
    print("Cluster summary:")
    print(pd.DataFrame(summary_records))
    summary_payload = {
        "label_mapping": label_mapping,
        "clusters": summary_records,
    }

    print_heading("STEP 5: SAVE CLUSTERING OUTPUTS")
    CLUSTER_SUMMARY_PATH.write_text(
        json.dumps(summary_payload, indent=2), encoding="utf-8"
    )
    write_report(summary_records)

    print(f"Clustered data saved to: {CLUSTERED_DATA_PATH}")
    print(f"Cluster summary saved to: {CLUSTER_SUMMARY_PATH}")
    print(f"Clustering report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
