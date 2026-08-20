from pydantic import BaseModel


class ApplicantRequest(BaseModel):

    age: int
    employment_type: str
    employment_years: float

    monthly_income: float

    loan_amount: float
    loan_tenure_months: int
    existing_loans: int

    monthly_debt_payment: float
    post_loan_dti: float

    credit_history_months: int
    credit_utilization: float
    repayment_consistency: float
    previous_missed_payments: int

    monthly_transactions: int
    average_transaction_amount: float
    ntc_flag: int