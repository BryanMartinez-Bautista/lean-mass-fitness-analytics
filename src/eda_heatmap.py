import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean.csv")

# Keep only the numeric columns and compute correlations
corr = df.select_dtypes(include="number").corr()

# Heatmap of all numeric columns
plt.figure(figsize=(20, 16))
sns.heatmap(corr, cmap="coolwarm", center=0)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("figures/corr_heatmap.png")

# Top 15 columns most correlated with lean_mass_kg
top = corr["lean_mass_kg"].drop("lean_mass_kg")
top = top.abs().sort_values(ascending=False).head(15)
print(top.round(3))