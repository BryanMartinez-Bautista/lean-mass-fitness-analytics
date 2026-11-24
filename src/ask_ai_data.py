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

    ("Broken engineered column",
     "I'm predicting lean_mass_kg. A column called "
     "'Burns Calories (per 30 min)_bc' has values around 1e19 to 1e20, while "
     "the original 'Burns Calories (per 30 min)' column ranges from about 129 "
     "to 382. Should I drop it, try to fix it, or keep it? Please explain "
     "the tradeoffs."),

    ("Near-constant column",
     "I'm predicting lean_mass_kg. The column pct_carbs is about 0.50 for "
     "every row (mean 0.49998, std 0.0015). Should I drop it, keep it, or "
     "something else? Please explain the tradeoffs."),

    ("Calorie balance negatives",
     "I'm predicting lean_mass_kg. cal_balance has 2,832 negative values "
     "(min -1266). I think this is a legitimate calorie deficit rather than "
     "an error. Should I keep these values as they are? Please explain "
     "the tradeoffs."),

    ("Target leakage",
     "I'm predicting lean_mass_kg. These columns look closely related to "
     "body composition: Weight (kg), Fat_Percentage, BMI, BMI_calc, and "
     "protein_per_kg (protein divided by weight). Which of them could leak "
     "the target, and should I exclude them from the models? Please explain "
     "the tradeoffs."),
]

LOG_PATH = "report/ai_log.json"


def already_done():
    """Steps that are already saved in the log, so we don't repeat them."""
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return {entry["step"] for entry in json.load(f)}
    return set()


def ask_with_retry(question, step, tries=3, wait=30):
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