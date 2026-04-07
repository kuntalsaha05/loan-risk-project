# K-Means Clustering Results

## Method
- Used K-Means clustering with 3 clusters
- Clustered borrowers into low, medium, and high risk groups
- Used numeric loan and borrower risk features after preprocessing

## Cluster Summary

| Risk Cluster | Records | Avg Loan Amount | Avg Interest Rate | Avg Annual Income | Avg DTI | Default Rate |
| --- | --- | --- | --- | --- | --- | --- |
| high_risk | 48475 | 11546.91 | 15.84 | 53079.85 | 21.81 | 0.2673 |
| low_risk | 41823 | 10186.76 | 10.76 | 63135.66 | 13.10 | 0.1199 |
| medium_risk | 29702 | 23925.35 | 14.21 | 111146.75 | 16.02 | 0.1893 |

## Interpretation
- Default rate is computed after clustering and is used only for interpretation.
- Higher DTI and interest rates generally indicate stronger repayment risk.
- These clusters can support segmentation, dashboards, and model explanations.