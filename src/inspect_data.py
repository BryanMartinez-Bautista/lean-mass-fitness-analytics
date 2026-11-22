import pandas as pd
import numpy as np

df = pd.read_csv("data/fitness.csv")

print("Shape:", df.shape)

print("\n--- Missing values ---")
missing = df.isna().sum()
print(missing[missing > 0] if missing.any() else "None")

print("\n--- Duplicate rows ---")
print(df.duplicated().sum())

print("\n--- Constant columns ---")
print([c for c in df.columns if df[c].nunique() <= 1])

num = df.select_dtypes(include=np.number)

print("\n--- Columns with negative values ---")
neg = (num < 0).sum()
print(neg[neg > 0])

print("\n--- Categorical columns (unique counts) ---")
print(df.select_dtypes(exclude=np.number).nunique())

print("\n--- Numeric summary ---")
print(num.describe().T.to_string())