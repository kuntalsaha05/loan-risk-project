# DET Mini Project PPT Content

## Slide 1: Title Slide
**Title:** Loan Risk Analysis and Prediction System  
**Course:** DET Mini Project  
**Prepared By:** Student Name  
**Topic:** Data Exploration, Preprocessing, Mining, Machine Learning, and Visualization

## Slide 2: Project Objective
- Analyze a real loan dataset
- Identify factors related to loan default
- Apply preprocessing and feature engineering
- Use supervised and unsupervised learning techniques
- Present results through charts, clustering, and prediction outputs

## Slide 3: Dataset Overview
- Dataset used: `lending_club_loan_two.csv`
- Type: Structured CSV dataset
- Total rows: 396,030
- Selected columns after preprocessing: 24

### Dataset Features
- Quantitative: loan amount, annual income, DTI, interest rate
- Nominal: loan status, grade, purpose, verification status
- Time-related: issue date, earliest credit line

## Slide 4: Dataset Exploration and Analysis
- Explored column names, data types, and dataset shape
- Identified numerical and categorical features
- Studied important borrower-related fields such as:
  - `loan_amnt`
  - `annual_inc`
  - `dti`
  - `loan_status`
  - `grade`
- Created dataset description and summary report

### Key Findings
- The dataset is structured and suitable for machine learning
- Loan status is the target behavior for default analysis
- Income, DTI, and grade are important risk indicators

## Slide 5: Data Preprocessing Steps
- Handled missing values
- Removed unnecessary columns
- Clipped outliers using IQR-based limits
- Converted date columns into usable features
- Selected relevant features for analysis
- Created engineered fields:
  - `default_flag`
  - `default_stage`

## Slide 6: Preprocessing Output
- Raw data converted into cleaned processed dataset
- New derived fields:
  - `issue_year`
  - `issue_month`
  - `credit_history_years`
  - `default_flag`
  - `default_stage`
- Final dataset stored as:
  - `processed_lending_club_loan.csv`

## Slide 7: Unit III Theoretical Concepts
### Association Rule Mining
- Used to discover relationships among features
- Helps find borrower patterns linked to safer or riskier behavior

### Important Measures
- **Support:** frequency of occurrence of a rule
- **Confidence:** reliability of the rule
- **Lift:** strength of relationship compared to random chance

### Algorithm Used
- Apriori algorithm

## Slide 8: Unit III Application on Dataset
- Continuous values converted into buckets such as:
  - income = low / medium / high
  - loan amount = low / medium / high
  - DTI = low / medium / high
- Association rules generated from processed data

### Example Rule
- Grade A + high income + short term -> default = no

## Slide 9: Unit IV Theoretical Concepts
### Supervised Learning
- Learns from labeled data
- Used for prediction tasks
- Target variable in this project:
  - `default_flag`

### Unsupervised Learning
- Learns patterns from unlabeled data
- Used for grouping borrowers into clusters

## Slide 10: Supervised Learning Algorithms Used
- Logistic Regression
- Decision Tree
- Random Forest

### Purpose
- Predict whether a borrower is likely to default
- Support stage classification and risk estimation

## Slide 11: Supervised Learning Results
| Model | Accuracy | F1 Score |
| --- | --- | --- |
| Logistic Regression | 0.8056 | 0.0876 |
| Decision Tree | 0.8017 | 0.1476 |
| Random Forest | 0.8047 | 0.0358 |

### Best Model
- Decision Tree performed best based on F1 score

## Slide 12: Unsupervised Learning Algorithm Used
### K-Means Clustering
- Divides borrowers into groups based on similarity
- Used numeric features like:
  - loan amount
  - income
  - DTI
  - interest rate
  - credit history years

## Slide 13: Clustering Results
- Borrowers grouped into:
  - low risk
  - medium risk
  - high risk

### Cluster Summary
| Cluster | Records | Avg Default Flag |
| --- | --- | --- |
| low_risk | 41,823 | 0.1199 |
| medium_risk | 29,702 | 0.1893 |
| high_risk | 48,475 | 0.2673 |

## Slide 14: Data Visualization Techniques Used
### Tools
- Python
- Matplotlib
- Seaborn

### Charts Created
- Risk distribution graph
- Cluster scatter plot
- Association rule confidence chart
- Model comparison chart

## Slide 15: Visualization Output
### Visual Insights
- Risk distribution shows borrower default categories
- Cluster plot shows borrower grouping by income and DTI
- Association chart highlights strongest rules
- Model comparison chart shows classifier performance

## Slide 16: System Implementation
- Built a loan risk system module with:
  - default prediction
  - stage classification
  - interest recommendation
  - what-if simulation

### Example Output
- Default probability: 0.081
- Default stage: non_default
- Risk cluster: low_risk
- Recommended interest rate: 10.5

## Slide 17: Architecture Flow
```text
Dataset -> Preprocessing -> ETL / Database -> Association Mining ->
Classification + Clustering -> Visualization -> Prediction Module -> Output
```

## Slide 18: Conclusion
- The project successfully covered DET syllabus concepts
- Data was explored, cleaned, transformed, and analyzed
- Association mining explained Unit III concepts
- Classification and clustering covered Unit IV
- Visualization and system implementation made the project practical

## Slide 19: Future Scope
- Add live user input frontend
- Improve class imbalance handling
- Deploy the model as a web application
- Add more advanced dashboards and explainability

## Slide 20: Thank You
**Thank You**

Questions?
