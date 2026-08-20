import pandas as pd
import joblib

from xgboost import XGBClassifier

from sklearn.model_selection import (
    RandomizedSearchCV,
    StratifiedKFold
)

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score
)


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
# LOAD TEST DATA
# --------------------------------------------------

X_test = pd.read_csv(
    "data/X_test.csv"
)

y_test = pd.read_csv(
    "data/y_test.csv"
).squeeze()


print("\n==============================")
print("DATA")
print("==============================")

print("Training:", X_train.shape)
print("Testing :", X_test.shape)


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
# STRATIFIED 5-FOLD CROSS VALIDATION
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
# BEST MODEL
# --------------------------------------------------

best_xgboost = (
    search.best_estimator_
)


# --------------------------------------------------
# TEST PREDICTIONS
# --------------------------------------------------

y_probability = (
    best_xgboost.predict_proba(
        X_test
    )[:, 1]
)


# --------------------------------------------------
# DEFAULT CLASS PREDICTIONS
# --------------------------------------------------

y_prediction = (
    y_probability >= 0.5
).astype(int)


# --------------------------------------------------
# ROC-AUC
# --------------------------------------------------

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


# --------------------------------------------------
# PR-AUC
# --------------------------------------------------

pr_auc = average_precision_score(
    y_test,
    y_probability
)


print("\n==============================")
print("TEST RESULTS")
print("==============================")


print(
    f"ROC-AUC : {roc_auc:.4f}"
)

print(
    f"PR-AUC  : {pr_auc:.4f}"
)


# --------------------------------------------------
# CLASSIFICATION REPORT
# --------------------------------------------------

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")


print(
    classification_report(
        y_test,
        y_prediction,
        digits=4
    )
)


# --------------------------------------------------
# CONFUSION MATRIX
# --------------------------------------------------

print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")


print(
    confusion_matrix(
        y_test,
        y_prediction
    )
)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

joblib.dump(
    best_xgboost,
    "models/xgboost_tuned.pkl"
)


print("\n==============================")
print("MODEL SAVED")
print("==============================")

print(
    "models/xgboost_tuned.pkl"
)