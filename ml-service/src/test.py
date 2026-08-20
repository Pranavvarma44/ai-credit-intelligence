import pandas as pd

data = pd.read_csv("data/train.csv")

print("\n==============================")
print("NTC DEFAULT RATE")
print("==============================")

print(
    data.groupby("ntc_flag")["default"].mean()
)


print("\n==============================")
print("NTC RISK BY DTI")
print("==============================")

data["dti_bucket"] = pd.cut(
    data["post_loan_dti"],
    bins=[0, 0.3, 0.5, 0.7, 1.0, 1.5],
    include_lowest=True
)

print(
    data[
        data["ntc_flag"] == 1
    ].groupby("dti_bucket", observed=True)["default"].agg(
        ["count", "mean"]
    )
)


print("\n==============================")
print("HIGH-RISK NTC APPLICANTS")
print("==============================")

high_risk_ntc = data[
    (data["ntc_flag"] == 1) &
    (data["post_loan_dti"] >= 0.8)
]

print(
    high_risk_ntc[
        [
            "monthly_income",
            "loan_amount",
            "post_loan_dti",
            "employment_years",
            "employment_type",
            "default"
        ]
    ].describe()
)


print("\n==============================")
print("HIGH-RISK NTC DEFAULT RATE")
print("==============================")

print(
    high_risk_ntc["default"].mean()
)

print(
    "Count:",
    len(high_risk_ntc)
)