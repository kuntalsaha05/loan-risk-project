from pathlib import Path
import json
import os
import sys

# Fixes a Windows warning from joblib when scikit-learn checks CPU cores.
os.environ["LOKY_MAX_CPU_COUNT"] = "4"

try:
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.tree import DecisionTreeClassifier
except ModuleNotFoundError:
    print("Required system libraries are missing. Run: pip install -r backend/requirements.txt")
    sys.exit(1)


# 1. Set file paths.
base_dir = Path(__file__).resolve().parents[1]
data_dir = base_dir / "data"
report_dir = base_dir / "report"

processed_file = data_dir / "processed_lending_club_loan.csv"
output_file = data_dir / "system_demo_output.json"
report_file = report_dir / "SYSTEM_IMPLEMENTATION.md"


# 2. Load the processed dataset.
df = pd.read_csv(processed_file, low_memory=False)

max_sample_size = 100000
if len(df) > max_sample_size:
    df = df.sample(n=max_sample_size, random_state=42)

df = df.reset_index(drop=True)
print("System training dataset loaded:")
print(df.shape)


# 3. Select features for default prediction.
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

X = df[feature_columns]
y = df["default_flag"]

categorical_columns = X.select_dtypes(include=["object", "string"]).columns.tolist()
numeric_columns = []
for column in X.columns:
    if column not in categorical_columns:
        numeric_columns.append(column)


# 4. Build preprocessing for numeric and categorical data.
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


# 5. Train the Decision Tree model for default prediction.
default_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(max_depth=8, random_state=42)),
    ]
)

default_model.fit(X, y)
print("\nDefault prediction model trained.")


# 6. Train K-Means model for risk clustering.
cluster_columns = [
    "loan_amnt",
    "int_rate",
    "annual_inc",
    "dti",
    "revol_util",
    "credit_history_years",
]

cluster_input = df[cluster_columns]
cluster_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("kmeans", KMeans(n_clusters=3, random_state=42, n_init=10)),
    ]
)

cluster_ids = cluster_pipeline.fit_predict(cluster_input)
df["cluster_id"] = cluster_ids

cluster_summary = (
    df.groupby("cluster_id")
    .agg(
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
    risk_map[int(row["cluster_id"])] = risk_names[index]

print("Cluster label mapping:")
print(risk_map)


# 7. Create one demo borrower profile.
demo_profile = {
    "loan_amnt": 12000.0,
    "term": 36.0,
    "int_rate": 11.5,
    "installment": 395.0,
    "grade": "B",
    "sub_grade": "B3",
    "annual_inc": 72000.0,
    "verification_status": "Verified",
    "purpose": "debt_consolidation",
    "dti": 18.4,
    "open_acc": 10.0,
    "pub_rec": 0.0,
    "revol_bal": 14500.0,
    "revol_util": 52.0,
    "mort_acc": 1.0,
    "pub_rec_bankruptcies": 0.0,
    "issue_year": 2019,
    "issue_month": 6,
    "credit_history_years": 8.5,
}

demo_df = pd.DataFrame([demo_profile], columns=feature_columns)


# 8. Predict default probability.
default_probability = float(default_model.predict_proba(demo_df)[0][1])
default_probability = round(default_probability, 4)

if default_probability < 0.15:
    default_stage = "non_default"
elif default_probability < 0.35:
    default_stage = "active"
elif default_probability < 0.60:
    default_stage = "delinquent"
else:
    default_stage = "default"


# 9. Predict risk cluster.
cluster_profile = pd.DataFrame([demo_profile], columns=cluster_columns)
cluster_id = int(cluster_pipeline.predict(cluster_profile)[0])
risk_cluster = risk_map.get(cluster_id, "medium_risk")


# 10. Recommend interest rate.
base_rate = demo_profile["int_rate"]
if risk_cluster == "low_risk":
    recommended_interest = max(6.0, base_rate - 1.0)
elif risk_cluster == "medium_risk":
    recommended_interest = base_rate
else:
    recommended_interest = min(24.0, base_rate + 1.5 + default_probability * 2)

recommended_interest = round(recommended_interest, 2)

prediction = {
    "default_probability": default_probability,
    "default_stage": default_stage,
    "risk_cluster": risk_cluster,
    "recommended_interest_rate": recommended_interest,
}

print("\nPrediction result:")
print(json.dumps(prediction, indent=2))


# 11. Run simple what-if simulation.
scenarios = []

base_case = demo_profile.copy()
scenarios.append(("base_case", base_case))

lower_loan = demo_profile.copy()
lower_loan["loan_amnt"] = round(lower_loan["loan_amnt"] * 0.85, 2)
scenarios.append(("lower_loan_amount", lower_loan))

lower_dti = demo_profile.copy()
lower_dti["dti"] = round(max(0.0, lower_dti["dti"] - 5), 2)
scenarios.append(("lower_dti", lower_dti))

shorter_term = demo_profile.copy()
shorter_term["term"] = 36.0
shorter_term["installment"] = round(shorter_term["installment"] * 1.1, 2)
scenarios.append(("shorter_term", shorter_term))

simulation_results = []
for scenario_name, scenario_profile in scenarios:
    scenario_df = pd.DataFrame([scenario_profile], columns=feature_columns)
    scenario_probability = float(default_model.predict_proba(scenario_df)[0][1])
    scenario_probability = round(scenario_probability, 4)

    if scenario_probability < 0.15:
        scenario_stage = "non_default"
    elif scenario_probability < 0.35:
        scenario_stage = "active"
    elif scenario_probability < 0.60:
        scenario_stage = "delinquent"
    else:
        scenario_stage = "default"

    scenario_cluster_df = pd.DataFrame([scenario_profile], columns=cluster_columns)
    scenario_cluster_id = int(cluster_pipeline.predict(scenario_cluster_df)[0])
    scenario_risk_cluster = risk_map.get(scenario_cluster_id, "medium_risk")

    simulation_results.append(
        {
            "scenario": scenario_name,
            "loan_amnt": scenario_profile["loan_amnt"],
            "dti": scenario_profile["dti"],
            "term": scenario_profile["term"],
            "default_probability": scenario_probability,
            "default_stage": scenario_stage,
            "risk_cluster": scenario_risk_cluster,
        }
    )

print("\nWhat-if simulation:")
print(json.dumps(simulation_results, indent=2))


# 12. Save system output.
output_data = {
    "input_profile": demo_profile,
    "prediction": prediction,
    "what_if_simulation": simulation_results,
}

output_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
print(f"\nSystem demo output saved to: {output_file}")


# 13. Save system report.
report_lines = [
    "# System Implementation",
    "",
    "- Default prediction using Decision Tree.",
    "- Risk grouping using K-Means clustering.",
    "- Stage classification using probability ranges.",
    "- Interest recommendation using risk cluster.",
    "- What-if simulation using changed borrower values.",
]

report_file.write_text("\n".join(report_lines), encoding="utf-8")
print(f"System report saved to: {report_file}")
