import numpy as np
import pandas as pd

np.random.seed(42)

N = 30000


# --------------------------------------------------
# 1. AGE
# --------------------------------------------------

age = np.random.randint(
    21,
    61,
    N
)


# --------------------------------------------------
# 2. EMPLOYMENT TYPE
# --------------------------------------------------

employment_type = np.random.choice(
    [
        "Salaried",
        "Self-Employed",
        "Contract"
    ],
    size=N,
    p=[0.6, 0.3, 0.1]
)


# --------------------------------------------------
# 3. EMPLOYMENT YEARS
# --------------------------------------------------

potential_work_years = age - 18

employment_fraction = np.random.beta(
    a=3,
    b=2,
    size=N
)

employment_years = (
    potential_work_years *
    employment_fraction
)

employment_years = np.maximum(
    employment_years,
    0.5
)

employment_years = np.round(
    employment_years,
    1
)


# --------------------------------------------------
# 4. MONTHLY INCOME
# --------------------------------------------------

monthly_income = np.random.lognormal(
    mean=np.log(50_000),
    sigma=0.55,
    size=N
)

monthly_income = np.clip(
    monthly_income,
    15_000,
    500_000
).astype(int)


# --------------------------------------------------
# 5. LOAN AMOUNT
# --------------------------------------------------

annual_income = monthly_income * 12

loan_to_income_ratio = np.random.lognormal(
    mean=np.log(0.45),
    sigma=0.45,
    size=N
)

loan_amount = (
    annual_income *
    loan_to_income_ratio
)

loan_amount = np.clip(
    loan_amount,
    25_000,
    2_000_000
).astype(int)


# --------------------------------------------------
# 6. LOAN TENURE
# --------------------------------------------------

loan_tenure_months = np.random.choice(
    [12, 24, 36, 48, 60],
    size=N,
    p=[0.10, 0.20, 0.35, 0.20, 0.15]
)


# --------------------------------------------------
# 7. INTEREST RATE
# --------------------------------------------------

interest_rate = np.random.uniform(
    10,
    24,
    N
)

monthly_rate = (
    interest_rate /
    12 /
    100
)


# --------------------------------------------------
# 8. NEW LOAN EMI
# --------------------------------------------------

P = loan_amount
r = monthly_rate
n = loan_tenure_months

loan_emi = (
    P * r * (1 + r) ** n
    / ((1 + r) ** n - 1)
)


# --------------------------------------------------
# 9. EXISTING LOANS
# --------------------------------------------------

existing_loans = np.random.poisson(
    lam=1.0,
    size=N
)

existing_loans = np.clip(
    existing_loans,
    0,
    5
)


# --------------------------------------------------
# 10. EXISTING LOAN PAYMENTS
# --------------------------------------------------

existing_loan_payment_per_loan = np.random.uniform(
    3_000,
    15_000,
    N
)

existing_loan_payment = (
    existing_loans *
    existing_loan_payment_per_loan
)


# --------------------------------------------------
# 11. TOTAL MONTHLY DEBT
# --------------------------------------------------

monthly_debt_payment = (
    loan_emi +
    existing_loan_payment
)


# --------------------------------------------------
# 12. POST-LOAN DTI
# --------------------------------------------------

debt_to_income_ratio = (
    monthly_debt_payment /
    monthly_income
)

debt_to_income_ratio = np.clip(
    debt_to_income_ratio,
    0,
    1.5
)


# --------------------------------------------------
# 13. NEW-TO-CREDIT FLAG
# --------------------------------------------------

# Prototype assumption:
# approximately 15% of applicants have no formal
# credit history.

ntc_flag = (
    np.random.random(N) < 0.15
)


# --------------------------------------------------
# 14. CREDIT HISTORY
# --------------------------------------------------

credit_history_months = np.zeros(N)

non_ntc = ~ntc_flag

credit_history_months[non_ntc] = np.random.gamma(
    shape=3,
    scale=20,
    size=non_ntc.sum()
)

max_credit_history = np.maximum(
    (age - 18) * 12,
    0
)

credit_history_months = np.minimum(
    credit_history_months,
    max_credit_history
)

credit_history_months = np.clip(
    credit_history_months,
    0,
    180
)

# Only NTC applicants should have zero history.
credit_history_months = np.where(
    ntc_flag,
    0,
    np.maximum(
        credit_history_months,
        1
    )
)

credit_history_months = (
    credit_history_months.astype(int)
)


# --------------------------------------------------
# 15. CREDIT UTILIZATION
# --------------------------------------------------

credit_utilization = np.zeros(N)

# Traditional utilization unavailable for NTC
# applicants in this prototype.

credit_utilization[non_ntc] = (
    np.random.beta(
        a=2.5,
        b=4.5,
        size=non_ntc.sum()
    ) * 100
)

credit_utilization = np.clip(
    credit_utilization,
    0,
    100
)


# --------------------------------------------------
# 16. PREVIOUS MISSED PAYMENTS
# --------------------------------------------------

previous_missed_payments = np.random.poisson(
    lam=0.4,
    size=N
)

previous_missed_payments = np.clip(
    previous_missed_payments,
    0,
    6
)


# --------------------------------------------------
# 17. REPAYMENT CONSISTENCY
# --------------------------------------------------

repayment_consistency = (
    np.random.beta(
        a=8,
        b=2,
        size=N
    ) * 100
)

repayment_consistency -= (
    previous_missed_payments * 8
)

repayment_consistency = np.clip(
    repayment_consistency,
    0,
    100
)


# --------------------------------------------------
# 18. MONTHLY TRANSACTIONS
# --------------------------------------------------

monthly_transactions = np.random.poisson(
    lam=40,
    size=N
)

monthly_transactions = np.maximum(
    monthly_transactions,
    1
)


# --------------------------------------------------
# 19. TRANSACTION VOLUME
# --------------------------------------------------

# Synthetic simulation parameter.
transaction_income_fraction = np.random.uniform(
    0.4,
    0.9,
    N
)

average_transaction_amount = (
    monthly_income *
    transaction_income_fraction /
    monthly_transactions
)

average_transaction_amount = np.maximum(
    average_transaction_amount,
    100
)

average_transaction_amount = np.round(
    average_transaction_amount,
    2
)


# --------------------------------------------------
# 20. SPENDING HISTORY
# --------------------------------------------------

spending_history = np.random.lognormal(
    mean=np.log(
        np.maximum(
            monthly_income *
            transaction_income_fraction,
            1
        )
    )[:, None],
    sigma=0.20,
    size=(N, 6)
)

spending_volatility = (
    spending_history.std(axis=1) /
    spending_history.mean(axis=1)
)


# --------------------------------------------------
# 21. INCOME HISTORY
# --------------------------------------------------

income_history = np.random.lognormal(
    mean=np.log(
        np.maximum(
            monthly_income,
            1
        )
    )[:, None],
    sigma=0.15,
    size=(N, 6)
)

income_variation = (
    income_history.std(axis=1) /
    income_history.mean(axis=1)
)


# --------------------------------------------------
# 22. INCOME STABILITY
# --------------------------------------------------

income_stability = (
    1 /
    (1 + income_variation)
)

income_stability = np.clip(
    income_stability,
    0,
    1
)


# --------------------------------------------------
# 23. NET CASH-FLOW HISTORY
# --------------------------------------------------

net_cash_flow_history = (
    income_history -
    spending_history
)


# --------------------------------------------------
# 24. NET CASH-FLOW VARIATION
# --------------------------------------------------

net_cash_flow_variation = (
    net_cash_flow_history.std(axis=1) /
    np.maximum(
        np.abs(
            net_cash_flow_history.mean(axis=1)
        ),
        1
    )
)


# --------------------------------------------------
# 25. CASH-FLOW STABILITY
# --------------------------------------------------

cash_flow_stability = (
    1 /
    (1 + net_cash_flow_variation)
)

cash_flow_stability = np.clip(
    cash_flow_stability,
    0,
    1
)


# --------------------------------------------------
# 26. CREATE INITIAL DATAFRAME
# --------------------------------------------------

data = pd.DataFrame({
    "age": age,
    "employment_type": employment_type,
    "employment_years": employment_years,
    "monthly_income": monthly_income,

    "loan_amount": loan_amount,
    "loan_tenure_months": loan_tenure_months,
    "existing_loans": existing_loans,
    "monthly_debt_payment": monthly_debt_payment,
    "post_loan_dti": debt_to_income_ratio,

    "credit_history_months": credit_history_months,
    "credit_utilization": credit_utilization,
    "repayment_consistency": repayment_consistency,
    "previous_missed_payments": previous_missed_payments,

    "monthly_transactions": monthly_transactions,
    "average_transaction_amount": average_transaction_amount,
    "spending_volatility": spending_volatility,
    "cash_flow_stability": cash_flow_stability,
    "income_stability": income_stability
})


# --------------------------------------------------
# 27. NORMALIZED RISK COMPONENTS
# --------------------------------------------------

dti_risk = np.clip(
    data["post_loan_dti"] / 1.0,
    0,
    1
)

utilization_risk = (
    data["credit_utilization"] / 100
)

missed_payment_risk = np.clip(
    data["previous_missed_payments"] / 3,
    0,
    1
)

repayment_risk = (
    1 -
    data["repayment_consistency"] / 100
)

spending_risk = np.clip(
    data["spending_volatility"] / 0.4,
    0,
    1
)

cash_flow_risk = (
    1 -
    data["cash_flow_stability"]
)

income_stability_risk = (
    1 -
    data["income_stability"]
)


# --------------------------------------------------
# 28. LATENT RISK SCORE
# --------------------------------------------------

risk_score = (
    2.0 * dti_risk
    + 1.5 * utilization_risk
    + 1.5 * missed_payment_risk
    + 1.5 * repayment_risk
    + 1.0 * spending_risk
    + 1.0 * cash_flow_risk
    + 0.8 * income_stability_risk
)


# --------------------------------------------------
# 29. PROBABILITY OF DEFAULT
# --------------------------------------------------

risk_threshold = 5.0

probability_of_default = (
    1 /
    (
        1 +
        np.exp(
            -(risk_score - risk_threshold)
        )
    )
)


# --------------------------------------------------
# 30. DEFAULT OUTCOME
# --------------------------------------------------

default = (
    np.random.random(N)
    <
    probability_of_default
).astype(int)


# --------------------------------------------------
# 31. ADD TARGET + MODELING VARIABLES
# --------------------------------------------------

data["risk_score"] = risk_score

data["probability_of_default"] = (
    probability_of_default
)

data["default"] = default


# --------------------------------------------------
# 32. SAVE DATASET
# --------------------------------------------------

data.to_csv(
    "credit_risk_dataset.csv",
    index=False
)


# --------------------------------------------------
# 33. VALIDATION
# --------------------------------------------------

print("\n==============================")
print("DATASET SUMMARY")
print("==============================")

print(
    data[
        [
            "age",
            "monthly_income",
            "loan_amount",
            "post_loan_dti",
            "credit_history_months",
            "credit_utilization",
            "previous_missed_payments",
            "spending_volatility",
            "cash_flow_stability",
            "income_stability"
        ]
    ].describe()
)


print("\n==============================")
print("PROBABILITY OF DEFAULT")
print("==============================")

print(
    data["probability_of_default"].describe()
)


print("\n==============================")
print("DEFAULT DISTRIBUTION")
print("==============================")

print(
    data["default"].value_counts()
)


print("\n==============================")
print("DEFAULT RATE")
print("==============================")

print(
    f"{data['default'].mean():.4%}"
)


print("\n==============================")
print("RISK SCORE BY DEFAULT")
print("==============================")

print(
    data.groupby("default")["risk_score"].mean()
)


print("\n==============================")
print("PROBABILITY BY DEFAULT")
print("==============================")

print(
    data.groupby("default")[
        "probability_of_default"
    ].mean()
)


print("\n==============================")
print("RISK FEATURES BY DEFAULT")
print("==============================")

print(
    data.groupby("default")[
        [
            "post_loan_dti",
            "credit_utilization",
            "previous_missed_payments",
            "repayment_consistency",
            "spending_volatility",
            "cash_flow_stability",
            "income_stability"
        ]
    ].mean()
)


print("\n==============================")
print("NTC PERCENTAGE")
print("==============================")

print(
    f"{(data['credit_history_months'] == 0).mean():.4%}"
)


print("\n==============================")
print("NTC CREDIT UTILIZATION")
print("==============================")

print(
    data[
        data["credit_history_months"] == 0
    ]["credit_utilization"].describe()
)


print("\n==============================")
print("DATASET SHAPE")
print("==============================")

print(data.shape)

print("\nDataset saved as:")
print("credit_risk_dataset.csv")