import sys
from pathlib import Path
from app.services.explainability import get_risk_factors
from app.services.gemini import generate_risk_explanation

# --------------------------------------------------
# ML SERVICE PATH
# --------------------------------------------------

PROJECT_ROOT = (
    Path(__file__).resolve()
    .parents[3]
)

ML_SRC = PROJECT_ROOT / "ml-service" / "src"

sys.path.insert(
    0,
    str(ML_SRC)
)


from predict import predict_credit_risk


# --------------------------------------------------
# PREDICTION SERVICE
# --------------------------------------------------

def predict_applicant(applicant_data):

    prediction = predict_credit_risk(
        applicant_data
    )

    risk_factors = get_risk_factors(
        applicant_data
    )

    explanation = generate_risk_explanation(
        probability=prediction["probability_of_default"],
        decision=prediction["decision"],
        risk_increasing_factors=
            risk_factors["risk_increasing_factors"],
        risk_reducing_factors=
            risk_factors["risk_reducing_factors"]
    )

    return {
        **prediction,
        **risk_factors,
        "explanation": explanation
    }