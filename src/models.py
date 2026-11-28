import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

df = pd.read_csv("data/clean.csv")
target = "lean_mass_kg"

# Excluded on purpose (see AI log): Weight (kg), Fat_Percentage, BMI, BMI_calc,
# protein_per_kg (leakage), Calories and cal_balance (stand-ins for weight)

habits = ["Workout_Frequency (days/week)", "Session_Duration (hours)",
          "Experience_Level", "Calories_Burned", "Daily meals frequency",
          "Proteins", "Carbs", "Fats"]

feature_sets = {
    "A: habits only": habits,
    "B: habits + Age, Height": habits + ["Age", "Height (m)"],
    "C: B + Water_Intake": habits + ["Age", "Height (m)", "Water_Intake (liters)"],
}

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
}

rows = []
for set_name, cols in feature_sets.items():
    X_train, X_test, y_train, y_test = train_test_split(
        df[cols], df[target], test_size=0.2, random_state=42)
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        cv = cross_val_score(model, df[cols], df[target], cv=5, scoring="r2")
        rows.append({
            "features": set_name,
            "model": model_name,
            "R2": round(r2_score(y_test, pred), 4),
            "RMSE": round(np.sqrt(mean_squared_error(y_test, pred)), 3),
            "MAE": round(mean_absolute_error(y_test, pred), 3),
            "CV R2 (5-fold)": round(cv.mean(), 4),
        })

results = pd.DataFrame(rows)
print(results.to_string(index=False))
results.to_csv("report/model_results.csv", index=False)