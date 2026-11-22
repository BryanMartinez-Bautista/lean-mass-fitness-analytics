from datasets import load_dataset

ds = load_dataset("Idankhen/SmartFitnessNutritionAnalyticsDataset", split="train")
df = ds.to_pandas()
df.to_csv("data/fitness.csv", index=False)

print(df.shape)
print(df.columns.tolist())
print(df.head())