import pandas as pd

df = pd.read_csv("data/clean.csv")

est = df["Weight (kg)"] * (1 - df["Fat_Percentage"] / 100)
print("Correlation with Weight x (1 - fat%):", round(df["lean_mass_kg"].corr(est), 4))
print("Mean absolute difference (kg):", round((df["lean_mass_kg"] - est).abs().mean(), 3))

cols = ["Weight (kg)", "Fat_Percentage", "BMI", "BMI_calc", "protein_per_kg"]
print("\nCorrelation with lean_mass_kg:")
print(df[cols + ["lean_mass_kg"]].corr()["lean_mass_kg"].drop("lean_mass_kg").round(3))