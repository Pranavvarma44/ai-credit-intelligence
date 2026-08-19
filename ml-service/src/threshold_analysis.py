import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score
)

import joblib


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

X_test = pd.read_csv(
    "data/X_test.csv"
)

y_test = pd.read_csv(
    "data/y_test.csv"
).squeeze()


# --------------------------------------------------
# LOAD MODELS
# --------------------------------------------------

random_forest = joblib.load(
    "models/random_forest.pkl"
)

xgboost_model = joblib.load(
    "models/xgboost_model.pkl"
)
tuned_xgboost = joblib.load(
    "models/xgboost_tuned.pkl"
)


# --------------------------------------------------
# GET PROBABILITIES
# --------------------------------------------------

rf_probability = random_forest.predict_proba(
    X_test
)[:, 1]

xgb_probability = xgboost_model.predict_proba(
    X_test
)[:, 1]
tuned_xgb_probability = (
    tuned_xgboost.predict_proba(
        X_test
    )[:, 1]
)


# --------------------------------------------------
# THRESHOLD ANALYSIS
# --------------------------------------------------

thresholds = [
    0.05,
    0.075,
    0.10,
    0.125,
    0.15,
    0.175,
    0.20,
    0.25,
    0.30,
    0.40,
    0.50
]

for name, probability in [
    ("Random Forest", rf_probability),
    ("XGBoost", xgb_probability),
    ("Tuned XGBoost", tuned_xgb_probability)
]:

    print("\n==============================")
print("TUNED XGBOOST")
print("==============================")

print(
    "\nThreshold | Precision | Recall | F1"
)

for threshold in thresholds:

    prediction = (
        tuned_xgb_probability >= threshold
    ).astype(int)

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

    print(
        f"{threshold:9.2f} | "
        f"{precision:9.4f} | "
        f"{recall:6.4f} | "
        f"{f1:6.4f}"
    )