import pandas as pd
from scipy import stats

df = pd.read_csv("data/clean.csv")

# Split lean mass into groups by workout frequency and by experience level
freq_groups = [g["lean_mass_kg"] for _, g in df.groupby("Workout_Frequency (days/week)")]
exp_groups = [g["lean_mass_kg"] for _, g in df.groupby("Experience_Level")]

# Test 1: ANOVA, lean mass by workout frequency
f, p = stats.f_oneway(*freq_groups)
print("ANOVA by workout frequency: F =", round(f, 3), ", p =", p)

# Test 2: ANOVA, lean mass by experience level
f, p = stats.f_oneway(*exp_groups)
print("ANOVA by experience level: F =", round(f, 3), ", p =", p)

# Test 3: Pearson correlation with lean mass
for col in ["Workout_Frequency (days/week)", "Proteins", "Carbs", "Fats"]:
    r, p = stats.pearsonr(df[col], df["lean_mass_kg"])
    print(col, ": r =", round(r, 4), ", p =", p, ", r squared =", round(r ** 2, 6))

# Test 4: Levene's test, is the spread equal across workout frequency groups?
w, p = stats.levene(*freq_groups)
print("Levene's test: W =", round(w, 3), ", p =", p)