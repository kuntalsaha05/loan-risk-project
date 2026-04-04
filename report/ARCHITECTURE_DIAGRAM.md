# Architecture Diagram

## System Flow

```text
Raw Dataset (CSV)
        |
        v
Data Understanding
        |
        v
Data Preprocessing
- cleaning
- transformation
- feature engineering
- reduction
        |
        v
Processed Dataset
        |
        v
ETL Pipeline
- extract
- transform
- load
        |
        v
SQLite Database / Data Warehouse Layer
        |
        +------------------------------+
        |                              |
        v                              v
Association Rule Mining         Machine Learning
(Apriori)                       - Classification
                                - K-Means Clustering
        |                              |
        +---------------+--------------+
                        |
                        v
Visualization Layer
- risk distribution
- rule chart
- cluster graph
- model comparison
                        |
                        v
System Implementation Layer
- default prediction
- stage classification
- interest recommendation
- what-if simulation
                        |
                        v
Frontend / Output Dashboard
```

## Module Mapping
- `data/lending_club_loan_two.csv`: raw dataset
- `backend/preprocess_data.py`: preprocessing
- `backend/load_to_database.py`: ETL and database loading
- `models/association_rule_mining.py`: association rules
- `models/train_classification_models.py`: supervised learning
- `models/kmeans_clustering.py`: unsupervised learning
- `models/generate_visualizations.py`: charts and graphs
- `backend/loan_risk_system.py`: integrated prediction system

## Syllabus Mapping
- Unit I: data types and preprocessing
- Unit II: ETL and data warehouse
- Unit III: association rule mining
- Unit IV: classification and clustering
