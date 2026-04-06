# Association Rule Mining

## Method
- Used Apriori-based frequent itemset mining
- Converted continuous fields into categorical buckets
- Generated rules using support, confidence, and lift

## Top Rules

| Antecedent | Consequent | Support | Confidence | Lift |
| --- | --- | --- | --- | --- |
| grade_bucket_grade=A, income_bucket_income=high | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.0626 | 0.9274 | 3.2591 |
| dti_bucket_dti=low, grade_bucket_grade=A | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.0670 | 0.9269 | 3.2574 |
| grade_bucket_grade=A, loan_bucket_loan=low | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.0524 | 0.9241 | 3.2475 |
| credit_history_bucket_credit_history=medium, grade_bucket_grade=A | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.0510 | 0.9216 | 3.2389 |
| grade_bucket_grade=D, term_bucket_term=short | default_bucket_default=no, interest_bucket_interest=high | 0.0746 | 0.7176 | 3.2342 |
| grade_bucket_grade=A, purpose_bucket_purpose=debt_consolidation | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.0747 | 0.9180 | 3.2262 |
| grade_bucket_grade=A, loan_bucket_loan=medium | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.0524 | 0.9176 | 3.2245 |
| grade_bucket_grade=A, income_bucket_income=medium | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.0511 | 0.9175 | 3.2243 |
| grade_bucket_grade=A | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.1486 | 0.9166 | 3.2212 |
| dti_bucket_dti=medium, grade_bucket_grade=A | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.0506 | 0.9157 | 3.2180 |
| credit_history_bucket_credit_history=high, grade_bucket_grade=A | default_bucket_default=no, interest_bucket_interest=low, term_bucket_term=short | 0.0582 | 0.9100 | 3.1978 |
| grade_bucket_grade=A, income_bucket_income=high, term_bucket_term=short | default_bucket_default=no, interest_bucket_interest=low | 0.0626 | 0.9532 | 3.1285 |
| grade_bucket_grade=A, income_bucket_income=high | default_bucket_default=no, interest_bucket_interest=low | 0.0643 | 0.9523 | 3.1253 |
| dti_bucket_dti=low, grade_bucket_grade=A, term_bucket_term=short | default_bucket_default=no, interest_bucket_interest=low | 0.0670 | 0.9511 | 3.1215 |
| dti_bucket_dti=low, grade_bucket_grade=A | default_bucket_default=no, interest_bucket_interest=low | 0.0687 | 0.9508 | 3.1203 |
| grade_bucket_grade=D | default_bucket_default=no, interest_bucket_interest=high | 0.1107 | 0.6904 | 3.1115 |
| credit_history_bucket_credit_history=medium, grade_bucket_grade=A, term_bucket_term=short | default_bucket_default=no, interest_bucket_interest=low | 0.0510 | 0.9421 | 3.0918 |
| credit_history_bucket_credit_history=medium, grade_bucket_grade=A | default_bucket_default=no, interest_bucket_interest=low | 0.0521 | 0.9418 | 3.0910 |
| grade_bucket_grade=A, loan_bucket_loan=medium, term_bucket_term=short | default_bucket_default=no, interest_bucket_interest=low | 0.0524 | 0.9402 | 3.0856 |
| grade_bucket_grade=A, loan_bucket_loan=medium | default_bucket_default=no, interest_bucket_interest=low | 0.0536 | 0.9393 | 3.0828 |

## Interpretation
- Higher lift indicates a stronger relationship than random chance.
- Rules ending in `default=yes` help identify risky borrower profiles.
- Rules ending in `default=no` help identify safer borrower profiles.