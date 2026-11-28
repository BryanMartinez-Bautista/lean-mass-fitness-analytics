import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean.csv")

# Histogram of the target
plt.figure(figsize=(8, 5))
plt.hist(df["lean_mass_kg"], bins=40, color="steelblue", edgecolor="white")
plt.xlabel("Lean mass (kg)")
plt.ylabel("Number of people")
plt.title("Distribution of lean_mass_kg")
plt.tight_layout()
plt.savefig("figures/lean_mass_hist.png")
plt.close()

# Group-by summaries
freq = df.groupby("Workout_Frequency (days/week)")["lean_mass_kg"].agg(
    ["count", "mean", "std"]).round(2)
exp = df.groupby("Experience_Level")["lean_mass_kg"].agg(
    ["count", "mean", "std"]).round(2)
print("Lean mass by workout frequency:")
print(freq)
print("\nLean mass by experience level:")
print(exp)

# Bar charts of the group means
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
freq["mean"].plot(kind="bar", ax=axes[0], color="steelblue")
axes[0].set_xlabel("Workout days per week")
axes[0].set_ylabel("Mean lean mass (kg)")
axes[0].set_title("Lean mass by workout frequency")
exp["mean"].plot(kind="bar", ax=axes[1], color="darkorange")
axes[1].set_xlabel("Experience level")
axes[1].set_ylabel("Mean lean mass (kg)")
axes[1].set_title("Lean mass by experience level")
plt.tight_layout()
plt.savefig("figures/lean_mass_by_group.png")
plt.close()