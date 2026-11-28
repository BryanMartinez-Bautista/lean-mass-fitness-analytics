import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

df = pd.read_csv("data/clean.csv")

# Check 1: session duration, meals, and workout frequency
cols = ["Session_Duration (hours)", "Daily meals frequency", "Workout_Frequency (days/week)"]
X_train, X_test, y_train, y_test = train_test_split(
    df[cols], df["lean_mass_kg"], test_size=0.2, random_state=42)
rf = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1).fit(X_train, y_train)
print("Session, meals, workout frequency, Random Forest R2:", round(r2_score(y_test, rf.predict(X_test)), 4))

# Check 2: macros only
cols = ["Proteins", "Carbs", "Fats"]
X_train, X_test, y_train, y_test = train_test_split(
    df[cols], df["lean_mass_kg"], test_size=0.2, random_state=42)
rf = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1).fit(X_train, y_train)
print("Macros only, Random Forest R2:", round(r2_score(y_test, rf.predict(X_test)), 4))