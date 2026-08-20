from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.applicant import ApplicantRequest
from app.schemas.response import PredictionResponse

from app.services.prediction import predict_applicant
from app.services.explainability import get_risk_factors
from app.services.gemini import generate_risk_explanation
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth import (
    init_database,
    create_user,
    get_user_by_email,
    authenticate_user,
    create_access_token,
)



# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="Credit Risk Prediction API",
    description="API for the Credit Risk Prediction System",
    version="1.0.0"
)
init_database()


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Credit Risk API is running"
    }


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

@app.on_event("startup")
def startup():

    init_database()
@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(
    applicant: ApplicantRequest
):

    try:

        # ------------------------------------------
        # CONVERT REQUEST TO DICTIONARY
        # ------------------------------------------

        applicant_data = applicant.model_dump()


        # ------------------------------------------
        # MODEL PREDICTION
        # ------------------------------------------

        prediction = predict_applicant(
            applicant_data
        )


        # ------------------------------------------
        # SHAP EXPLANATION
        # ------------------------------------------

        risk_factors = get_risk_factors(
            applicant_data
        )


        # ------------------------------------------
        # GEMINI EXPLANATION
        # ------------------------------------------

        explanation = generate_risk_explanation(

            prediction[
                "probability_of_default"
            ],

            prediction[
                "decision"
            ],

            applicant_data,

            risk_factors[
                "risk_increasing_factors"
            ],

            risk_factors[
                "risk_reducing_factors"
            ]
        )


        # ------------------------------------------
        # COMBINE RESPONSE
        # ------------------------------------------

        response = {

            "probability_of_default":
                prediction[
                    "probability_of_default"
                ],

            "decision":
                prediction[
                    "decision"
                ],

            "risk_increasing_factors":
                risk_factors[
                    "risk_increasing_factors"
                ],

            "risk_reducing_factors":
                risk_factors[
                    "risk_reducing_factors"
                ],

            "explanation":
                explanation
        }


        return response


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post(
    "/auth/register",
    response_model=UserResponse
)
def register(
    user: UserCreate
):

    try:

        # ------------------------------------------
        # CHECK EXISTING USER
        # ------------------------------------------

        existing_user = (
            get_user_by_email(
                user.email
            )
        )


        if existing_user:

            raise HTTPException(
                status_code=400,
                detail=(
                    "An account with this email "
                    "already exists."
                )
            )


        # ------------------------------------------
        # CREATE USER
        # ------------------------------------------

        new_user = create_user(

            name=user.name,

            email=user.email,

            password=user.password,

        )


        return new_user


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# ==================================================
# LOGIN
# ==================================================

@app.post("/auth/login")
def login(
    user: UserLogin
):

    try:

        # ------------------------------------------
        # AUTHENTICATE USER
        # ------------------------------------------

        authenticated_user = authenticate_user(
            user.email,
            user.password
        )

        if not authenticated_user:

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )


        # ------------------------------------------
        # CREATE JWT
        # ------------------------------------------

        access_token = create_access_token(

            user_id=authenticated_user["id"],

            email=authenticated_user["email"]

        )


        # ------------------------------------------
        # RETURN RESPONSE
        # ------------------------------------------

        return {

            "access_token": access_token,

            "token_type": "bearer",

            "user": {

                "id":
                    authenticated_user["id"],

                "name":
                    authenticated_user["name"],

                "email":
                    authenticated_user["email"]

            }

        }


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )