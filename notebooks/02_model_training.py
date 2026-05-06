import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay


# Create output folders
os.makedirs("models", exist_ok=True)
os.makedirs("reports/figures", exist_ok=True)

# Load data
df = pd.read_csv("data/buffet_waste_sample.csv")

# Target variable
target = "waste_level"

# Features selected for prediction
# Important: We do NOT use leftover_qty, leftover_ratio, possible_reason, or recommended_action.
# These are outcome-related fields and would cause data leakage.
features = [
    "meal_period",
    "dish_category",
    "kitchen_section",
    "estimated_guests",
    "actual_guests",
    "event_type",
    "occupancy_rate",
    "weather",
    "prepared_qty",
    "service_time_remaining",
    "refill_count",
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
]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features),
    ]
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train model
pipeline.fit(X_train, y_train)

# Predict
y_pred = pipeline.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=["Low", "Medium", "High"])

print("===== Model Training Completed =====")
print(f"Accuracy: {accuracy:.4f}")
print("\n===== Classification Report =====")
print(report)

# Save model
joblib.dump(pipeline, "models/waste_level_classifier.pkl")

# Save metrics
with open("reports/model_metrics.txt", "w", encoding="utf-8") as f:
    f.write("Waste Level Classification Model\n")
    f.write("=================================\n\n")
    f.write(f"Accuracy: {accuracy:.4f}\n\n")
    f.write("Classification Report:\n")
    f.write(report)

# Save confusion matrix chart
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Low", "Medium", "High"]
)

disp.plot()
plt.title("Confusion Matrix: Waste Level Classification")
plt.tight_layout()
plt.savefig("reports/figures/confusion_matrix_waste_level.png")
plt.close()

print("\nSaved model: models/waste_level_classifier.pkl")
print("Saved metrics: reports/model_metrics.txt")
print("Saved figure: reports/figures/confusion_matrix_waste_level.png")
