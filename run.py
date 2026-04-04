"""
run.py - Full pipeline runner for the Loan Risk Project.

Runs each stage in order:
  1. Data preprocessing
  2. ETL / database load
  3. Classification model training
  4. K-Means clustering
  5. Association rule mining
  6. Visualization generation
  7. System demo (prediction + what-if simulation)

Usage:
    python run.py
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

STEPS = [
    ("Preprocessing data", [sys.executable, "backend/preprocess_data.py"]),
    ("Loading data into database", [sys.executable, "backend/load_to_database.py"]),
    ("Training classification models", [sys.executable, "models/train_classification_models.py"]),
    ("Running K-Means clustering", [sys.executable, "models/kmeans_clustering.py"]),
    ("Mining association rules", [sys.executable, "models/association_rule_mining.py"]),
    ("Generating visualizations", [sys.executable, "models/generate_visualizations.py"]),
    ("Running system demo", [sys.executable, "backend/loan_risk_system.py"]),
]


def run_step(label: str, command: list[str]) -> bool:
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")
    result = subprocess.run(command, cwd=BASE_DIR)
    if result.returncode != 0:
        print(f"\n[ERROR] Step failed: {label}")
        return False
    return True


def main() -> None:
    print("Loan Risk Project - Full Pipeline Runner")
    print("=========================================")

    for label, command in STEPS:
        if not run_step(label, command):
            print("\nPipeline stopped due to an error.")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("  Pipeline complete.")
    print("=" * 60)
    print("\nOpen frontend/index.html in a browser to view the dashboard.")


if __name__ == "__main__":
    main()
