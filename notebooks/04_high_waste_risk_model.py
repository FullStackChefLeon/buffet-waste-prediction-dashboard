import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

os.makedirs("models", exist_ok=True)
os.makedirs("reports/figures", exist_ok=True)

df = pd.read_csv("data/buffet_waste_sample.csv")

# Binary target:
# 1 = High Waste Risk
# 0 = Not High Waste Risk
df["high_waste_risk"] = (df["waste_level"] == "High").astype(int)

# Feature engineering
# Note: We avoid using leftover_qty and leftover_ratio because they are outcome variables.

df["prepared_qty_per_estimated_guest"] = df["prepared_qty"] / df["estimated_guests"]

df["refill_per_15min"] = df["refill_count"] / (df["service_time_remaining"] / 15)

df["is_late_service"] = (df["service_time_remaining"] <= 30).astype(int)

df["is_low_occupancy"] = (df["occupancy_rate"] < 0.60).astype(int)

df["is_normal_service"] = (df["event_type"] == "normal").astype(int)

df["is_late_high_refill"] = (
    (df["service_time_remaining"] <= 30) & (df["refill_count"] >= 2)
).astype(int)

target = "high_waste_risk"

features = [
    "meal_period",
    "dish_category",
    "kitchen_section",
    "event_type",
    "weather",
    "estimated_guests",
    "occupancy_rate",
    "prepared_qty",
    "service_time_remaining",
    "refill_count",
    "prepared_qty_per_estimated_guest",
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
    "occupancy_rate",
    "prepared_qty",
    "service_time_remaining",
    "refill_count",
    "prepared_qty_per_estimated_guest",
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
    class_weight="balanced"
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

# Predict probabilities
y_proba = pipeline.predict_proba(X_test)[:, 1]

# Threshold:
# Lower threshold means the model is more sensitive to high waste risk.
threshold = 0.45
y_pred = (y_proba >= threshold).astype(int)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)

report = classification_report(
    y_test,
    y_pred,
    target_names=["Not High Waste Risk", "High Waste Risk"]
)

cm = confusion_matrix(y_test, y_pred)

print("===== High Waste Risk Model Completed =====")
print(f"Threshold: {threshold}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc:.4f}")

print("\n===== Classification Report =====")
print(report)

joblib.dump(pipeline, "models/high_waste_risk_model.pkl")

with open("reports/high_waste_risk_model_metrics.txt", "w", encoding="utf-8") as f:
    f.write("High Waste Risk Binary Classification Model\n")
    f.write("===========================================\n\n")
    f.write(f"Threshold: {threshold}\n")
    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"F1-score: {f1:.4f}\n")
    f.write(f"ROC-AUC: {roc_auc:.4f}\n\n")
    f.write("Classification Report:\n")
    f.write(report)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Not High Risk", "High Risk"]
)

disp.plot()
plt.title("High Waste Risk Confusion Matrix")
plt.tight_layout()
plt.savefig("reports/figures/high_waste_risk_confusion_matrix.png")
plt.close()

print("\nSaved model: models/high_waste_risk_model.pkl")
print("Saved metrics: reports/high_waste_risk_model_metrics.txt")
print("Saved figure: reports/figures/high_waste_risk_confusion_matrix.png")
