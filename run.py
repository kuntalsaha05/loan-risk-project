import subprocess
import sys
from pathlib import Path


# 1. Set the project folder.
base_dir = Path(__file__).resolve().parent


# 2. List all scripts in the order they should run.
steps = [
    ["Preprocessing data", "backend/preprocess_data.py"],
    ["Loading data into database", "backend/load_to_database.py"],
    ["Training classification models", "models/train_classification_models.py"],
    ["Running K-Means clustering", "models/kmeans_clustering.py"],
    ["Mining association rules", "models/association_rule_mining.py"],
    ["Generating visualizations", "models/generate_visualizations.py"],
    ["Running system demo", "backend/loan_risk_system.py"],
]


# 3. Run each script one by one.
print("Loan Risk Project - Full Pipeline")

for step in steps:
    step_name = step[0]
    script_path = step[1]

    print("\n" + "=" * 60)
    print(step_name)
    print("=" * 60)

    result = subprocess.run([sys.executable, script_path], cwd=base_dir)

    if result.returncode != 0:
        print(f"Stopped because this step failed: {step_name}")
        sys.exit(1)


# 4. Show final message.
print("\nPipeline completed successfully.")
print("Open frontend/index.html to view the dashboard.")
