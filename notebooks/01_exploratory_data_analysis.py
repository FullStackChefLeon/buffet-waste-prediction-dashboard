import os
import pandas as pd
import matplotlib.pyplot as plt

# Create output folder
os.makedirs("reports/figures", exist_ok=True)

# Load data
df = pd.read_csv("data/buffet_waste_sample.csv")

print("===== Dataset Overview =====")
print("Shape:", df.shape)

print("\n===== Columns =====")
print(df.columns.tolist())

print("\n===== First 5 Rows =====")
pd.set_option("display.max_columns", None)
print(df.head())

print("\n===== Missing Values =====")
print(df.isna().sum())

print("\n===== Waste Level Distribution =====")
waste_counts = df["waste_level"].value_counts()
print(waste_counts)

# 1. Top dishes by average leftover ratio
dish_waste = (
    df.groupby("dish_name")["leftover_ratio"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

print("\n===== Top Dishes by Average Leftover Ratio =====")
print(dish_waste.head(10))

dish_waste.to_csv("reports/top_dishes_by_leftover_ratio.csv", index=False)

# 2. Waste by kitchen section
section_waste = (
    df.groupby("kitchen_section")["leftover_ratio"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

print("\n===== Average Leftover Ratio by Kitchen Section =====")
print(section_waste)

section_waste.to_csv("reports/waste_by_kitchen_section.csv", index=False)

# 3. Waste by meal period
meal_waste = (
    df.groupby("meal_period")["leftover_ratio"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

print("\n===== Average Leftover Ratio by Meal Period =====")
print(meal_waste)

meal_waste.to_csv("reports/waste_by_meal_period.csv", index=False)

# 4. Waste by event type
event_waste = (
    df.groupby("event_type")["leftover_ratio"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

print("\n===== Average Leftover Ratio by Event Type =====")
print(event_waste)

event_waste.to_csv("reports/waste_by_event_type.csv", index=False)

# 5. Chart: waste level distribution
plt.figure(figsize=(6, 4))
waste_counts.plot(kind="bar")
plt.title("Waste Level Distribution")
plt.xlabel("Waste Level")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig("reports/figures/waste_level_distribution.png")
plt.close()

# 6. Chart: top dishes by leftover ratio
plt.figure(figsize=(8, 5))
dish_waste.head(10).plot(
    x="dish_name",
    y="leftover_ratio",
    kind="bar",
    legend=False
)
plt.title("Top 10 Dishes by Average Leftover Ratio")
plt.xlabel("Dish Name")
plt.ylabel("Average Leftover Ratio")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("reports/figures/top_dishes_by_leftover_ratio.png")
plt.close()

# 7. Chart: section waste
plt.figure(figsize=(7, 4))
section_waste.plot(
    x="kitchen_section",
    y="leftover_ratio",
    kind="bar",
    legend=False
)
plt.title("Average Leftover Ratio by Kitchen Section")
plt.xlabel("Kitchen Section")
plt.ylabel("Average Leftover Ratio")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("reports/figures/waste_by_kitchen_section.png")
plt.close()

# 8. Chart: meal period waste
plt.figure(figsize=(6, 4))
meal_waste.plot(
    x="meal_period",
    y="leftover_ratio",
    kind="bar",
    legend=False
)
plt.title("Average Leftover Ratio by Meal Period")
plt.xlabel("Meal Period")
plt.ylabel("Average Leftover Ratio")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("reports/figures/waste_by_meal_period.png")
plt.close()

print("\nAnalysis completed.")
print("CSV summaries saved in: reports/")
print("Figures saved in: reports/figures/")
