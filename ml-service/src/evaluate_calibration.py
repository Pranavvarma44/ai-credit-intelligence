import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import (
    brier_score_loss
)
from sklearn.calibration import calibration_curve


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
# LOAD MODELS
# --------------------------------------------------

tuned_xgboost = joblib.load(
    "models/xgboost_tuned.pkl"
)

calibrated_xgboost = joblib.load(
    "models/xgboost_calibrated.pkl"
)


# --------------------------------------------------
# GET PROBABILITIES
# --------------------------------------------------

raw_probability = (
    tuned_xgboost.predict_proba(
        X_test
    )[:, 1]
)

calibrated_probability = (
    calibrated_xgboost.predict_proba(
        X_test
    )[:, 1]
)


# --------------------------------------------------
# BRIER SCORES
# --------------------------------------------------

raw_brier = brier_score_loss(
    y_test,
    raw_probability
)

calibrated_brier = brier_score_loss(
    y_test,
    calibrated_probability
)


print("\n==============================")
print("CALIBRATION EVALUATION")
print("==============================")

print(
    f"Raw XGBoost Brier Score       : "
    f"{raw_brier:.4f}"
)

print(
    f"Calibrated XGBoost Brier Score: "
    f"{calibrated_brier:.4f}"
)


# --------------------------------------------------
# CALIBRATION CURVE
# --------------------------------------------------

raw_fraction, raw_mean = calibration_curve(
    y_test,
    raw_probability,
    n_bins=10,
    strategy="uniform"
)

calibrated_fraction, calibrated_mean = calibration_curve(
    y_test,
    calibrated_probability,
    n_bins=10,
    strategy="uniform"
)


# --------------------------------------------------
# PLOT
# --------------------------------------------------

plt.figure(figsize=(8, 6))

plt.plot(
    raw_mean,
    raw_fraction,
    marker="o",
    label="Raw XGBoost"
)

plt.plot(
    calibrated_mean,
    calibrated_fraction,
    marker="o",
    label="Calibrated XGBoost"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Perfect calibration"
)

plt.xlabel(
    "Mean predicted probability"
)

plt.ylabel(
    "Actual default rate"
)

plt.title(
    "Calibration Curve"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "plots/calibration_curve.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()