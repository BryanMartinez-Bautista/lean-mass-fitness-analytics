import pandas as pd

df = pd.read_csv("data/clean.csv")

print("Correlation with Weight (kg):")
print(df[["Calories", "cal_balance", "Water_Intake (liters)", "Height (m)"]]
      .corrwith(df["Weight (kg)"]).round(3))

print("\nCorrelation with lean_mass_kg (your original predictors):")
print(df[["Workout_Frequency (days/week)", "Proteins", "Carbs", "Fats",
          "Calories", "Water_Intake (liters)"]]
      .corrwith(df["lean_mass_kg"]).round(3))