import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

df = pd.read_csv("data/clean.csv")

habits = ["Workout_Frequency (days/week)", "Session_Duration (hours)",
          "Experience_Level", "Calories_Burned", "Daily meals frequency",
          "Proteins", "Carbs", "Fats"]


def fit_r2(cols):
    X_train, X_test, y_train, y_test = train_test_split(
        df[cols], df["lean_mass_kg"], test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    return rf, r2_score(y_test, rf.predict(X_test))


# 1. Which columns does the forest rely on?
rf, r2 = fit_r2(habits)
print("All habit columns: R2 =", round(r2, 4))
for name, imp in sorted(zip(habits, rf.feature_importances_), key=lambda x: -x[1]):
    print(" ", name, round(imp, 3))

# 2. What happens if each column is removed?
print("\nR2 with one column removed:")
for col in habits:
    _, r2 = fit_r2([c for c in habits if c != col])
    print(" without", col, ":", round(r2, 4))

# 3. Does calories per hour of exercise track body weight?
rate = df["Calories_Burned"] / df["Session_Duration (hours)"]
print("\nCalories_Burned / Session_Duration vs Weight:",
      round(rate.corr(df["Weight (kg)"]), 3))