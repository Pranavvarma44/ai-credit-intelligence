import pandas as pd
from sklearn.metrics import(
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score,average_precision_score,
    confusion_matrix
    )
import joblib

#load data
X_test=pd.read_csv(
    "data/X_test.csv"    
)

y_test=pd.read_csv(
    "data/y_test.csv"
).squeeze()

#load models
random_forest=joblib.load("models/random_forest.pkl")
xgboost_model=joblib.load("models/xgboost_model.pkl")
tuned_random_forest = joblib.load(
    "models/random_forest_tuned.pkl"
)
tuned_xgboost = joblib.load(
    "models/xgboost_tuned.pkl"
)

#predictions
rf_probability = random_forest.predict_proba(
    X_test
)[:, 1]

xgb_probability = xgboost_model.predict_proba(
    X_test
)[:, 1]
tuned_rf_probability = (
    tuned_random_forest.predict_proba(
        X_test
    )[:, 1]
)
tuned_xgb_probability = (
    tuned_xgboost.predict_proba(
        X_test
    )[:, 1]
)
# DEFAULT PREDICTIONS
rf_prediction = (
    rf_probability >= 0.5
).astype(int)

xgb_prediction = (
    xgb_probability >= 0.5
).astype(int)
tuned_rf_prediction = (
    tuned_rf_probability >= 0.5
).astype(int)
tuned_xgb_prediction = (
    tuned_xgb_probability >= 0.5
).astype(int)

def evaluate_model(
        name,y_true,prediction,probability
):
    print(name)
    accuracy=accuracy_score(y_true,prediction)
    precision=precision_score(y_true,prediction,zero_division=0)
    recall=recall_score(y_true,prediction,zero_division=0)
    f1=f1_score(y_true,prediction,zero_division=0)
    roc_auc=roc_auc_score(y_true,probability)
    pr_auc=average_precision_score(y_true,probability)
    cm=confusion_matrix(y_true,prediction)
    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1 Score : {f1:.4f}"
    )

    print(
        f"ROC-AUC  : {roc_auc:.4f}"
    )

    print(
        f"PR-AUC   : {pr_auc:.4f}"
    )

    print("\nConfusion Matrix:")

    print(cm)
    return {
        "model": name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "pr_auc": pr_auc
    }
rf_results = evaluate_model(
    "Random Forest",
    y_test,
    rf_prediction,
    rf_probability
)

xgb_results = evaluate_model(
    "XGBoost",
    y_test,
    xgb_prediction,
    xgb_probability
)
tuned_rf_results = evaluate_model(
    "Tuned Random Forest",
    y_test,
    tuned_rf_prediction,
    tuned_rf_probability
)
tuned_xgb_results = evaluate_model(
    "Tuned XGBoost",
    y_test,
    tuned_xgb_prediction,
    tuned_xgb_probability
)
results = pd.DataFrame([
    rf_results,
    xgb_results,
    tuned_rf_results,
    tuned_xgb_results
])

print("MODEL COMPARISON")


print(
    results.to_string(
        index=False
    )
)