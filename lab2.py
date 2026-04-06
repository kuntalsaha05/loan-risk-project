import pandas as pd
import numpy as np

data = {
    'Range': ['Mathematics', 'English Literature', 'Science', 'History', 'Computer Science', 'Geography', 'Physical Education','Art & Design', 'Foreign Language'], 
    '1st Semester': [85, 78, 80, 75, 90, 72, 88, 82, 74],
    '2nd Semester': [88, 82, 84, 78, 92, 76, 90, 85, 77],
    '3rd Semester': [90, 80, 88, 80, 94, 78, 91, 87, 79],
    '4th Semester': [92, 85, 86, 82, 95, 80, 93, 89, 81],
    'Average Grade': [88.75, 81.25, 84.5, 78.75, 92.75, 76.5, 90.5, 85.75, 77.75],
    'Grade': ['B', 'B', 'B', 'C', 'A', 'C', 'A', 'B', 'C']
} 

df = pd.DataFrame(data)
print(df)


df.loc[1,'2nd Semester'] = pd.NA
print(df) 
df.loc[4,'2nd Semester'] = pd.NA
print(df) 
df.loc[4,'Average Grade'] = pd.NA
print(df) 
df.loc[7,'Grade'] = pd.NA
print(df) 

# DataFrame.dropna():
df.dropna(axis=0, thresh=2) 
print(df)

# DataFrame.fillna():
df.fillna(0)  
print(df)

df.drop_duplicates()  
print(df)

# DataFrame.replace():
df.replace({'C': 'C+'}) 
print(df)

df['Range'] = df['Range'].str.strip() 
print(df)
df['Range'] = df['Range'].str.lower() 
print(df)

# DataFrame.astype():
df['1st Semester'] = df['1st Semester'].astype(float)
print(df)

# DataFrame.rename():
df.rename(columns={'Range': 'Subject'}) 
print(df)

# DataFrame.sort_values():
df.sort_values(by='Average Grade', ascending=False) 
print(df)

# DataFrame.isnull():
df[df['Grade'].isnull()]  
print(df)

# DataFrame.apply():
df['Average Grade'] = df['Average Grade'].apply(lambda x: x * 1.05)  
print(df)

data2 = {
    'Range': ['Economics', 'Psychology', 'Music', 'Drama'],
    '1st Semester': [83, 91, 79, 86],
    '2nd Semester': [85, 89, 82, 88],
    '3rd Semester': [87, 92, 84, 89],
    '4th Semester': [89, 94, 86, 91],
    'Average Grade': [86.0, 91.5, 82.75, 88.5],
    'Grade': ['B', 'A', 'B', 'B']
}

df2 = pd.DataFrame(data2)
print(df2)

df_merged = pd.concat([df, df2])
print("Merged DataFrame (df + df2):")
print(df_merged)