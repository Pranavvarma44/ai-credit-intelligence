import pandas as pd
import joblib


# --------------------------------------------------
# LOAD MODEL + PREPROCESSOR + THRESHOLD
# --------------------------------------------------

MODEL_PATH = "models/xgboost_tuned.pkl"
PREPROCESSOR_PATH = "models/preprocessor.pkl"
THRESHOLD_PATH = "models/final_threshold.txt"


model = joblib.load(MODEL_PATH)
encoder = joblib.load(PREPROCESSOR_PATH)

with open(THRESHOLD_PATH, "r") as file:
    threshold = float(file.read())


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

NUMERICAL_FEATURES = [
    "age",
    "employment_years",
    "monthly_income",
    "loan_amount",
    "loan_tenure_months",
    "existing_loans",
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

CATEGORICAL_FEATURES = [
    "employment_type"
]


# --------------------------------------------------
# PREDICTION FUNCTION
# --------------------------------------------------

def predict_credit_risk(applicant):

    # Convert dictionary to DataFrame
    data = pd.DataFrame(
        [applicant]
    )

    # ------------------------------
    # Numerical features
    # ------------------------------

    numerical_data = data[
        NUMERICAL_FEATURES
    ].copy()

    # ------------------------------
    # Categorical features
    # ------------------------------

    categorical_data = data[
        CATEGORICAL_FEATURES
    ].copy()

    # ------------------------------
    # One-hot encode
    # ------------------------------

    encoded = encoder.transform(
        categorical_data
    )

    encoded_columns = (
        encoder.get_feature_names_out(
            CATEGORICAL_FEATURES
        )
    )

    encoded_data = pd.DataFrame(
        encoded,
        columns=encoded_columns,
        index=data.index
    )

    # ------------------------------
    # Combine features
    # ------------------------------

    X = pd.concat(
        [
            numerical_data,
            encoded_data
        ],
        axis=1
    )

    # ------------------------------
    # Predict probability
    # ------------------------------

    probability = model.predict_proba(
        X
    )[0, 1]

    # ------------------------------
    # Apply threshold
    # ------------------------------

    prediction = int(
        probability >= threshold
    )

    # ------------------------------
    # Decision
    # ------------------------------

    if prediction == 1:
        decision = "Review"
    else:
        decision = "Approve"

    return {
        "probability_of_default": round(
            float(probability),
            4
        ),
        "decision": decision
    }
if __name__ == "__main__":

    applicant = {
        "age": 35,
        "employment_type": "Salaried",
        "employment_years": 8,
        "monthly_income": 50000,
        "loan_amount": 200000,
        "loan_tenure_months": 36,
        "existing_loans": 1,
        "monthly_debt_payment": 15000,
        "post_loan_dti": 0.45,
        "credit_history_months": 48,
        "credit_utilization": 30,
        "repayment_consistency": 80,
        "previous_missed_payments": 0,
        "monthly_transactions": 40,
        "average_transaction_amount": 800,
        "spending_volatility": 0.17,
        "cash_flow_stability": 0.70,
        "income_stability": 0.90
    }

    result = predict_credit_risk(
        applicant
    )

    print("\n==============================")
    print("PREDICTION")
    print("==============================")

    print(result)