from pathlib import Path
import json
import sys


try:
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.tree import DecisionTreeClassifier
except ModuleNotFoundError:
    print(
        "Missing dependencies for system module.\n"
        "Install project dependencies first, for example:\n"
        "pip install -r backend/requirements.txt"
    )
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "report"
PROCESSED_DATA_PATH = DATA_DIR / "processed_lending_club_loan.csv"
SYSTEM_REPORT_PATH = REPORT_DIR / "SYSTEM_IMPLEMENTATION.md"
SAMPLE_OUTPUT_PATH = DATA_DIR / "system_demo_output.json"
MAX_SAMPLE_SIZE = 100000


def print_heading(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


class LoanRiskSystem:
    def __init__(self) -> None:
        self.feature_columns = [
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
        self.cluster_features = [
            "loan_amnt",
            "int_rate",
            "annual_inc",
            "dti",
            "revol_util",
            "credit_history_years",
        ]
        self.default_model: Pipeline | None = None
        self.cluster_pipeline: Pipeline | None = None
        self.cluster_label_map: dict[int, str] = {}
        self.training_default_flags: pd.Series | None = None

    def load_training_data(self) -> pd.DataFrame:
        if not PROCESSED_DATA_PATH.exists():
            raise FileNotFoundError(f"Processed dataset not found: {PROCESSED_DATA_PATH}")
        df = pd.read_csv(PROCESSED_DATA_PATH, low_memory=False)
        if len(df) > MAX_SAMPLE_SIZE:
            df = df.sample(n=MAX_SAMPLE_SIZE, random_state=42)
        return df.reset_index(drop=True)

    def build_preprocessor(self, X: pd.DataFrame) -> ColumnTransformer:
        categorical_columns = X.select_dtypes(include=["object", "string"]).columns.tolist()
        numeric_columns = [column for column in X.columns if column not in categorical_columns]

        return ColumnTransformer(
            transformers=[
                (
                    "num",
                    Pipeline(
                        steps=[
                            ("imputer", SimpleImputer(strategy="median")),
                            ("scaler", StandardScaler()),
                        ]
                    ),
                    numeric_columns,
                ),
                (
                    "cat",
                    Pipeline(
                        steps=[
                            ("imputer", SimpleImputer(strategy="most_frequent")),
                            ("encoder", OneHotEncoder(handle_unknown="ignore")),
                        ]
                    ),
                    categorical_columns,
                ),
            ]
        )

    def fit(self) -> None:
        print_heading("STEP 1: LOAD TRAINING DATA")
        df = self.load_training_data()
        print("System training dataset loaded")
        print("Shape after sampling:", df.shape)

        print_heading("STEP 2: TRAIN DEFAULT PREDICTION MODEL")
        X = df[self.feature_columns].copy()
        y = df["default_flag"].copy()
        print("Classification features:")
        print(X.columns.tolist())
        print("Target distribution:")
        print(y.value_counts(normalize=True))

        self.default_model = Pipeline(
            steps=[
                ("preprocessor", self.build_preprocessor(X)),
                ("classifier", DecisionTreeClassifier(max_depth=8, random_state=42)),
            ]
        )
        self.default_model.fit(X, y)
        print("Decision Tree classifier trained")

        print_heading("STEP 3: TRAIN RISK CLUSTER MODEL")
        cluster_df = df[self.cluster_features].copy()
        self.training_default_flags = y.reset_index(drop=True)
        print("Clustering features:")
        print(cluster_df.columns.tolist())
        print("Note: default_flag is used only to label clusters after K-Means.")
        self.cluster_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("kmeans", KMeans(n_clusters=3, random_state=42, n_init=10)),
            ]
        )
        cluster_ids = pd.Series(self.cluster_pipeline.fit_predict(cluster_df), index=cluster_df.index)
        self.cluster_label_map = self._build_cluster_label_map(cluster_df, cluster_ids)
        print("Cluster label mapping:")
        print(self.cluster_label_map)

    def _build_cluster_label_map(
        self, cluster_df: pd.DataFrame, cluster_ids: pd.Series
    ) -> dict[int, str]:
        if self.training_default_flags is None:
            raise RuntimeError("Training labels are not available for cluster mapping.")
        summary = (
            cluster_df.assign(
                cluster_id=cluster_ids,
                default_flag=self.training_default_flags.values,
            )
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
        return {
            int(row["cluster_id"]): risk_names[index]
            for index, row in summary.iterrows()
        }

    def _predict_default_probability(self, profile: dict) -> float:
        if self.default_model is None:
            raise RuntimeError("System model is not fitted.")
        input_df = pd.DataFrame([profile], columns=self.feature_columns)
        probability = float(self.default_model.predict_proba(input_df)[0][1])
        return round(probability, 4)

    def _classify_stage(self, default_probability: float) -> str:
        if default_probability < 0.15:
            return "non_default"
        if default_probability < 0.35:
            return "active"
        if default_probability < 0.60:
            return "delinquent"
        return "default"

    def _recommend_interest_rate(self, profile: dict, default_probability: float, risk_cluster: str) -> float:
        base_rate = float(profile["int_rate"])
        if risk_cluster == "low_risk":
            recommended = max(6.0, base_rate - 1.0)
        elif risk_cluster == "medium_risk":
            recommended = base_rate
        else:
            recommended = min(24.0, base_rate + 1.5 + default_probability * 2)
        return round(recommended, 2)

    def _predict_risk_cluster(self, profile: dict, default_probability: float) -> str:
        if self.cluster_pipeline is None:
            raise RuntimeError("Cluster model is not fitted.")
        cluster_profile = {
            "loan_amnt": profile["loan_amnt"],
            "int_rate": profile["int_rate"],
            "annual_inc": profile["annual_inc"],
            "dti": profile["dti"],
            "revol_util": profile["revol_util"],
            "credit_history_years": profile["credit_history_years"],
        }
        cluster_df = pd.DataFrame([cluster_profile], columns=self.cluster_features)
        cluster_id = int(self.cluster_pipeline.predict(cluster_df)[0])
        return self.cluster_label_map.get(cluster_id, "medium_risk")

    def predict(self, profile: dict) -> dict:
        default_probability = self._predict_default_probability(profile)
        risk_cluster = self._predict_risk_cluster(profile, default_probability)
        default_stage = self._classify_stage(default_probability)
        recommended_interest = self._recommend_interest_rate(
            profile, default_probability, risk_cluster
        )

        return {
            "default_probability": default_probability,
            "default_stage": default_stage,
            "risk_cluster": risk_cluster,
            "recommended_interest_rate": recommended_interest,
        }

    def what_if_simulation(self, profile: dict) -> list[dict]:
        scenarios = [
            ("base_case", profile),
            (
                "lower_loan_amount",
                {**profile, "loan_amnt": round(profile["loan_amnt"] * 0.85, 2)},
            ),
            (
                "lower_dti",
                {**profile, "dti": round(max(0.0, profile["dti"] - 5), 2)},
            ),
            (
                "shorter_term",
                {**profile, "term": 36.0, "installment": round(profile["installment"] * 1.1, 2)},
            ),
        ]

        results = []
        for scenario_name, scenario_profile in scenarios:
            scenario_result = self.predict(scenario_profile)
            results.append(
                {
                    "scenario": scenario_name,
                    "loan_amnt": scenario_profile["loan_amnt"],
                    "dti": scenario_profile["dti"],
                    "term": scenario_profile["term"],
                    "default_probability": scenario_result["default_probability"],
                    "default_stage": scenario_result["default_stage"],
                    "risk_cluster": scenario_result["risk_cluster"],
                    "recommended_interest_rate": scenario_result["recommended_interest_rate"],
                }
            )
        return results


def build_demo_profile() -> dict:
    return {
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


def write_system_report() -> None:
    lines = [
        "# System Implementation",
        "",
        "## Modules",
        "- Default prediction using Decision Tree classification",
        "- Stage classification using probability thresholds",
        "- Interest recommendation using predicted risk level",
        "- What-if simulation for borrower scenario comparison",
        "",
        "## Input Features",
        "- Loan amount, term, interest rate, installment",
        "- Credit and income related borrower features",
        "- Verification status, purpose, grade, and sub-grade",
        "",
        "## Output",
        "- Default probability",
        "- Default stage",
        "- Risk cluster",
        "- Recommended interest rate",
        "- Scenario comparison for what-if analysis",
    ]
    SYSTEM_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    print_heading("LOAN RISK SYSTEM DEMO")
    system = LoanRiskSystem()
    system.fit()

    print_heading("STEP 4: BUILD DEMO BORROWER PROFILE")
    demo_profile = build_demo_profile()
    print(demo_profile)

    print_heading("STEP 5: PREDICT RISK AND RUN WHAT-IF SIMULATION")
    prediction = system.predict(demo_profile)
    simulation = system.what_if_simulation(demo_profile)
    print("Prediction result:")
    print(json.dumps(prediction, indent=2))
    print("What-if simulation:")
    print(json.dumps(simulation, indent=2))

    payload = {
        "input_profile": demo_profile,
        "prediction": prediction,
        "what_if_simulation": simulation,
    }

    print_heading("STEP 6: SAVE SYSTEM OUTPUTS")
    SAMPLE_OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_system_report()

    print(f"System demo output saved to: {SAMPLE_OUTPUT_PATH}")
    print(f"System implementation report saved to: {SYSTEM_REPORT_PATH}")


if __name__ == "__main__":
    main()
