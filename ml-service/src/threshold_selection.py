import pandas as pd
import joblib
from sklearn.model_selection import StratifiedKFold,cross_val_predict
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score
)
X_train = pd.read_csv(
    "data/X_train.csv"
)

y_train = pd.read_csv(
    "data/y_train.csv"
).squeeze()

xgboost_model = joblib.load(
    "models/xgboost_tuned.pkl"
)
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)
oof_probability = cross_val_predict(
    xgboost_model,
    X_train,
    y_train,
    cv=cv,
    method="predict_proba",
    n_jobs=-1
)[:, 1]
thresholds = [
    0.05,
    0.07,
    0.10,
    0.12,
    0.15,
    0.17,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50
]
results = []

print("\n==============================")
print("OUT-OF-FOLD THRESHOLD ANALYSIS")
print("==============================")

print(
    "\nThreshold | Precision | Recall | F1"
)

for threshold in thresholds:

    prediction = (
        oof_probability >= threshold
    ).astype(int)

    precision = precision_score(
        y_train,
        prediction,
        zero_division=0
    )

    recall = recall_score(
        y_train,
        prediction,
        zero_division=0
    )

    f1 = f1_score(
        y_train,
        prediction,
        zero_division=0
    )

    results.append({
        "threshold": threshold,
        "precision": precision,
        "recall": recall,
        "f1": f1
    })

    print(
        f"{threshold:9.2f} | "
        f"{precision:9.4f} | "
        f"{recall:6.4f} | "
        f"{f1:6.4f}"
    )
results_df = pd.DataFrame(results)

best_row = results_df.loc[
    results_df["f1"].idxmax()
]

best_threshold = best_row["threshold"]

print("\n==============================")
print("BEST THRESHOLD")
print("==============================")

print(
    f"Threshold : {best_threshold:.2f}"
)

print(
    f"Precision : {best_row['precision']:.4f}"
)

print(
    f"Recall    : {best_row['recall']:.4f}"
)

print(
    f"F1        : {best_row['f1']:.4f}"
)


# --------------------------------------------------
# SAVE THRESHOLD
# --------------------------------------------------

with open(
    "models/final_threshold.txt",
    "w"
) as file:

    file.write(
        str(best_threshold)
    )

print("\nThreshold saved.")
