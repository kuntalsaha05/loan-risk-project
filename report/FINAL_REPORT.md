# Loan Risk Analysis and Prediction System

## Abstract
This project builds a loan risk analysis and prediction system using a real loan dataset. The work is aligned with syllabus Units I-IV and covers data understanding, preprocessing, ETL, data warehouse design, association rule mining, supervised learning, unsupervised learning, visualization, system implementation, and architecture design.

## 1. Introduction
Loan default prediction is important for banks and financial institutions because it helps reduce losses and improve decision-making. In this project, a loan dataset is analyzed to identify risky borrowers, discover patterns, and build predictive models for loan default and borrower segmentation.

The main objectives of the project are:
- understand the structure of the loan dataset
- preprocess and transform the data
- build an ETL pipeline and simple warehouse layer
- apply association rule mining
- train classification models for default prediction
- apply K-Means clustering for borrower grouping
- generate visualizations
- implement a prediction and recommendation system

## 2. Dataset Description
The dataset used in the project is:
- `lending_club_loan_two.csv`

It is a structured CSV dataset containing borrower, loan, and repayment-related attributes.

### Data Types
- Structured data: CSV dataset
- Quantitative data: loan amount, annual income, DTI, interest rate
- Nominal data: loan status, grade, purpose, verification status
- Time-related data: issue date, earliest credit line

### Processed Dataset Summary
- Rows: 396030
- Selected columns: 24

Important processed features include:
- `default_flag`
- `default_stage`
- `issue_year`
- `issue_month`
- `credit_history_years`

## 3. Data Preprocessing
The preprocessing stage was implemented in [preprocess_data.py](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/backend/preprocess_data.py).

The following operations were performed:
- missing value handling
- removal of unnecessary columns
- outlier clipping using the IQR approach
- data transformation for date fields
- feature engineering for `default_flag` and `default_stage`
- feature reduction by selecting relevant columns

This stage satisfies Unit I requirements for preprocessing and data engineering.

## 4. ETL Process
The ETL stage was implemented in [load_to_database.py](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/backend/load_to_database.py).

### Extract
- the processed CSV file was read from the `data` folder

### Transform
- date fields were standardized for storage
- cleaned and selected features were preserved

### Load
- the processed data was loaded into a SQLite database:
  - database: `loan_risk.db`
  - table: `loan_records`

This satisfies Unit II ETL requirements.

## 5. Data Warehouse Design
A simple star-schema style warehouse design was prepared.

### Fact Table
- `fact_loan_transactions`

### Dimension Tables
- `dim_user`
- `dim_time`
- `dim_loan`

### Concepts Covered
- OLTP: transaction and input side of the system
- OLAP: analysis and reporting side of the system

This satisfies the Unit II warehouse component.

## 6. Association Rule Mining
Association rule mining was implemented in [association_rule_mining.py](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/models/association_rule_mining.py) using the Apriori concept.

The script transformed continuous features into categorical buckets and generated rules using:
- support
- confidence
- lift

### Example Findings
- grade A with high income and short term is strongly associated with `default=no`
- grade A with low DTI and low interest is also strongly associated with `default=no`

The results were saved in:
- [association_rules.csv](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/data/association_rules.csv)
- [ASSOCIATION_RULES.md](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/report/ASSOCIATION_RULES.md)

This satisfies Unit III association rule mining.

## 7. Supervised Learning
Classification models were implemented in [train_classification_models.py](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/models/train_classification_models.py).

### Models Used
- Logistic Regression
- Decision Tree
- Random Forest

### Target
- `default_flag`

### Results
| Model | Accuracy | F1 Score |
| --- | --- | --- |
| Logistic Regression | 0.8056 | 0.0876 |
| Decision Tree | 0.8017 | 0.1476 |
| Random Forest | 0.8047 | 0.0358 |

### Best Model
- Decision Tree performed best based on F1 score.

This satisfies the Unit IV classification requirement.

## 8. Unsupervised Learning
K-Means clustering was implemented in [kmeans_clustering.py](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/models/kmeans_clustering.py).

Borrowers were grouped into:
- low risk
- medium risk
- high risk

### Cluster Summary
| Risk Cluster | Records | Default Rate |
| --- | --- | --- |
| low_risk | 41823 | 0.1199 |
| medium_risk | 29702 | 0.1893 |
| high_risk | 48475 | 0.2673 |

The clustering was corrected to avoid using `default_flag` as an input feature. The default rate is now measured after clustering for interpretation only.

This satisfies the Unit IV clustering requirement.

## 9. Visualization
Visualizations were generated to support analysis and reporting:
- risk distribution graph
- cluster scatter graph
- association rule confidence chart
- model comparison graph

Generated files:
- [risk_distribution.png](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/report/visuals/risk_distribution.png)
- [cluster_scatter.png](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/report/visuals/cluster_scatter.png)
- [association_rules.png](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/report/visuals/association_rules.png)
- [feature_importance_proxy.png](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/report/visuals/feature_importance_proxy.png)

## 10. System Implementation
The integrated system module was implemented in [loan_risk_system.py](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/backend/loan_risk_system.py).

### Features of the System
- default prediction
- stage classification
- interest recommendation
- what-if simulation

### Demo Output
For a sample borrower profile, the system predicted:
- default probability: 0.081
- default stage: non_default
- risk cluster: low_risk
- recommended interest rate: 10.5

This satisfies the implementation component of the project.

## 11. Architecture
The project architecture follows this flow:

```text
Dataset -> Preprocessing -> ETL / Database -> Association Mining ->
Classification + Clustering -> Visualization -> System Module -> Output
```

The detailed architecture is documented in [ARCHITECTURE_DIAGRAM.md](c:/Users/sahak/Documents/AIDS/Projects/loan-risk-project/report/ARCHITECTURE_DIAGRAM.md).

## 12. Syllabus Mapping
- Unit I: data types and preprocessing
- Unit II: ETL and data warehouse
- Unit III: association rule mining
- Unit IV: classification and clustering

## 13. Conclusion
This project successfully developed a loan risk analysis and prediction system aligned with the syllabus. The dataset was cleaned and transformed, loaded into a database, analyzed using association rules, modeled using classification and clustering techniques, and connected to a system module for practical prediction and recommendation.

The project demonstrates how data engineering, data mining, machine learning, and reporting can be integrated into one complete analytical workflow.
