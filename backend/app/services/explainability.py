from pathlib import Path
import sys

import pandas as pd
import joblib
import shap


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

SRC_DIR = Path(__file__).resolve().parents[3]

ML_SRC = SRC_DIR / "ml-service" / "src"
MODEL_DIR = ML_SRC / "models"


# --------------------------------------------------
# IMPORT SHARED PREPROCESSING
# --------------------------------------------------

sys.path.insert(
    0,
    str(ML_SRC)
)

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

explainer = shap.TreeExplainer(
    model
)


# --------------------------------------------------
# EXPLAIN PREDICTION
# --------------------------------------------------

def explain_prediction(applicant):

    data = pd.DataFrame(
        [applicant]
    )

    X = prepare_features(
        data,
        encoder=encoder,
        fit=False
    )

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

            "shap_value": round(
                float(value),
                6
            )
        })

    # --------------------------------------------------
    # SORT BY ABSOLUTE SHAP IMPACT
    # --------------------------------------------------

    contributions.sort(
        key=lambda x: abs(
            x["shap_value"]
        ),
        reverse=True
    )

    return contributions


# --------------------------------------------------
# FEATURE DESCRIPTIONS
# --------------------------------------------------

def get_feature_description(
    feature,
    ntc=False
):

    # --------------------------------------------------
    # NTC-SPECIFIC DESCRIPTIONS
    # --------------------------------------------------

    if ntc:

        ntc_descriptions = {

            "credit_history_months":
                "No previous formal credit history",

            "credit_utilization":
                "No previous revolving-credit utilization",

            "previous_missed_payments":
                "No previous repayment history",

            "repayment_consistency":
                "No established repayment history"
        }

        if feature in ntc_descriptions:

            return ntc_descriptions[
                feature
            ]


    # --------------------------------------------------
    # NORMAL DESCRIPTIONS
    # --------------------------------------------------

    descriptions = {

        "post_loan_dti":
            "Post-loan debt-to-income ratio",

        "monthly_income":
            "Monthly income",

        "loan_amount":
            "Requested loan amount",

        "loan_tenure_months":
            "Loan tenure",

        "existing_loans":
            "Existing loans",

        "monthly_debt_payment":
            "Monthly debt payment",

        "credit_history_months":
            "Credit history length",

        "credit_utilization":
            "Credit utilization",

        "previous_missed_payments":
            "Previous missed payments",

        "repayment_consistency":
            "Repayment consistency",

        "monthly_transactions":
            "Monthly transactions",

        "average_transaction_amount":
            "Average transaction amount",

        "age":
            "Age",

        "employment_years":
            "Employment history",

        "employment_type_Contract":
            "Contract employment",

        "employment_type_Salaried":
            "Salaried employment",

        "employment_type_Self-Employed":
            "Self-employed",

        "ntc_flag":
            "New-to-credit status"
    }

    return descriptions.get(
        feature,
        feature
    )


# --------------------------------------------------
# FORMAT FEATURE VALUE
# --------------------------------------------------

def format_feature_value(
    feature,
    value,
    applicant
):

    if value is None:

        return None


    # --------------------------------------------------
    # NTC FLAG
    # --------------------------------------------------

    if feature == "ntc_flag":

        return (
            "New to Credit"
            if value == 1
            else
            "Established Credit"
        )


    # --------------------------------------------------
    # EMPLOYMENT TYPE
    # --------------------------------------------------

    if feature.startswith(
        "employment_type_"
    ):

        if value == 1:

            return feature.replace(
                "employment_type_",
                ""
            )

        return None


    # --------------------------------------------------
    # DTI
    # --------------------------------------------------

    if feature == "post_loan_dti":

        return (
            f"{float(value) * 100:.1f}%"
        )


    # --------------------------------------------------
    # CREDIT UTILIZATION
    # --------------------------------------------------

    if feature == "credit_utilization":

        return (
            f"{float(value):.1f}%"
        )


    # --------------------------------------------------
    # REPAYMENT CONSISTENCY
    # --------------------------------------------------

    if feature == "repayment_consistency":

        return (
            f"{float(value):.1f}%"
        )


    # --------------------------------------------------
    # CURRENCY VALUES
    # --------------------------------------------------

    if feature in {
        "monthly_income",
        "loan_amount",
        "monthly_debt_payment",
        "average_transaction_amount"
    }:

        return (
            f"₹{float(value):,.0f}"
        )


    # --------------------------------------------------
    # NORMAL NUMERICAL VALUES
    # --------------------------------------------------

    if isinstance(
        value,
        (int, float)
    ):

        if float(value).is_integer():

            return str(
                int(value)
            )

        return f"{float(value):.2f}"


    return str(value)


# --------------------------------------------------
# GET RISK FACTORS
# --------------------------------------------------

def get_risk_factors(
    applicant,
    top_n=5
):

    contributions = explain_prediction(
        applicant
    )

    ntc = (
        applicant.get(
            "ntc_flag",
            0
        ) == 1
    )

    risk_increasing = []

    risk_reducing = []


    # --------------------------------------------------
    # PROCESS SHAP CONTRIBUTIONS
    # --------------------------------------------------

    for item in contributions:

        feature = item[
            "feature"
        ]

        shap_value = item[
            "shap_value"
        ]


        # Ignore zero contribution
        if shap_value == 0:

            continue


        # --------------------------------------------------
        # GET ORIGINAL APPLICANT VALUE
        # --------------------------------------------------

        value = applicant.get(
            feature
        )


        # --------------------------------------------------
        # HUMAN-READABLE LABEL
        # --------------------------------------------------

        label = get_feature_description(
            feature,
            ntc=ntc
        )


        # --------------------------------------------------
        # HUMAN-READABLE VALUE
        # --------------------------------------------------

        value_display = format_feature_value(
            feature,
            value,
            applicant
        )


        # --------------------------------------------------
        # BUILD FACTOR
        # --------------------------------------------------

        factor = {

            "feature":
                feature,

            "label":
                label,

            "value":
                value,

            "value_display":
                value_display,

            "shap_value":
                round(
                    float(shap_value),
                    4
                ),

            "impact":
                round(
                    abs(shap_value),
                    4
                )
        }


        # --------------------------------------------------
        # DIRECTION
        # --------------------------------------------------

        if shap_value > 0:

            factor[
                "direction"
            ] = "increases_risk"

            risk_increasing.append(
                factor
            )

        else:

            factor[
                "direction"
            ] = "reduces_risk"

            risk_reducing.append(
                factor
            )


    # --------------------------------------------------
    # SORT FACTORS
    # --------------------------------------------------

    risk_increasing.sort(
        key=lambda x: x["impact"],
        reverse=True
    )

    risk_reducing.sort(
        key=lambda x: x["impact"],
        reverse=True
    )


    # --------------------------------------------------
    # RETURN
    # --------------------------------------------------

    return {

        "risk_increasing_factors":
            risk_increasing[
                :top_n
            ],

        "risk_reducing_factors":
            risk_reducing[
                :top_n
            ]
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    # --------------------------------------------------
    # HIGH-RISK NTC APPLICANT
    # --------------------------------------------------

    applicant = {

        "age": 24,

        "employment_type":
            "Contract",

        "employment_years":
            2,

        "monthly_income":
            25000,

        "loan_amount":
            600000,

        "loan_tenure_months":
            24,

        "existing_loans":
            0,

        "monthly_debt_payment":
            22000,

        "post_loan_dti":
            0.88,

        "credit_history_months":
            0,

        "credit_utilization":
            0,

        "repayment_consistency":
            65,

        "previous_missed_payments":
            0,

        "monthly_transactions":
            30,

        "average_transaction_amount":
            700,

        "ntc_flag":
            1
    }


    # --------------------------------------------------
    # GET RESULTS
    # --------------------------------------------------

    results = get_risk_factors(
        applicant
    )


    # --------------------------------------------------
    # PRINT RISK-INCREASING FACTORS
    # --------------------------------------------------

    print("\n==============================")
    print("RISK INCREASING FACTORS")
    print("==============================")


    for item in results[
        "risk_increasing_factors"
    ]:

        print(item)


    # --------------------------------------------------
    # PRINT RISK-REDUCING FACTORS
    # --------------------------------------------------

    print("\n==============================")
    print("RISK REDUCING FACTORS")
    print("==============================")


    for item in results[
        "risk_reducing_factors"
    ]:

        print(item)