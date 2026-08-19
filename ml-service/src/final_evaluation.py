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
# LOAD FINAL MODEL
# --------------------------------------------------

xgboost_model = joblib.load(
    "models/xgboost_tuned.pkl"
)


# --------------------------------------------------
# FINAL THRESHOLD
# --------------------------------------------------

with open(
    "models/final_threshold.txt",
    "r"
) as file:

    threshold = float(
        file.read()
    )


# --------------------------------------------------
# PREDICT PROBABILITIES
# --------------------------------------------------

probability = (
    xgboost_model.predict_proba(
        X_test
    )[:, 1]
)


# --------------------------------------------------
# APPLY FINAL THRESHOLD
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
# PRINT RESULTS
# --------------------------------------------------

print("\n==============================")
print("FINAL MODEL EVALUATION")
print("==============================")

print(
    f"Final threshold : {threshold:.2f}"
)

print(
    f"Accuracy        : {accuracy:.4f}"
)

print(
    f"Precision       : {precision:.4f}"
)

print(
    f"Recall          : {recall:.4f}"
)

print(
    f"F1 Score        : {f1:.4f}"
)

print(
    f"ROC-AUC         : {roc_auc:.4f}"
)

print(
    f"PR-AUC          : {pr_auc:.4f}"
)

print("\nConfusion Matrix:")

print(cm)