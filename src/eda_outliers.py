import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean.csv")

cols = ["lean_mass_kg", "Age", "Height (m)", "Water_Intake (liters)",
        "Session_Duration (hours)", "Calories_Burned",
        "Proteins", "Carbs", "Fats"]

print("IQR outlier counts:")
for col in cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    n = ((df[col] < low) | (df[col] > high)).sum()
    print(f"{col}: {n} outliers ({n / len(df):.1%})")

df[cols].plot(kind="box", subplots=True, layout=(3, 3),
              sharey=False, figsize=(15, 10))
plt.tight_layout()
plt.savefig("figures/boxplots.png")