# Classification Results

## Models Used
- Logistic Regression
- Decision Tree
- Random Forest

## Evaluation Summary

| Model | Accuracy | F1 Score |
| --- | --- | --- |
| Logistic Regression | 0.8056 | 0.0876 |
| Decision Tree | 0.8017 | 0.1476 |
| Random Forest | 0.8047 | 0.0358 |

## Best Model
- Based on F1 score, the best model is `Decision Tree`.

## Detailed Reports

### Logistic Regression
```text
              precision    recall  f1-score   support

           0       0.81      0.99      0.89     19293
           1       0.55      0.05      0.09      4707

    accuracy                           0.81     24000
   macro avg       0.68      0.52      0.49     24000
weighted avg       0.76      0.81      0.73     24000
```

### Decision Tree
```text
              precision    recall  f1-score   support

           0       0.81      0.98      0.89     19293
           1       0.47      0.09      0.15      4707

    accuracy                           0.80     24000
   macro avg       0.64      0.53      0.52     24000
weighted avg       0.75      0.80      0.74     24000
```

### Random Forest
```text
              precision    recall  f1-score   support

           0       0.81      1.00      0.89     19293
           1       0.57      0.02      0.04      4707

    accuracy                           0.80     24000
   macro avg       0.69      0.51      0.46     24000
weighted avg       0.76      0.80      0.72     24000
```