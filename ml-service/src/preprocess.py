import pandas as pd
from sklearn.preprocessing import OneHotEncoder

NUMERICAL_FEATURES = [
    "age",
    "employment_years",
    "monthly_income",
    "loan_amount",
    "loan_tenure_months",
    "existing_loans",
    "monthly_debt_payment",
    "post_loan_dti",
    "credit_history_months",
    "credit_utilization",
    "repayment_consistency",
    "previous_missed_payments",
    "monthly_transactions",
    "average_transaction_amount",
    "spending_volatility",
    "cash_flow_stability",
    "income_stability"
]

CATEGORICAL_FEATURES = [
    "employment_type"
]


TARGET = "default"

def create_preprocessor():
    encoder=OneHotEncoder( handle_unknown="ignore",
        sparse_output=False)
    return encoder

def prepare_features(data,encoder=None,fit=False):
    numeric_data=data[NUMERICAL_FEATURES].copy()
    categorical_features=data[CATEGORICAL_FEATURES].copy()
    if fit:
        encoded=encoder.fit_transform(categorical_features)
    else:
        encoded=encoder.transform(categorical_features)
    encoded_columns=(encoder.get_feature_names_out(CATEGORICAL_FEATURES))
    encoded_data=pd.DataFrame(encoded,columns=encoded_columns,index=data.index)
    X=pd.concat([numeric_data,encoded_data],axis=1)
    return X
    
