# Loan Risk Project

This project is organized to align with syllabus Units I-IV and covers the full workflow from dataset understanding to analytics, machine learning, and system implementation.

## Current Setup

- Raw dataset: `data/lending_club_loan_two.csv`
- Preprocessing script: `backend/preprocess_data.py`
- ETL/database load script: `backend/load_to_database.py`
- System module: `backend/loan_risk_system.py`
- Association rule script: `models/association_rule_mining.py`
- Classification script: `models/train_classification_models.py`
- K-Means clustering script: `models/kmeans_clustering.py`
- Visualization script: `models/generate_visualizations.py`
- Python dependencies: `backend/requirements.txt`
- Report planning notes: `report/PROJECT_PLAN.md`
- Architecture diagram: `report/ARCHITECTURE_DIAGRAM.md`
- Frontend dashboard: `frontend/index.html`

## Frontend

Open `frontend/index.html` in a browser to view the project dashboard.
It presents:
- project summary metrics
- classification and clustering results
- demo prediction output
- what-if simulation table
- generated project visuals

## Syllabus-Aligned Process

### Step 1 - Understand Data (Unit I: Data Types)
- Download loan dataset in CSV format.
- Identify data types in the dataset:
  - Structured data: CSV dataset
  - Quantitative data: income, loan amount
  - Nominal data: loan status
  - Time-series data: issue date, payment date
- Document this in the dataset description section of the report.

### Step 2 - Data Preprocessing (Unit I)
- Perform data cleaning to handle missing values.
- Remove noisy data and outliers.
- Integrate relevant columns where needed.
- Transform data by creating new features such as:
  - `default_flag`
  - `default_stage`
- Reduce data using feature selection.
- Apply sampling if needed to reduce dataset size.

This step satisfies the Data Engineering and Preprocessing part of the syllabus.

### Step 3 - ETL Process (Unit II)
- Extract: load the CSV dataset.
- Transform: preprocess the data using Python.
- Load: store the processed data in a database.

The ETL pipeline should be clearly described in the report.

### Step 4 - Data Warehouse Design (Unit II)
- Create a simple warehouse schema.
- Fact table:
  - Loan transactions
- Dimension tables:
  - User dimension
  - Time dimension
  - Loan dimension
- Include a star schema diagram.

Also explain:
- OLTP: user input and transaction system
- OLAP: analytics and dashboard system

### Step 5 - Association Rule Mining (Unit III)
- Use the Apriori concept, even with a basic implementation.
- Find patterns such as:
  - High DTI + low income -> default
  - Large loan + short tenure -> high risk
- Generate association rules.
- Show support and confidence values.

This satisfies the association rule mining requirement.

### Step 6 - Supervised Learning (Unit IV)
- Train classification models:
  - Logistic Regression
  - Decision Tree
  - Random Forest
- Use these for:
  - Default prediction
  - Stage prediction

### Step 7 - Unsupervised Learning (Unit IV)
- Apply K-Means clustering.
- Cluster users into groups such as:
  - Low risk
  - Medium risk
  - High risk
- Visualize the clusters.

This satisfies the clustering techniques requirement.

### Step 8 - Visualization
- Create charts for:
  - Risk distribution
  - Clusters
  - Association rules
  - Feature importance

### Step 9 - System Implementation
- Build modules for:
  - Prediction
  - Stage classification
  - Interest recommendation
  - What-if simulation

### Step 10 - Architecture Diagram

```text
Dataset -> Preprocessing -> Data Warehouse ->
Association Mining -> ML Models ->
Frontend -> Output Dashboard
```

## Final Coverage
- Unit I: data preprocessing
- Unit II: ETL and data warehouse
- Unit III: association rule mining
- Unit IV: classification and K-Means clustering

This project plan keeps the implementation clearly aligned with the syllabus.
