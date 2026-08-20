import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured"
    )


client = genai.Client(
    api_key=API_KEY
)


def generate_risk_explanation(
    probability,
    decision,
    risk_increasing_factors,
    risk_reducing_factors
):

    prompt = f"""
You are explaining the result of a credit-risk machine learning model
to a user.

The machine learning model has already made the prediction and decision.
You must NOT change, override, or question the decision.

Probability of default:
{probability:.2%}

Decision:
{decision}

Risk-increasing factors identified by SHAP:
{risk_increasing_factors}

Risk-reducing factors identified by SHAP:
{risk_reducing_factors}

Write a concise, professional explanation in simple language.

Requirements:
1. State the probability and decision.
2. Explain the 2-3 most important factors that increased risk.
3. Explain the 1-2 most important factors that reduced risk.
4. Only use the information provided.
5. Do not invent applicant information.
6. Do not call SHAP values a "risk score".
7. Do not say a SHAP value is a percentage.
8. Do not provide financial advice.
9. Do not make a new prediction or change the decision.
10. Keep the explanation under 150 words.

Return only the explanation, without headings or markdown.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

if __name__ == "__main__":

    explanation = generate_risk_explanation(
        probability=0.6932,
        decision="Review",
        risk_increasing_factors=[
            {
                "feature": "previous_missed_payments",
                "impact": 1.0568,
                "direction": "increases_risk"
            },
            {
                "feature": "repayment_consistency",
                "impact": 0.5911,
                "direction": "increases_risk"
            },
            {
                "feature": "credit_utilization",
                "impact": 0.499,
                "direction": "increases_risk"
            }
        ],
        risk_reducing_factors=[
            {
                "feature": "credit_history_months",
                "impact": 0.0401,
                "direction": "reduces_risk"
            },
            {
                "feature": "employment_years",
                "impact": 0.0164,
                "direction": "reduces_risk"
            }
        ]
    )

    print("\n==============================")
    print("GEMINI EXPLANATION")
    print("==============================")
    print(explanation)