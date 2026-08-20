import sys
from pathlib import Path


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


# --------------------------------------------------
# IMPORT ML PREDICTION
# --------------------------------------------------

from predict import predict_credit_risk


# --------------------------------------------------
# PREDICTION SERVICE
# --------------------------------------------------

def predict_applicant(applicant_data):

    # ------------------------------------------
    # XGBOOST PREDICTION ONLY
    # ------------------------------------------

    prediction = predict_credit_risk(
        applicant_data
    )


    # ------------------------------------------
    # RETURN PREDICTION
    # ------------------------------------------

    return prediction