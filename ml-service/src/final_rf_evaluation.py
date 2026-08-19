import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)


# --------------------------------------------------
# LOAD TEST DATA
# --------------------------------------------------

X_test = pd.read_csv(
    "data/X_test.csv"
)

y_test = pd.read_csv(
    "data/y_test.csv"
).squeeze()


# --------------------------------------------------
# LOAD TUNED RANDOM FOREST
# --------------------------------------------------

random_forest = joblib.load(
    "models/random_forest_tuned.pkl"
)


# --------------------------------------------------
# FINAL RF THRESHOLD
# --------------------------------------------------

threshold = 0.45


# --------------------------------------------------
# PREDICT PROBABILITIES
# --------------------------------------------------

probability = (
    random_forest.predict_proba(
        X_test
    )[:, 1]
)


# --------------------------------------------------
# APPLY THRESHOLD
# --------------------------------------------------

prediction = (
    probability >= threshold
).astype(int)


# --------------------------------------------------
# METRICS
# --------------------------------------------------

accuracy = accuracy_score(
    y_test,
    prediction
)

precision = precision_score(
    y_test,
    prediction,
    zero_division=0
)

recall = recall_score(
    y_test,
    prediction,
    zero_division=0
)

f1 = f1_score(
    y_test,
    prediction,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    probability
)

pr_auc = average_precision_score(
    y_test,
    probability
)

cm = confusion_matrix(
    y_test,
    prediction
)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\n==============================")
print("TUNED RANDOM FOREST")
print("==============================")

print(f"Threshold : {threshold:.2f}")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")
print(f"PR-AUC    : {pr_auc:.4f}")

print("\nConfusion Matrix:")
print(cm)