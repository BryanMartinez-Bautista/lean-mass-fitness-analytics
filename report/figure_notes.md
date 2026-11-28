## Figure 1: Correlation heatmap (corr_heatmap.png)
Caption: Pairwise correlations between all numeric columns in the cleaned data.

Lean mass is almost perfectly related to body weight (r = 0.982) and is also
strongly related to Calories (0.963), BMI (0.769), protein_per_kg (0.722),
cal_balance (0.708), and Fat_Percentage (0.659). We found that lean_mass_kg
equals Weight x (1 - Fat_Percentage/100) exactly, and that Calories correlates
0.978 with Weight, so these columns describe body size rather than habits and
are excluded from the models. Among the remaining columns, only Height (0.477)
and Water_Intake (0.435) show a moderate relationship with lean mass. The
workout and nutrition columns are close to zero (Workout_Frequency 0.025,
Proteins, Carbs, and Fats about -0.002), so they carry little linear signal.

## Figure 2: Boxplots of key variables (boxplots.png)
Caption: Boxplots for lean mass, demographics, workout, and macronutrient columns.

Using the IQR rule, Age, Height, Water_Intake, and Session_Duration have no
outliers. Calories_Burned (2.5%) and Proteins, Carbs, and Fats (about 2% each)
have a small share of high values, and lean_mass_kg has 17 outliers (0.1%).
The values stay within plausible ranges, so they look like the tails of the
distributions and not errors. I kept them, because removing them would discard
real data and Random Forest is not sensitive to them.

## Figure 3: Distribution of lean mass (lean_mass_hist.png)
Caption: Histogram of lean_mass_kg for all 20,000 people.

Lean mass ranges from about 31 to 90 kg with a mean of 53.8 kg. The mean is
above the median (51.2 kg), so the distribution has a right skewed tail. 
Most people fall between about 45 and 62 kg.

## Figure 4: Lean mass by workout frequency and experience level (lean_mass_by_group.png)
Caption: Mean lean mass for each workout-frequency group and each experience level.

Mean lean mass differs by less than 2 kg across workout-frequency groups
(53.1 to 54.9 kg) and experience levels (53.0 to 54.6 kg), so these habits
show little relationship with lean mass in this dataset. The spread within
groups narrows as frequency and experience rise (standard deviation falls from
13.9 kg at 2 days to 9.0 kg at 5 days), meaning heavier training groups are
more similar to each other, even though their averages are close.