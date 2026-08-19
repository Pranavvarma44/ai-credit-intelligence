import pandas as pd
import numpy as np


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

data = pd.read_csv(
    "credit_risk_dataset.csv"
)


# --------------------------------------------------
# RISK SCORE BINS
# --------------------------------------------------

data["risk_score_bin"] = pd.cut(
    data["risk_score"],
    bins=[
        0,
        2,
        2.5,
        3,
        3.5,
        4,
        5,
        np.inf
    ]
)


risk_analysis = (
    data
    .groupby(
        "risk_score_bin",
        observed=True
    )
    .agg(
        applicants=("default", "count"),
        defaults=("default", "sum"),
        default_rate=("default", "mean"),
        average_probability=(
            "probability_of_default",
            "mean"
        )
    )
)


# --------------------------------------------------
# PRINT RISK ANALYSIS
# --------------------------------------------------

print("\n==============================")
print("DEFAULT RATE BY RISK SCORE")
print("==============================")

print(
    risk_analysis
)


# --------------------------------------------------
# PROBABILITY BINS
# --------------------------------------------------

data["probability_bin"] = pd.cut(
    data["probability_of_default"],
    bins=[
        0,
        0.05,
        0.10,
        0.20,
        0.30,
        0.50,
        1.0
    ]
)


probability_analysis = (
    data
    .groupby(
        "probability_bin",
        observed=True
    )
    .agg(
        applicants=("default", "count"),
        defaults=("default", "sum"),
        actual_default_rate=("default", "mean"),
        average_predicted_probability=(
            "probability_of_default",
            "mean"
        )
    )
)


# --------------------------------------------------
# PRINT PROBABILITY ANALYSIS
# --------------------------------------------------

print("\n==============================")
print("ACTUAL DEFAULT RATE BY GENERATED PROBABILITY")
print("==============================")

print(
    probability_analysis
)


# --------------------------------------------------
# CORRELATIONS
# --------------------------------------------------

print("\n==============================")
print("TARGET CORRELATIONS")
print("==============================")

print(
    data[
        [
            "risk_score",
            "probability_of_default",
            "default"
        ]
    ].corr()
)


# --------------------------------------------------
# AVERAGES
# --------------------------------------------------

print("\n==============================")
print("AVERAGES BY DEFAULT")
print("==============================")

print(
    data.groupby("default")[
        [
            "risk_score",
            "probability_of_default"
        ]
    ].mean()
)