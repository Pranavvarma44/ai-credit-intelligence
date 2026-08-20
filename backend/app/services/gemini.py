import os

from google import genai
from dotenv import load_dotenv


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# GENERATE RISK EXPLANATION
# --------------------------------------------------

def generate_risk_explanation(
    probability,
    decision,
    applicant,
    risk_increasing_factors,
    risk_reducing_factors
):

    # --------------------------------------------------
    # NTC CHECK
    # --------------------------------------------------

    ntc = (
        applicant.get(
            "ntc_flag",
            0
        ) == 1
    )


    # --------------------------------------------------
    # CREDIT CONTEXT
    # --------------------------------------------------

    if ntc:

        credit_context = """
The applicant is NEW TO CREDIT (NTC).

This means the applicant does not have an established formal
credit history.

For an NTC applicant:

- credit_history_months = 0 means there is no previous formal
  credit history available.

- credit_utilization = 0 means there is no previous revolving
  credit utilization information available.

- previous_missed_payments = 0 means there is no previous formal
  repayment history from which missed payments can be evaluated.

- repayment_consistency does NOT represent an established formal
  credit repayment history.

IMPORTANT:
Do NOT describe these zero values as evidence of excellent credit
behavior or responsible repayment.

Instead, explain that historical credit information is unavailable
because the applicant is new to credit.

Focus primarily on current financial information such as:
income, loan amount, post-loan DTI, employment, debt burden,
transaction activity, and affordability.
"""

    else:

        credit_context = """
The applicant has an established credit history.

Credit history, credit utilization, previous missed payments,
and repayment consistency can therefore be interpreted as
historical credit behavior when relevant.
"""


    # --------------------------------------------------
    # DECISION CONTEXT
    # --------------------------------------------------

    if decision == "Review":

        decision_context = """
The application has been classified as REVIEW.

Review does NOT mean automatic rejection.

It means the application has crossed the model's review threshold
and requires additional assessment before a final lending decision.
"""

    else:

        decision_context = """
The application has been classified as APPROVE.

Approve means the predicted risk is below the model's review
threshold. Do not describe this as a guarantee that the applicant
will repay the loan.
"""


    # --------------------------------------------------
    # PROMPT
    # --------------------------------------------------

    prompt = f"""
You are an AI assistant explaining a credit-risk assessment
to a loan applicant.

Your explanation must be clear, concise, professional, neutral,
and easy for a non-technical person to understand.

{credit_context}

{decision_context}

IMPORTANT RULES:

1. Do not change or contradict the model's decision.

2. Do not invent applicant information.

3. Use the provided risk factors as the primary basis for the
   explanation.

4. Explain SHAP factors as factors that contributed toward or
   away from the model's assessed risk.

5. Do NOT say that a SHAP value represents a percentage change
   in default probability.

6. Do not mention SHAP, machine learning, algorithms, feature
   engineering, or other technical implementation details.

7. Do not provide financial advice.

8. Do not say that the applicant will definitely default.

9. Do not exaggerate the importance of a factor.

10. Focus on the strongest 2-4 risk-increasing factors and
    strongest 2-3 risk-reducing factors.

11. Avoid repeating the same information in multiple sections.

12. Keep the explanation concise. Aim for approximately
    250-350 words maximum.

13. Use actual applicant values when they make the explanation
    clearer.

14. If the applicant is NTC, clearly distinguish between
    "no negative credit history" and "no credit history available."

15. For NTC applicants, do NOT describe zero missed payments,
    zero credit utilization, or zero credit history as evidence
    of good credit behavior.

16. Do not expose internal model thresholds or technical
    implementation details.


--------------------------------------------------
APPLICANT INFORMATION
--------------------------------------------------

Age: {applicant.get("age")}

Employment type:
{applicant.get("employment_type")}

Employment years:
{applicant.get("employment_years")}

Monthly income:
{applicant.get("monthly_income")}

Loan amount:
{applicant.get("loan_amount")}

Loan tenure:
{applicant.get("loan_tenure_months")} months

Existing loans:
{applicant.get("existing_loans")}

Monthly debt payment:
{applicant.get("monthly_debt_payment")}

Post-loan DTI:
{applicant.get("post_loan_dti")}

Credit history:
{applicant.get("credit_history_months")} months

Credit utilization:
{applicant.get("credit_utilization")}

Repayment consistency:
{applicant.get("repayment_consistency")}

Previous missed payments:
{applicant.get("previous_missed_payments")}

Monthly transactions:
{applicant.get("monthly_transactions")}

Average transaction amount:
{applicant.get("average_transaction_amount")}

NTC status:
{"New to Credit" if ntc else "Established Credit History"}


--------------------------------------------------
MODEL RESULT
--------------------------------------------------

Probability of default:
{probability:.2%}

Decision:
{decision}


--------------------------------------------------
RISK-INCREASING FACTORS
--------------------------------------------------

{risk_increasing_factors}


--------------------------------------------------
RISK-REDUCING FACTORS
--------------------------------------------------

{risk_reducing_factors}


--------------------------------------------------
REQUIRED RESPONSE FORMAT
--------------------------------------------------

Use exactly these four sections:

### Decision Summary

Briefly explain the decision and estimated probability of default.

### Key Risk Factors

Explain the most important factors that increased the assessed risk.
Use actual values where useful.

### Positive Factors

Explain the most important factors that helped reduce the assessed
risk.

### Credit History

If the applicant is NTC, clearly explain that there is no established
formal credit history and that this means historical credit behavior
cannot be evaluated.

If the applicant has an established credit history, briefly explain
the relevant available credit-history information.

Do not add additional sections.

Do not use a disclaimer at the end.

Keep the tone professional, clear, and applicant-friendly.
"""


    # --------------------------------------------------
    # GEMINI REQUEST
    # --------------------------------------------------

    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=prompt
    )


    # --------------------------------------------------
    # RETURN
    # --------------------------------------------------

    return response.text


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    applicant = {

        "age": 24,

        "employment_type":
            "Salaried",

        "employment_years":
            3,

        "monthly_income":
            60000,

        "loan_amount":
            150000,

        "loan_tenure_months":
            36,

        "existing_loans":
            0,

        "monthly_debt_payment":
            4167,

        "post_loan_dti":
            0.0694,

        "credit_history_months":
            0,

        "credit_utilization":
            0,

        "repayment_consistency":
            100,

        "previous_missed_payments":
            0,

        "monthly_transactions":
            45,

        "average_transaction_amount":
            900,

        "ntc_flag":
            1
    }


    explanation = generate_risk_explanation(

        probability=0.0099,

        decision="Approve",

        applicant=applicant,

        risk_increasing_factors=[

            {
                "feature":
                    "age",

                "impact":
                    0.0452,

                "direction":
                    "increases_risk"
            },

            {
                "feature":
                    "employment_years",

                "impact":
                    0.0378,

                "direction":
                    "increases_risk"
            }
        ],

        risk_reducing_factors=[

            {
                "feature":
                    "post_loan_dti",

                "impact":
                    0.4944,

                "direction":
                    "reduces_risk"
            },

            {
                "feature":
                    "repayment_consistency",

                "impact":
                    0.335,

                "direction":
                    "reduces_risk"
            }
        ]
    )


    print("\n==============================")
    print("GEMINI EXPLANATION")
    print("==============================")

    print(explanation)