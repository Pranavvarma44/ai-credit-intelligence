import os 
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import joblib

X_train=pd.read_csv(
     "data/X_train.csv"
)

X_test=pd.read_csv(
     "data/X_test.csv"
)

y_train=pd.read_csv(
     "data/y_train.csv"
).squeeze()

y_test=pd.read_csv(
     "data/y_test.csv"
).squeeze()

print("Data")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)
print("X_test :", X_test.shape)
print("y_test :", y_test.shape)

random_forest=RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    min_samples_leaf=5,
    max_features="sqrt",
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

xgboost_model=XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42
)
print("TRAINING RANDOM FOREST")
random_forest.fit(X_train,y_train)
print("Random Forest training complete.")

print("TRAINING XGBOOST")
xgboost_model.fit(X_train,y_train)
print("XGBoost training complete.")

# --------------------------------------------------
# PREDICT PROBABILITIES
# --------------------------------------------------

rf_probability = random_forest.predict_proba(
    X_test
)[:, 1]

xgb_probability = xgboost_model.predict_proba(
    X_test
)[:, 1]


# --------------------------------------------------
# DEFAULT PREDICTIONS
# --------------------------------------------------

rf_prediction = (
    rf_probability >= 0.5
).astype(int)

xgb_prediction = (
    xgb_probability >= 0.5
).astype(int)

print("SAMPLE PREDICTIONS")
print("\nRandom Forest:")
print(rf_probability[:10])

print("\nXGBoost:")
print(xgb_probability[:10])

os.makedirs(
    "models",
    exist_ok=True
)


joblib.dump(
    random_forest,
    "models/random_forest.pkl"
)

joblib.dump(
    xgboost_model,
    "models/xgboost_model.pkl"
)


print("\n==============================")
print("MODELS SAVED")
print("==============================")

print("models/random_forest.pkl")
print("models/xgboost_model.pkl")