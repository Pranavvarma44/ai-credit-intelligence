import sys
from pathlib import Path

import joblib
import pandas as pd
import shap


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

ML_SRC = PROJECT_ROOT / "ml-service" / "src"
MODEL_DIR = ML_SRC / "models"

sys.path.insert(0, str(ML_SRC))


# --------------------------------------------------
# IMPORT SHARED PREPROCESSING
# --------------------------------------------------

from preprocess import prepare_features


# --------------------------------------------------
# LOAD MODEL + PREPROCESSOR
# --------------------------------------------------

model = joblib.load(
    MODEL_DIR / "xgboost_tuned.pkl"
)

encoder = joblib.load(
    MODEL_DIR / "preprocessor.pkl"
)


# --------------------------------------------------
# SHAP EXPLAINER
# --------------------------------------------------

explainer = shap.TreeExplainer(model)


# --------------------------------------------------
# EXPLAIN PREDICTION
# --------------------------------------------------

def explain_prediction(applicant):

    # Convert dictionary to DataFrame
    data = pd.DataFrame(
        [applicant]
    )

    # Use the same preprocessing
    # used during model training
    X = prepare_features(
        data,
        encoder=encoder,
        fit=False
    )

    # Calculate SHAP values
    shap_values = explainer.shap_values(
        X
    )

    values = shap_values[0]

    feature_names = X.columns

    contributions = []

    for feature, value in zip(
        feature_names,
        values
    ):

        contributions.append({
            "feature": feature,
            "shap_value": float(value)
        })

    # Sort by absolute impact
    contributions.sort(
        key=lambda x: abs(x["shap_value"]),
        reverse=True
    )

    return contributions
def get_risk_factors(applicant, top_n=5):

    contributions = explain_prediction(
        applicant
    )

    risk_increasing = []
    risk_reducing = []

    for item in contributions:

        shap_value = item["shap_value"]

        factor = {
            "feature": item["feature"],
            "impact": round(
                abs(shap_value),
                4
            )
        }

        if shap_value > 0:

            factor["direction"] = "increases_risk"

            risk_increasing.append(
                factor
            )

        elif shap_value < 0:

            factor["direction"] = "reduces_risk"

            risk_reducing.append(
                factor
            )

    # Already sorted by absolute SHAP value,
    # but sort each group again for clarity.

    risk_increasing.sort(
        key=lambda x: x["impact"],
        reverse=True
    )

    risk_reducing.sort(
        key=lambda x: x["impact"],
        reverse=True
    )

    return {
        "risk_increasing_factors": risk_increasing[:top_n],
        "risk_reducing_factors": risk_reducing[:top_n]
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

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

    results = get_risk_factors(
        applicant
    )

    print("\n==============================")
    print("RISK INCREASING FACTORS")
    print("==============================")

    for item in results["risk_increasing_factors"]:
        print(item)

    print("\n==============================")
    print("RISK REDUCING FACTORS")
    print("==============================")

    for item in results["risk_reducing_factors"]:
        print(item)