import pandas as pd

from sklearn.ensemble import RandomForestClassifier
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
# BASE MODEL
# --------------------------------------------------

random_forest = RandomForestClassifier(
    class_weight="balanced",
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
        5,
        8,
        12,
        16,
        None
    ],

    "min_samples_leaf": [
        1,
        2,
        5,
        10
    ],

    "max_features": [
        "sqrt",
        "log2",
        0.5
    ]
}


# --------------------------------------------------
# CROSS-VALIDATION
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
    estimator=random_forest,
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
print("TUNING RANDOM FOREST")
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
# BEST MODEL
# --------------------------------------------------

best_random_forest = (
    search.best_estimator_
)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

joblib.dump(
    best_random_forest,
    "models/random_forest_tuned.pkl"
)

print("\nTuned Random Forest saved.")