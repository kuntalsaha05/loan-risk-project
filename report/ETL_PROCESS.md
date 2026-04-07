# ETL Process

## Extract
- Loaded `processed_lending_club_loan.csv` from the data folder.
- Records extracted: 396030

## Transform
- Converted date fields into YYYY-MM-DD format.
- Kept the cleaned columns from preprocessing.

## Load
- Loaded the data into SQLite database `loan_risk.db`.
- Table name: `loan_records`.