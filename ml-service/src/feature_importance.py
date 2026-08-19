import pandas as pd
import joblib
import matplotlib.pyplot as plt


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

X_train = pd.read_csv(
    "data/X_train.csv"
)


# --------------------------------------------------
# LOAD MODELS
# --------------------------------------------------

random_forest = joblib.load(
    "models/random_forest.pkl"
)

xgboost_model = joblib.load(
    "models/xgboost_model.pkl"
)


# --------------------------------------------------
# RANDOM FOREST IMPORTANCE
# --------------------------------------------------

rf_importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": random_forest.feature_importances_
})

rf_importance = rf_importance.sort_values(
    "importance",
    ascending=False
)


print("\n==============================")
print("RANDOM FOREST FEATURE IMPORTANCE")
print("==============================")

print(
    rf_importance.to_string(
        index=False
    )
)


# --------------------------------------------------
# XGBOOST IMPORTANCE
# --------------------------------------------------

xgb_importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": xgboost_model.feature_importances_
})

xgb_importance = xgb_importance.sort_values(
    "importance",
    ascending=False
)


print("\n==============================")
print("XGBOOST FEATURE IMPORTANCE")
print("==============================")

print(
    xgb_importance.to_string(
        index=False
    )
)


# --------------------------------------------------
# RANDOM FOREST PLOT
# --------------------------------------------------

plt.figure(figsize=(10, 7))

plt.barh(
    rf_importance["feature"].head(10)[::-1],
    rf_importance["importance"].head(10)[::-1]
)

plt.title(
    "Top 10 Random Forest Features"
)

plt.xlabel("Importance")

plt.tight_layout()

plt.savefig(
    "plots/random_forest_feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# --------------------------------------------------
# XGBOOST PLOT
# --------------------------------------------------

plt.figure(figsize=(10, 7))

plt.barh(
    xgb_importance["feature"].head(10)[::-1],
    xgb_importance["importance"].head(10)[::-1]
)

plt.title(
    "Top 10 XGBoost Features"
)

plt.xlabel("Importance")

plt.tight_layout()

plt.savefig(
    "plots/xgboost_feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()