import pandas as pd

data={
    "PRN":[101,102,103,104,105],
    "Name": ["Sid", "Maddy", "Manan", "Kuntal", "Saksham"],
    "Marks":[95, 85, 92, 73, 89],
    "Age":[20,21,19,18, 20],
    "Gender":["M","M","M","F","M"]
}
df=pd.DataFrame(data)
print(df)

