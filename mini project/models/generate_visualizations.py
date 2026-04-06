"""
generate_visualizations.py - Create charts from project results.

This module reads processed data, cluster labels, association rules, and model metrics,
then saves images and a summary markdown file.
"""

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
    print(
        "Missing dependencies for visualization.\n"
        "Install project dependencies first, for example:\n"
        "pip install -r backend/requirements.txt"
    )
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "report"
VISUAL_DIR = REPORT_DIR / "visuals"

PROCESSED_DATA_PATH = DATA_DIR / "processed_lending_club_loan.csv"
CLUSTERED_DATA_PATH = DATA_DIR / "clustered_loan_data.csv"
ASSOCIATION_RULES_PATH = DATA_DIR / "association_rules.csv"
CLASSIFICATION_METRICS_PATH = DATA_DIR / "classification_metrics.json"
VISUAL_REPORT_PATH = REPORT_DIR / "VISUALIZATION_SUMMARY.md"


def ensure_output_dir() -> None:
    """Create the visual output directory if it does not exist."""
    VISUAL_DIR.mkdir(parents=True, exist_ok=True)


def plot_risk_distribution(df: pd.DataFrame) -> Path:
    """Plot the count of each loan default stage."""
    output_path = VISUAL_DIR / "risk_distribution.png"
    plt.figure(figsize=(8, 5))
    sns.countplot(
        data=df,
        x="default_stage",
        order=df["default_stage"].value_counts().index,
    )
    plt.title("Risk Distribution by Default Stage")
    plt.xlabel("Default Stage")
    plt.ylabel("Count")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def plot_clusters(df: pd.DataFrame) -> Path:
    """Plot borrower clusters by annual income and DTI."""
    output_path = VISUAL_DIR / "cluster_scatter.png"
    sample_df = df.sample(n=min(len(df), 5000), random_state=42)
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
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def plot_association_rules(df: pd.DataFrame) -> Path:
    """Plot the top association rules by confidence."""
    output_path = VISUAL_DIR / "association_rules.png"
    top_rules = df.head(10).copy()
    if top_rules.empty:
        plt.figure(figsize=(8, 5))
        plt.text(0.5, 0.5, "No association rules available", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=200)
        plt.close()
        return output_path

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
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def plot_feature_importance() -> Path:
    """Plot a comparison of model F1 scores as a proxy for feature importance."""
    output_path = VISUAL_DIR / "feature_importance_proxy.png"
    metrics = json.loads(CLASSIFICATION_METRICS_PATH.read_text(encoding="utf-8"))
    plot_df = pd.DataFrame(
        {
            "model": list(metrics.keys()),
            "f1_score": [metrics[name]["f1_score"] for name in metrics],
        }
    )
    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=plot_df,
        x="model",
        y="f1_score",
        hue="model",
        palette="Greens",
        legend=False,
    )
    plt.title("Model Performance Comparison (F1 Score)")
    plt.xlabel("Model")
    plt.ylabel("F1 Score")
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def write_report(paths: list[Path]) -> None:
    """Write a markdown file linking the generated visualizations."""
    lines = [
        "# Visualization Summary",
        "",
        "## Generated Charts",
        f"- Risk distribution: `visuals/{paths[0].name}`",
        f"- Cluster graph: `visuals/{paths[1].name}`",
        f"- Association rule chart: `visuals/{paths[2].name}`",
        f"- Feature importance / model comparison: `visuals/{paths[3].name}`",
        "",
        "## Purpose",
        "- Risk distribution graph supports borrower status analysis.",
        "- Cluster graph shows low, medium, and high risk segmentation.",
        "- Association rule chart highlights the strongest mined rules.",
        "- Model comparison graph summarizes supervised learning performance.",
    ]
    VISUAL_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Generate visual output and save a simple summary report."""
    ensure_output_dir()
    sns.set_theme(style="whitegrid")

    processed_df = pd.read_csv(PROCESSED_DATA_PATH, low_memory=False)
    clustered_df = pd.read_csv(CLUSTERED_DATA_PATH, low_memory=False)
    association_df = pd.read_csv(ASSOCIATION_RULES_PATH)

    image_paths = [
        plot_risk_distribution(processed_df),
        plot_clusters(clustered_df),
        plot_association_rules(association_df),
        plot_feature_importance(),
    ]
    write_report(image_paths)

    for path in image_paths:
        print(f"Generated visualization: {path}")
    print(f"Visualization summary saved to: {VISUAL_REPORT_PATH}")


if __name__ == "__main__":
    main()
