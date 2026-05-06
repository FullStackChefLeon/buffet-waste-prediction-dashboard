import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay


os.makedirs("models", exist_ok=True)
os.makedirs("reports/figures", exist_ok=True)

df = pd.read_csv("data/buffet_waste_sample.csv")

# -----------------------------
# Feature Engineering
# -----------------------------

df["guest_difference"] = df["estimated_guests"] - df["actual_guests"]

df["guest_accuracy_ratio"] = df["actual_guests"] / df["estimated_guests"]

df["prepared_qty_per_estimated_guest"] = df["prepared_qty"] / df["estimated_guests"]

df["prepared_qty_per_actual_guest"] = df["prepared_qty"] / df["actual_guests"]

df["refill_per_15min"] = df["refill_count"] / (df["service_time_remaining"] / 15)

df["is_late_service"] = (df["service_time_remaining"] <= 30).astype(int)

df["is_low_occupancy"] = (df["occupancy_rate"] < 0.60).astype(int)

df["is_normal_service"] = (df["event_type"] == "normal").astype(int)

df["is_late_high_refill"] = (
    (df["service_time_remaining"] <= 30) & (df["refill_count"] >= 2)
).astype(int)


target = "waste_level"

features = [
    "meal_period",
    "dish_category",
    "kitchen_section",
    "event_type",
    "weather",
    "estimated_guests",
    "actual_guests",
    "occupancy_rate",
    "prepared_qty",
    "service_time_remaining",
    "refill_count",
    "guest_difference",
    "guest_accuracy_ratio",
    "prepared_qty_per_estimated_guest",
    "prepared_qty_per_actual_guest",
    "refill_per_15min",
    "is_late_service",
    "is_low_occupancy",
    "is_normal_service",
    "is_late_high_refill",
]

X = df[features]
y = df[target]

categorical_features = [
    "meal_period",
    "dish_category",
    "kitchen_section",
    "event_type",
    "weather",
]

numeric_features = [
    "estimated_guests",
    "actual_guests",
    "occupancy_rate",
    "prepared_qty",
    "service_time_remaining",
    "refill_count",
    "guest_difference",
    "guest_accuracy_ratio",
    "prepared_qty_per_estimated_guest",
    "prepared_qty_per_actual_guest",
    "refill_per_15min",
    "is_late_service",
    "is_low_occupancy",
    "is_normal_service",
    "is_late_high_refill",
]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", StandardScaler(), numeric_features),
    ]
)

model = RandomForestClassifier(
    n_estimators=400,
    max_depth=8,
    min_samples_leaf=4,
    random_state=42,
    class_weight="balanced_subsample"
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=["Low", "Medium", "High"])

print("===== Improved Model Training Completed =====")
print(f"Accuracy: {accuracy:.4f}")
print("\n===== Classification Report =====")
print(report)

joblib.dump(pipeline, "models/improved_waste_level_classifier.pkl")

with open("reports/improved_model_metrics.txt", "w", encoding="utf-8") as f:
    f.write("Improved Waste Level Classification Model\n")
    f.write("=========================================\n\n")
    f.write(f"Accuracy: {accuracy:.4f}\n\n")
    f.write("Classification Report:\n")
    f.write(report)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Low", "Medium", "High"]
)

disp.plot()
plt.title("Improved Model Confusion Matrix")
plt.tight_layout()
plt.savefig("reports/figures/improved_confusion_matrix_waste_level.png")
plt.close()

print("\nSaved model: models/improved_waste_level_classifier.pkl")
print("Saved metrics: reports/improved_model_metrics.txt")
print("Saved figure: reports/figures/improved_confusion_matrix_waste_level.png")
