import pandas as pd
from apyori import apriori

# Load dataset (make sure file is in same folder)
df = pd.read_csv('dataset/transaction_data.csv')

# Fix column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

# Check columns
print(df.columns)
print(df.head())

# Remove missing values
df = df.dropna()

# Group items by transaction
Transactions = df.groupby('TransactionId')['ItemDescription'].apply(list).tolist()

# Apply Apriori
rules = apriori(
    Transactions,
    min_support=0.01,
    min_confidence=0.1,
    min_lift=1,
    max_length=2
)

results = list(rules)

# Print Results
count = 0

for item in results:
    pair = list(item.items)

    if len(pair) > 1:
        print("Items:", pair)
        print("Support:", item.support)

        # SAFE rule extraction
        for stat in item.ordered_statistics:
            if len(stat.items_base) > 0 and len(stat.items_add) > 0:
                print("Rule:", list(stat.items_base), "->", list(stat.items_add))
                print("Confidence:", stat.confidence)
                print("Lift:", stat.lift)
                count += 1

        print("---------------------------------")

print("Total Rules Found:", count)