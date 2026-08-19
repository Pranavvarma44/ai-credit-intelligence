import pandas as pd
import os
from sklearn.model_selection import train_test_split
import joblib
from preprocess import ( 
    create_preprocessor,
    prepare_features,
    TARGET
)

data=pd.read_csv("credit_risk_dataset.csv")
train_data,test_data=train_test_split(data,test_size=0.2,random_state=42, stratify=data[TARGET])
encoder=create_preprocessor()

X_train=prepare_features(train_data,encoder=encoder,fit=True)
y_train=train_data[TARGET]

joblib.dump(
    encoder,
    "models/preprocessor.pkl"
)

X_test=prepare_features(test_data,encoder=encoder,fit=False)
y_test=test_data[TARGET]

os.makedirs("data",exist_ok=True)

train_data.to_csv("data/train.csv",index=False)
test_data.to_csv("data/test.csv",index=False)

X_train.to_csv(
    "data/X_train.csv",
    index=False
)

X_test.to_csv(
    "data/X_test.csv",
    index=False
)

y_train.to_csv(
    "data/y_train.csv",
    index=False
)

y_test.to_csv(
    "data/y_test.csv",
    index=False
)

demo_data = test_data.sample(
    n=10,
    random_state=42
)

demo_data.to_csv(
    "data/demo_applicants.csv",
    index=False
)

demo_data = test_data.sample(
    n=10,
    random_state=42
)

demo_data.to_csv(
    "data/demo_applicants.csv",
    index=False
)



# --------------------------------------------------
# 10. PRINT RESULTS
# --------------------------------------------------

print("\n==============================")
print("DATA SPLIT")
print("==============================")

print(
    "Total:",
    len(data)
)

print(
    "Training:",
    len(train_data)
)

print(
    "Testing:",
    len(test_data)
)


print("\n==============================")
print("TARGET DISTRIBUTION")
print("==============================")

print("\nFull dataset:")
print(
    data[TARGET].value_counts(
        normalize=True
    )
)

print("\nTraining:")
print(
    y_train.value_counts(
        normalize=True
    )
)

print("\nTesting:")
print(
    y_test.value_counts(
        normalize=True
    )
)


print("\n==============================")
print("PREPROCESSED SHAPES")
print("==============================")

print(
    "X_train:",
    X_train.shape
)

print(
    "y_train:",
    y_train.shape
)

print(
    "X_test:",
    X_test.shape
)

print(
    "y_test:",
    y_test.shape
)


print("\n==============================")
print("FEATURES")
print("==============================")

print(
    X_train.columns.tolist()
)


print("\n==============================")
print("FILES CREATED")
print("==============================")

print("data/train.csv")
print("data/test.csv")
print("data/X_train.csv")
print("data/X_test.csv")
print("data/y_train.csv")
print("data/y_test.csv")
print("data/demo_applicants.csv")