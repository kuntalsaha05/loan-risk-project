# Data Warehouse Design

## Overview
The project uses a simple star-schema style design to align with Unit II concepts.

## Fact Table
- `fact_loan_transactions`
  - loan amount
  - interest rate
  - installment
  - annual income
  - DTI
  - revol_bal
  - revol_util
  - default_flag
  - default_stage

## Dimension Tables
- `dim_user`
  - annual income
  - verification status
  - mort_acc
  - pub_rec_bankruptcies

- `dim_time`
  - issue date
  - issue year
  - issue month
  - earliest credit line
  - credit history years

- `dim_loan`
  - loan amount
  - term
  - grade
  - sub_grade
  - purpose

## Star Schema Mapping
- Fact table connects with user, time, and loan dimensions.
- This supports analytical querying for default trends and risk grouping.

## OLTP vs OLAP
- OLTP: application-side user input and transaction capture
- OLAP: reporting, analytics, dashboards, and model-driven insights
