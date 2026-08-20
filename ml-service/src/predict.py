from pathlib import Path

import pandas as pd
import joblib


# --------------------------------------------------
# PATHS
# --------------------------------------------------

SRC_DIR = Path(__file__).resolve().parent
MODELS_DIR = SRC_DIR / "models"

MODEL_PATH = MODELS_DIR / "xgboost_tuned.pkl"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.pkl"
THRESHOLD_PATH = MODELS_DIR / "final_threshold.txt"


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load(
    MODEL_PATH
)

encoder = joblib.load(
    PREPROCESSOR_PATH
)


with open(
    THRESHOLD_PATH,
    "r"
) as file:

    threshold = float(
        file.read()
    )


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
    "ntc_flag"
]


CATEGORICAL_FEATURES = [
    "employment_type"
]


# --------------------------------------------------
# PREDICTION FUNCTION
# --------------------------------------------------

def predict_credit_risk(applicant):

    # ------------------------------
    # Convert dictionary to DataFrame
    # ------------------------------

    data = pd.DataFrame(
        [applicant]
    )


    # ------------------------------
    # Validate NTC information
    # ------------------------------

    if applicant["ntc_flag"] == 1:

        # NTC applicants should not have
        # previous formal credit information.

        data["existing_loans"] = 0
        data["credit_history_months"] = 0
        data["credit_utilization"] = 0
        data["previous_missed_payments"] = 0


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


    # ------------------------------
    # Return result
    # ------------------------------

    return {

        "probability_of_default":
            round(
                float(probability),
                4
            ),

        "decision":
            decision
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    # ----------------------------------------------
    # LOW-RISK NTC APPLICANT
    # ----------------------------------------------

    applicant = {
     "age": 24,
    "employment_type": "Contract",
    "employment_years": 2,
    "monthly_income": 25000,
    "loan_amount": 600000,
    "loan_tenure_months": 24,
    "existing_loans": 0,
    "monthly_debt_payment": 22000,
    "post_loan_dti": 0.88,
    "credit_history_months": 0,
    "credit_utilization": 0,
    "repayment_consistency": 65,
    "previous_missed_payments": 0,
    "monthly_transactions": 30,
    "average_transaction_amount": 700,
    "ntc_flag": 1
}

    result = predict_credit_risk(
        applicant
    )


    print("\n==============================")
    print("PREDICTION")
    print("==============================")


    print(
        f"Probability of default: "
        f"{result['probability_of_default']}"
    )


    print(
        f"Decision: "
        f"{result['decision']}"
    )


    print(
        f"Threshold: "
        f"{threshold}"
    )