from pydantic import BaseModel
from typing import List


class RiskFactor(BaseModel):

    feature: str
    label: str
    value: object | None = None
    value_display: str | None = None
    shap_value: float
    impact: float
    direction: str


class PredictionResponse(BaseModel):

    probability_of_default: float

    decision: str

    risk_increasing_factors: List[
        RiskFactor
    ]

    risk_reducing_factors: List[
        RiskFactor
    ]

    explanation: str