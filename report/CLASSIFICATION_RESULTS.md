# Classification Results

| Model | Accuracy | F1 Score |
| --- | --- | --- |
| Logistic Regression | 0.8043 | 0.0888 |
| Decision Tree | 0.8019 | 0.1091 |
| Random Forest | 0.8041 | 0.0325 |

## Detailed Reports

### Logistic Regression
```text
              precision    recall  f1-score   support

           0       0.81      0.99      0.89     19281
           1       0.52      0.05      0.09      4719

    accuracy                           0.80     24000
   macro avg       0.67      0.52      0.49     24000
weighted avg       0.75      0.80      0.73     24000
```

### Decision Tree
```text
              precision    recall  f1-score   support

           0       0.81      0.98      0.89     19281
           1       0.47      0.06      0.11      4719

    accuracy                           0.80     24000
   macro avg       0.64      0.52      0.50     24000
weighted avg       0.74      0.80      0.74     24000
```

### Random Forest
```text
              precision    recall  f1-score   support

           0       0.81      1.00      0.89     19281
           1       0.56      0.02      0.03      4719

    accuracy                           0.80     24000
   macro avg       0.68      0.51      0.46     24000
weighted avg       0.76      0.80      0.72     24000
```