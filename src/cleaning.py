import pandas as pd


def clean_data(df):
    df = df.copy()

    # Decision 1 (AI log: "Constant column"): drop columns with one value
    df = df.drop(columns=["meal_name"])

    # Decision 2 (AI log: "Negative values"): clip tiny negatives to 0
    for col in ["Physical exercise", "sugar_g", "cholesterol_mg"]:
        df[col] = df[col].clip(lower=0)

    # Decision 3 (AI log: "Noisy whole-number columns"): round to integers
    df["Workout_Frequency (days/week)"] = (
        df["Workout_Frequency (days/week)"].round().astype(int)
    )
    df["Experience_Level"] = df["Experience_Level"].round().astype(int)

    return df


if __name__ == "__main__":
    raw = pd.read_csv("data/fitness.csv")
    clean = clean_data(raw)

    print("Shape before:", raw.shape)
    print("Shape after: ", clean.shape)
    print("\nNegatives left in clipped columns:")
    print((clean[["Physical exercise", "sugar_g", "cholesterol_mg"]] < 0).sum())
    print("\nWorkout_Frequency values:")
    print(clean["Workout_Frequency (days/week)"].value_counts().sort_index())
    print("\nExperience_Level values:")
    print(clean["Experience_Level"].value_counts().sort_index())

    clean.to_csv("data/clean.csv", index=False)
    print("\nSaved data/clean.csv")