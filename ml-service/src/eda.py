import pandas as pd

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

data = pd.read_csv(
    "credit_risk_dataset.csv"
)


# --------------------------------------------------
# BASIC INFORMATION
# --------------------------------------------------

print("\n==============================")
print("DATASET SHAPE")
print("==============================")

print(data.shape)


print("\n==============================")
print("COLUMNS")
print("==============================")

print(data.columns.tolist())


print("\n==============================")
print("DATA TYPES")
print("==============================")

print(data.dtypes)


# --------------------------------------------------
# MISSING VALUES
# --------------------------------------------------

print("\n==============================")
print("MISSING VALUES")
print("==============================")

print(
    data.isnull().sum()
)


# --------------------------------------------------
# DUPLICATES
# --------------------------------------------------

print("\n==============================")
print("DUPLICATES")
print("==============================")

print(
    data.duplicated().sum()
)


# --------------------------------------------------
# TARGET DISTRIBUTION
# --------------------------------------------------

print("\n==============================")
print("DEFAULT DISTRIBUTION")
print("==============================")

print(
    data["default"].value_counts()
)


print("\nDefault percentage:")

print(
    data["default"]
    .value_counts(normalize=True)
    * 100
)


# --------------------------------------------------
# NUMERICAL SUMMARY
# --------------------------------------------------

print("\n==============================")
print("NUMERICAL SUMMARY")
print("==============================")

print(
    data.describe().T
)


# --------------------------------------------------
# EMPLOYMENT TYPE
# --------------------------------------------------

print("\n==============================")
print("EMPLOYMENT TYPE")
print("==============================")

print(
    data["employment_type"].value_counts()
)


# --------------------------------------------------
# FIRST FIVE ROWS
# --------------------------------------------------

print("\n==============================")
print("SAMPLE DATA")
print("==============================")

print(
    data.head()
)

# --------------------------------------------------
# DEFAULT GROUP COMPARISON
# --------------------------------------------------

print("\n==============================")
print("FEATURE MEANS BY DEFAULT")
print("==============================")

comparison_features = [
    "monthly_income",
    "loan_amount",
    "monthly_debt_payment",
    "post_loan_dti",
    "credit_history_months",
    "credit_utilization",
    "repayment_consistency",
    "previous_missed_payments",
    "monthly_transactions",
    "average_transaction_amount",
    "spending_volatility",
    "cash_flow_stability",
    "income_stability"
]

print(
    data.groupby("default")[comparison_features].mean().T
)

print("\n==============================")
print("DEFAULT RATE BY EMPLOYMENT TYPE")
print("==============================")

employment_default_rate = (
    data.groupby("employment_type")["default"]
    .mean()
    .sort_values(ascending=False)
)

print(
    employment_default_rate
)

# --------------------------------------------------
# CORRELATION ANALYSIS
# --------------------------------------------------

print("\n==============================")
print("CORRELATION WITH DEFAULT")
print("==============================")

numeric_features = data.select_dtypes(
    include=["int64", "float64"]
)

default_correlations = (
    numeric_features.corr()["default"]
    .sort_values(ascending=False)
)

print(default_correlations)

print("\n==============================")
print("HIGH FEATURE CORRELATIONS")
print("==============================")

feature_corr = numeric_features.drop(
    columns=["default"]
).corr()

for i in range(len(feature_corr.columns)):
    for j in range(i + 1, len(feature_corr.columns)):

        correlation = feature_corr.iloc[i, j]

        if abs(correlation) >= 0.70:

            print(
                f"{feature_corr.columns[i]} "
                f"<-> "
                f"{feature_corr.columns[j]} "
                f": {correlation:.3f}"
            )