from pathlib import Path
import sys
import joblib
import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[3]

ML_SRC = SRC_DIR / "ml-service" / "src"
MODEL_DIR = ML_SRC / "models"

sys.path.insert(0, str(ML_SRC))

from preprocess import prepare_features


model = joblib.load(
    MODEL_DIR / "xgboost_tuned.pkl"
)

encoder = joblib.load(
    MODEL_DIR / "preprocessor.pkl"
)


base_applicant = {
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


print("\n==============================")
print("DTI SENSITIVITY TEST")
print("==============================")


for dti in [
    0.10,
    0.30,
    0.50,
    0.70,
    0.88,
    1.00,
    1.20
]:

    applicant = base_applicant.copy()

    applicant["post_loan_dti"] = dti

    data = pd.DataFrame(
        [applicant]
    )

    X = prepare_features(
        data,
        encoder=encoder,
        fit=False
    )

    probability = model.predict_proba(
        X
    )[0, 1]

    print(
        f"DTI: {dti:.2f} "
        f"→ Probability: {probability:.4f}"
    )