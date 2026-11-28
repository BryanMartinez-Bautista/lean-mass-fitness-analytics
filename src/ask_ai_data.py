import json
import os
import time
from ai_assistant import ask_ai

context = """
Dataset: 20,000 rows, 54 columns about workouts, nutrition, and body
composition. Target to predict: lean_mass_kg (continuous, 31 to 90 kg).
No missing values and no duplicate rows were found.
"""

questions = [
    ("Constant column",
     "I'm predicting lean_mass_kg. The column meal_name has only 1 unique value "
     "across all 20,000 rows. Should I drop it or keep it? Please explain "
     "the tradeoffs."),

    ("Negative values",
     "I'm predicting lean_mass_kg. Physical exercise has 6,023 negative values "
     "(min -0.07), sugar_g has 67 (min -0.67), and cholesterol_mg has 110 "
     "(min -3.89). These can't be real measurements. Should I drop the rows, "
     "clip the values to 0, or something else? Please explain the tradeoffs."),

    ("Noisy whole-number columns",
     "I'm predicting lean_mass_kg. Workout_Frequency (days/week) ranges from "
     "1.94 to 5.06 with quartiles 2.98, 3.01, 4.00, and Experience_Level ranges "
     "from 1.00 to 3.05 with quartiles 1.01, 1.99, 2.02. They look like whole "
     "numbers with noise added. Should I round them to whole numbers, leave "
     "them as continuous, or something else? Please explain the tradeoffs."),

    ("Uninformative columns",
     "I'm predicting lean_mass_kg. Two columns may carry no useful "
     "information. 'Burns Calories (per 30 min)_bc' has values around 1e19 to "
     "1e20, while the original 'Burns Calories (per 30 min)' column ranges "
     "from about 129 to 382. pct_carbs is about 0.50 for every row (std "
     "0.0015). For each column, should I drop it, fix it, or keep it? Please "
     "explain the tradeoffs"),

    ("Target leakage",
     "I'm predicting lean_mass_kg. In my dataset, the correlation with "
     "lean_mass_kg is ___ for Weight (kg), ___ for Fat_Percentage, ___ for "
     "BMI, and ___ for protein_per_kg (protein divided by weight). Which of "
     "these could leak the target, and should I exclude them from my models "
     "if my goal is to understand how workout and nutrition habits relate "
     "to lean mass? Please explain the tradeoffs"),

    ("Weight-relationship and weak habit signals",
     "I'm predicting lean_mass_kg, and I already excluded Weight, "
     "Fat_Percentage, BMI, and protein_per_kg because lean mass equals "
     "Weight x (1 - Fat_Percentage/100). My data also shows Calories has "
     "correlation 0.978 with Weight and 0.963 with lean_mass_kg, cal_balance "
     "has 0.737 with Weight, and Water_Intake has 0.398 with Weight and 0.435 "
     "with lean_mass_kg. My workout and nutrition variables have almost no "
     "correlation with lean_mass_kg: Workout_Frequency 0.025, Proteins "
     "-0.002, Carbs -0.002, Fats -0.002. Should I exclude Calories, "
     "cal_balance, and Water_Intake as stand-ins for body size? And how "
     "should I frame my research question and expectations if habit "
     "variables show almost no linear relationship? Please explain the "
     "tradeoffs."),

    ("Outliers",
     "I'm predicting lean_mass_kg with Linear Regression as a baseline and "
     "Random Forest as an advanced model. Using the IQR rule on 20,000 rows, "
     "I found: lean_mass_kg 17 outliers (0.1%), Calories_Burned 507 (2.5%), "
     "Proteins 403 (2.0%), Carbs 405 (2.0%), and Fats 399 (2.0%). Age, "
     "Height, Water_Intake, and Session_Duration have none. The values are "
     "within plausible ranges (for example lean mass 31 to 90 kg). Should I "
     "keep them, cap them at the IQR bounds, or remove the rows? Please "
     "explain the tradeoffs for each model."),

    ("Choosing hypothesis tests",
     "I'm predicting lean_mass_kg (about 31 to 90 kg, 20,000 rows). Mean lean "
     "mass by Workout_Frequency (2, 3, 4, 5 days/week) is 54.00, 53.12, "
     "54.09, 54.88 kg with standard deviations 13.93, 13.16, 11.63, 8.95. By "
     "Experience_Level (1, 2, 3) it is 53.04, 54.10, 54.60 with standard "
     "deviations 13.40, 13.10, 8.66. The Pearson correlation of "
     "Workout_Frequency with lean_mass_kg is 0.025, and Proteins, Carbs, and "
     "Fats are about -0.002. Which formal hypothesis tests are appropriate "
     "here (for example t-test, ANOVA, Chi-square test, correlation analysis),"
     " what null hypothesis should each state, and how should I "
     "interpret a statistically significant but tiny effect with a large "
     "sample? Please keep it concise."),

    ("Choosing models and features",
     "I'm predicting lean_mass_kg (31 to 90 kg, 20,000 rows) with Linear "
     "Regression as a baseline and Random Forest as an advanced model. I "
     "excluded Weight, Fat_Percentage, BMI, BMI_calc, protein_per_kg (leakage), "
     "and Calories and cal_balance (they correlate 0.978 and 0.737 with "
     "Weight). My habit variables have almost no correlation with lean mass "
     "(Workout_Frequency 0.025, Proteins, Carbs, Fats about -0.002), while "
     "Height (0.477) and Water_Intake (0.435) are moderate. Which feature sets "
     "should I compare, how should I evaluate the models (train/test split, "
     "cross-validation, metrics), and what R2 should I expect? Please keep "
     "it concise."),
]

LOG_PATH = "report/ai_log.json"


def already_done():
    """Steps that are already saved in the log, so we don't repeat them."""
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return {entry["step"] for entry in json.load(f)}
    return set()


def ask_with_retry(question, step, tries=1, wait=30):
    """Try again if Gemini is temporarily overloaded (503)."""
    for attempt in range(1, tries + 1):
        try:
            return ask_ai(question, context, step=step)
        except Exception as e:
            print(f"Attempt {attempt} failed: {str(e)[:100]}")
            if attempt == tries:
                raise
            time.sleep(wait)


done = already_done()

for step, question in questions:
    if step in done:
        print(f"\n=== {step} === (already logged, skipping)")
        continue
    print(f"\n=== {step} ===")
    print(ask_with_retry(question, step))
    time.sleep(15)   # stays under 5 requests per minute