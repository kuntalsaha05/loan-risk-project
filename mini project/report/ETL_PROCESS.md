# ETL Process

## Extract
- Source file: `data/processed_lending_club_loan.csv`
- Records extracted: 396030

## Transform
- Parsed and standardized date fields for database storage
- Preserved engineered fields such as `default_flag` and `default_stage`
- Kept cleaned and selected features from preprocessing

## Load
- Target database: `data/loan_risk.db`
- Target table: `loan_records`
- Columns loaded: 24

## ETL Summary
- Extract: processed CSV loaded from the data folder
- Transform: final formatting and date normalization for storage
- Load: records inserted into SQLite for analytics and later dashboard use