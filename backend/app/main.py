from fastapi import FastAPI
from app.schemas.applicant import ApplicantRequest
from app.schemas.response import PredictionResponse

from app.services.prediction import predict_applicant


app = FastAPI(
    title="Credit Risk Prediction API",
    description="API for the Credit Risk Prediction System",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Credit Risk API is running"
    }

@app.post("/predict",response_model=PredictionResponse)
def predict(applicant:ApplicantRequest):
    result=predict_applicant(applicant.model_dump())
    return result