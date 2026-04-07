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
    print("Required clustering libraries are missing. Run: pip install -r backend/requirements.txt")
    sys.exit(1)


# 1. Set file paths.
base_dir = Path(__file__).resolve().parents[1]
data_dir = base_dir / "data"
report_dir = base_dir / "report"

processed_file = data_dir / "processed_lending_club_loan.csv"
clustered_file = data_dir / "clustered_loan_data.csv"
summary_file = data_dir / "cluster_summary.json"
report_file = report_dir / "CLUSTERING_RESULTS.md"


# 2. Load the processed dataset.
df = pd.read_csv(processed_file, low_memory=False)
print("Dataset loaded:")
print(df.shape)


# 3. Take a sample to make clustering faster.
max_sample_size = 120000
if len(df) > max_sample_size:
    df = df.sample(n=max_sample_size, random_state=42)

df = df.reset_index(drop=True)
print("\nDataset shape after sampling:")
print(df.shape)


# 4. Select numeric columns for K-Means clustering.
cluster_columns = [
    "loan_amnt",
    "int_rate",
    "annual_inc",
    "dti",
    "revol_util",
    "credit_history_years",
]

available_columns = []
for column in cluster_columns:
    if column in df.columns:
        available_columns.append(column)

cluster_input = df[available_columns]
print("\nK-Means input columns:")
print(available_columns)


# 5. Create and run K-Means clustering.
pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("kmeans", KMeans(n_clusters=3, random_state=42, n_init=10)),
    ]
)

cluster_ids = pipeline.fit_predict(cluster_input)
df["cluster_id"] = cluster_ids


# 6. Find which cluster is low, medium, and high risk.
cluster_summary = (
    df.groupby("cluster_id")
    .agg(
        records=("cluster_id", "size"),
        default_rate=("default_flag", "mean"),
        avg_int_rate=("int_rate", "mean"),
        avg_dti=("dti", "mean"),
    )
    .reset_index()
)

cluster_summary["risk_score"] = (
    cluster_summary["default_rate"] * 0.5
    + cluster_summary["avg_int_rate"] / cluster_summary["avg_int_rate"].max() * 0.3
    + cluster_summary["avg_dti"] / cluster_summary["avg_dti"].max() * 0.2
)

cluster_summary = cluster_summary.sort_values("risk_score").reset_index(drop=True)

risk_names = ["low_risk", "medium_risk", "high_risk"]
risk_map = {}
for index, row in cluster_summary.iterrows():
    cluster_id = int(row["cluster_id"])
    risk_map[cluster_id] = risk_names[index]

df["risk_cluster"] = df["cluster_id"].map(risk_map)

print("\nCluster label mapping:")
print(risk_map)


# 7. Save clustered dataset.
df.to_csv(clustered_file, index=False)
print(f"\nClustered data saved to: {clustered_file}")


# 8. Save cluster summary.
summary_records = cluster_summary.to_dict(orient="records")
summary_payload = {
    "label_mapping": risk_map,
    "clusters": summary_records,
}
summary_file.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")
print(f"Cluster summary saved to: {summary_file}")


# 9. Save clustering report.
lines = [
    "# K-Means Clustering Results",
    "",
    "| Cluster ID | Risk Name | Records | Default Rate | Avg Interest Rate | Avg DTI |",
    "| --- | --- | --- | --- | --- | --- |",
]

for _, row in cluster_summary.iterrows():
    cluster_id = int(row["cluster_id"])
    risk_name = risk_map[cluster_id]
    lines.append(
        f"| {cluster_id} | {risk_name} | {int(row['records'])} | "
        f"{row['default_rate']:.4f} | {row['avg_int_rate']:.2f} | {row['avg_dti']:.2f} |"
    )

report_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Clustering report saved to: {report_file}")
