import pandas as pd

from xgboost import XGBClassifier

from sklearn.model_selection import (
    RandomizedSearchCV,
    StratifiedKFold
)

import joblib


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
# BASE XGBOOST MODEL
# --------------------------------------------------

xgboost_model = XGBClassifier(
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)


# --------------------------------------------------
# PARAMETER SEARCH SPACE
# --------------------------------------------------

parameter_grid = {

    "n_estimators": [
        100,
        200,
        300,
        500
    ],

    "max_depth": [
        3,
        5,
        7,
        9
    ],

    "learning_rate": [
        0.01,
        0.03,
        0.05,
        0.1
    ],

    "subsample": [
        0.7,
        0.8,
        0.9,
        1.0
    ],

    "colsample_bytree": [
        0.7,
        0.8,
        0.9,
        1.0
    ]
}


# --------------------------------------------------
# 5-FOLD CROSS VALIDATION
# --------------------------------------------------

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# --------------------------------------------------
# RANDOMIZED SEARCH
# --------------------------------------------------

search = RandomizedSearchCV(
    estimator=xgboost_model,
    param_distributions=parameter_grid,
    n_iter=20,
    scoring="average_precision",
    cv=cv,
    verbose=2,
    random_state=42,
    n_jobs=-1
)


# --------------------------------------------------
# TRAIN
# --------------------------------------------------

print("\n==============================")
print("TUNING XGBOOST")
print("==============================")

search.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# BEST PARAMETERS
# --------------------------------------------------

print("\n==============================")
print("BEST PARAMETERS")
print("==============================")

print(
    search.best_params_
)


# --------------------------------------------------
# BEST CV SCORE
# --------------------------------------------------

print("\n==============================")
print("BEST CROSS-VALIDATION PR-AUC")
print("==============================")

print(
    search.best_score_
)


# --------------------------------------------------
# SAVE BEST MODEL
# --------------------------------------------------

best_xgboost = (
    search.best_estimator_
)

joblib.dump(
    best_xgboost,
    "models/xgboost_tuned.pkl"
)

print("\nTuned XGBoost saved.")