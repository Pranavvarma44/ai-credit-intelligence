import pandas as pd
import joblib

from sklearn.calibration import CalibratedClassifierCV


# --------------------------------------------------
# LOAD TRAINING DATA
# --------------------------------------------------

X_train = pd.read_csv(
    "data/X_train.csv"
)

y_train = pd.read_csv(
    "data/y_train.csv"
).squeeze()


# --------------------------------------------------
# LOAD TUNED XGBOOST
# --------------------------------------------------

xgboost_model = joblib.load(
    "models/xgboost_tuned.pkl"
)


# --------------------------------------------------
# CALIBRATE MODEL
# --------------------------------------------------

calibrated_xgboost = CalibratedClassifierCV(
    estimator=xgboost_model,
    method="sigmoid",
    cv=5,
    n_jobs=-1
)


# --------------------------------------------------
# TRAIN CALIBRATED MODEL
# --------------------------------------------------

print("\n==============================")
print("CALIBRATING XGBOOST")
print("==============================")

calibrated_xgboost.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

joblib.dump(
    calibrated_xgboost,
    "models/xgboost_calibrated.pkl"
)

print(
    "\nCalibrated XGBoost saved."
)