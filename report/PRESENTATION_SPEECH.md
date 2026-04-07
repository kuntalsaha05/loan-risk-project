# Presentation Speech

## Slide 1: Title Slide
Good morning everyone. My project title is **Loan Risk Analysis and Prediction System**.  
This is a DET mini project based on data exploration, preprocessing, association rule mining, supervised learning, unsupervised learning, visualization, and system implementation.

The main purpose of this project is to analyze a loan dataset and identify whether a borrower may become risky or safe from a loan repayment point of view.

## Slide 2: Project Objective
The objective of this project is to understand and analyze a real loan dataset.  
In this project, I explored the dataset, cleaned the data, created useful features, applied machine learning algorithms, and generated visualizations.

The project also includes association rule mining to find useful patterns and K-Means clustering to divide borrowers into different risk groups.

## Slide 3: Dataset Overview
The dataset used in this project is `lending_club_loan_two.csv`.  
It is a structured CSV dataset and contains loan-related information such as loan amount, interest rate, annual income, DTI, grade, purpose, and loan status.

After preprocessing, the dataset contains 396,030 rows and 24 selected columns.  
The dataset includes quantitative data, nominal data, and time-related data.

## Slide 4: Dataset Exploration and Analysis
First, I explored the dataset by checking its shape, column names, data types, missing values, and sample records.  
I identified important numerical fields like loan amount, income, interest rate, and DTI.

I also identified categorical fields like grade, sub-grade, purpose, verification status, and loan status.  
The loan status column was important because it helped create the target variable for default prediction.

## Slide 5: Data Preprocessing Steps
In preprocessing, I handled missing values, removed unnecessary columns, converted date columns, and selected useful features.

I also created two important engineered features: `default_flag` and `default_stage`.  
The `default_flag` tells whether the borrower defaulted or not, and `default_stage` classifies the loan status into categories like non-default, active, delinquent, or default.

Outliers in columns like loan amount, annual income, and DTI were handled using the IQR method.

## Slide 6: Preprocessing Output
After preprocessing, the final processed dataset was saved as `processed_lending_club_loan.csv`.  
The processed dataset includes useful features such as loan amount, term, interest rate, annual income, DTI, issue year, issue month, credit history years, default flag, and default stage.

This preprocessing step satisfies the Unit I part of the syllabus because it includes data cleaning, transformation, feature engineering, and data reduction.

## Slide 7: Unit III Theoretical Concepts
For Unit III, I used association rule mining.  
Association rule mining is used to find relationships and patterns between different variables in the dataset.

The three important measures are support, confidence, and lift.  
Support tells how frequently a pattern occurs. Confidence tells how reliable the rule is. Lift tells whether the relationship is stronger than random chance.

The algorithm used for this part is the Apriori algorithm.

## Slide 8: Unit III Application on Dataset
In this project, I converted continuous values into categories such as low, medium, and high.  
For example, income, loan amount, DTI, and interest rate were bucketed into categories.

Then I applied Apriori to generate association rules.  
One example pattern found was that Grade A borrowers with high income and short loan term are strongly associated with `default=no`.

This shows how association rule mining can help identify safer borrower profiles.

## Slide 9: Unit IV Theoretical Concepts
For Unit IV, I used both supervised and unsupervised learning.

Supervised learning is used when we have a target variable. In this project, the target variable is `default_flag`, which tells whether a borrower defaulted or not.

Unsupervised learning is used when we want to find hidden groups in the data without using a target label. For this, I used K-Means clustering.

## Slide 10: Supervised Learning Algorithms Used
I applied three supervised learning algorithms: Logistic Regression, Decision Tree, and Random Forest.

These models were trained to predict loan default.  
The input features included loan amount, term, interest rate, installment, grade, sub-grade, annual income, verification status, purpose, DTI, and credit history years.

The target variable was `default_flag`.

## Slide 11: Supervised Learning Results
The results show that all models had around 80 percent accuracy.  
However, accuracy alone is not enough because the dataset is imbalanced.

Decision Tree had the best F1 score among the three models, so I selected it as the best model for the prediction system.  
The Decision Tree model is also useful because it is easier to interpret compared to some complex models.

## Slide 12: Unsupervised Learning Algorithm Used
For unsupervised learning, I used K-Means clustering.  
K-Means groups similar borrowers together based on features like loan amount, interest rate, annual income, DTI, revolving utilization, and credit history years.

One important correction in this project is that `default_flag` was not used as an input for clustering.  
It was only used later to interpret the default rate of each cluster. This avoids data leakage.

## Slide 13: Clustering Results
The borrowers were divided into three risk groups: low risk, medium risk, and high risk.

The low-risk cluster had the lowest default rate, the medium-risk cluster had a moderate default rate, and the high-risk cluster had the highest default rate.

The corrected cluster results are:
low risk with around 11.99 percent default rate, medium risk with around 18.93 percent, and high risk with around 26.73 percent.

This makes the clustering result more realistic.

## Slide 14: Data Visualization Techniques Used
For visualization, I used Python libraries Matplotlib and Seaborn.

The charts created include risk distribution, cluster scatter plot, association rule confidence chart, and model comparison chart.

These visualizations make it easier to understand the dataset, compare model performance, and explain the final risk groups.

## Slide 15: Visualization Output
The risk distribution chart shows the distribution of loan stages.  
The cluster graph shows borrower segmentation based on income and DTI.

The association rule chart shows the strongest rules based on confidence.  
The model comparison chart shows how Logistic Regression, Decision Tree, and Random Forest performed.

## Slide 16: System Implementation
After analysis and modeling, I implemented a simple loan risk system.

The system gives default probability, default stage, risk cluster, recommended interest rate, and what-if simulation results.

For a sample borrower, the system predicted a default probability of 0.081, default stage as non-default, risk cluster as low risk, and recommended interest rate as 10.5.

## Slide 17: Architecture Flow
The architecture of the project follows this flow:
Dataset, preprocessing, ETL and database, association mining, classification, clustering, visualization, prediction module, and final output.

This architecture clearly connects the syllabus concepts into one complete project workflow.

## Slide 18: Conclusion
To conclude, this project successfully covers the main DET syllabus topics.

Unit I is covered through data exploration and preprocessing.  
Unit II is covered through ETL and data warehouse design.  
Unit III is covered through association rule mining.  
Unit IV is covered through classification and K-Means clustering.

The project also includes visualizations, a frontend dashboard, a final report, and a PowerPoint presentation.

## Slide 19: Future Scope
In the future, this project can be improved by adding a live backend API, improving class imbalance handling, using more advanced models, and deploying the frontend dashboard as a complete web application.

We can also add explainability techniques to show why a borrower is classified as low, medium, or high risk.

## Slide 20: Thank You
Thank you.  
This was my presentation on the Loan Risk Analysis and Prediction System.

I am ready to answer any questions.
