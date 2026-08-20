from pydantic import BaseModel

class RiskFactor(BaseModel):

    feature: str
    impact: float
    direction: str
class PredictionResponse(BaseModel):
   probability_of_default: float
   decision: str
   risk_increasing_factors: list[RiskFactor]
   risk_reducing_factors: list[RiskFactor]
   explanation: str