from pathlib import Path
import json
import sys

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
except ModuleNotFoundError:
    print("Required visualization libraries are missing. Run: pip install -r backend/requirements.txt")
    sys.exit(1)


# 1. Set file paths.
base_dir = Path(__file__).resolve().parents[1]
data_dir = base_dir / "data"
report_dir = base_dir / "report"
visual_dir = report_dir / "visuals"
visual_dir.mkdir(parents=True, exist_ok=True)

processed_file = data_dir / "processed_lending_club_loan.csv"
clustered_file = data_dir / "clustered_loan_data.csv"
rules_file = data_dir / "association_rules.csv"
metrics_file = data_dir / "classification_metrics.json"
visual_report_file = report_dir / "VISUALIZATION_SUMMARY.md"

sns.set_theme(style="whitegrid")


# 2. Load required data files.
processed_df = pd.read_csv(processed_file, low_memory=False)
clustered_df = pd.read_csv(clustered_file, low_memory=False)
rules_df = pd.read_csv(rules_file)
metrics = json.loads(metrics_file.read_text(encoding="utf-8"))

print("Processed data shape:", processed_df.shape)
print("Clustered data shape:", clustered_df.shape)
print("Association rules shape:", rules_df.shape)


# 3. Create risk distribution chart.
risk_chart = visual_dir / "risk_distribution.png"
plt.figure(figsize=(8, 5))
sns.countplot(
    data=processed_df,
    x="default_stage",
    order=processed_df["default_stage"].value_counts().index,
)
plt.title("Risk Distribution by Default Stage")
plt.xlabel("Default Stage")
plt.ylabel("Count")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(risk_chart, dpi=200)
plt.close()
print(f"Risk distribution chart saved to: {risk_chart}")


# 4. Create cluster chart.
cluster_chart = visual_dir / "cluster_scatter.png"
sample_df = clustered_df.sample(n=min(len(clustered_df), 5000), random_state=42)
plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=sample_df,
    x="annual_inc",
    y="dti",
    hue="risk_cluster",
    palette="Set2",
    alpha=0.7,
    s=35,
)
plt.title("Borrower Clusters by Income and DTI")
plt.xlabel("Annual Income")
plt.ylabel("DTI")
plt.tight_layout()
plt.savefig(cluster_chart, dpi=200)
plt.close()
print(f"Cluster chart saved to: {cluster_chart}")


# 5. Create association rule chart.
rules_chart = visual_dir / "association_rules.png"
top_rules = rules_df.head(10).copy()

if top_rules.empty:
    plt.figure(figsize=(8, 5))
    plt.text(0.5, 0.5, "No association rules available", ha="center", va="center")
    plt.axis("off")
else:
    top_rules["rule_label"] = (
        top_rules["antecedents"].str.slice(0, 40)
        + " -> "
        + top_rules["consequents"].str.slice(0, 20)
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=top_rules,
        y="rule_label",
        x="confidence",
        hue="rule_label",
        palette="Blues_r",
        legend=False,
    )
    plt.title("Top Association Rules by Confidence")
    plt.xlabel("Confidence")
    plt.ylabel("Rule")

plt.tight_layout()
plt.savefig(rules_chart, dpi=200)
plt.close()
print(f"Association rule chart saved to: {rules_chart}")


# 6. Create model comparison chart.
model_chart = visual_dir / "feature_importance_proxy.png"
model_names = []
f1_scores = []

for model_name in metrics:
    model_names.append(model_name)
    f1_scores.append(metrics[model_name]["f1_score"])

model_df = pd.DataFrame({"model": model_names, "f1_score": f1_scores})

plt.figure(figsize=(8, 5))
sns.barplot(
    data=model_df,
    x="model",
    y="f1_score",
    hue="model",
    palette="Greens",
    legend=False,
)
plt.title("Model Performance Comparison")
plt.xlabel("Model")
plt.ylabel("F1 Score")
plt.xticks(rotation=10)
plt.tight_layout()
plt.savefig(model_chart, dpi=200)
plt.close()
print(f"Model comparison chart saved to: {model_chart}")


# 7. Save visualization summary report.
lines = [
    "# Visualization Summary",
    "",
    f"- Risk distribution chart: `visuals/{risk_chart.name}`",
    f"- Cluster chart: `visuals/{cluster_chart.name}`",
    f"- Association rule chart: `visuals/{rules_chart.name}`",
    f"- Model comparison chart: `visuals/{model_chart.name}`",
]

visual_report_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Visualization summary saved to: {visual_report_file}")
