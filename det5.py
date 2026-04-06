import itertools
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from apyori import apriori
import numpy as np


Transactions = [
    ['Bread', 'Milk', 'Diaper', 'Eggs', 'Cola'],
    ['Milk', 'Beer', 'Cola'],
    ['Bread', 'Milk', 'Diaper', 'Beer'],
    ['Curd', 'Milk', 'Eggs'],
    ['Butter', 'Milk', 'Flour', 'Eggs'],
    ['Ice Cream', 'Milk'],
    ['Bread', 'Butter', 'Milk', 'Cola']
]

# Apply Apriori (PREDEFINED FUNCTION)
rules = apriori(
    Transactions,
    min_support=0.15,
    min_confidence=0.2,
    min_lift=1,
    max_length=2
)

results = list(rules)

# Print Results
for item in results:
    pair = item.items
    items = [x for x in pair]

    if len(items) > 1:
        print("Rule:", items[0], "->", items[1])
        print("Support:", item.support)
        print("Confidence:", item.ordered_statistics[0].confidence)
        print("Lift:", item.ordered_statistics[0].lift)
        print("---------------------------------")

