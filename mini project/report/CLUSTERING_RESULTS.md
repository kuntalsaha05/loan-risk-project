# K-Means Clustering Results

## Method
- Used K-Means clustering with 3 clusters
- Clustered borrowers into low, medium, and high risk groups
- Used numeric loan and borrower risk features after preprocessing

## Cluster Summary

| Risk Cluster | Records | Avg Loan Amount | Avg Interest Rate | Avg Annual Income | Avg DTI | Avg Default Flag |
| --- | --- | --- | --- | --- | --- | --- |
| high_risk | 22437 | 14432.42 | 15.93 | 61294.57 | 19.83 | 0.9997 |
| low_risk | 64794 | 9984.59 | 13.05 | 55094.09 | 17.46 | 0.0000 |
| medium_risk | 32769 | 22144.29 | 13.34 | 108938.83 | 15.40 | 0.0354 |

## Interpretation
- Higher average default flag suggests a riskier borrower cluster.
- Higher DTI and interest rates generally indicate stronger repayment risk.
- These clusters can support segmentation, dashboards, and model explanations.