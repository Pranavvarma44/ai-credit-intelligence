import pandas as pd
import matplotlib.pyplot as plt
import os

# Load dataset
data = pd.read_csv(
    "credit_risk_dataset.csv"
)

# Create folder for plots
os.makedirs("plots", exist_ok=True)


# --------------------------------------------------
# 1. DEFAULT DISTRIBUTION
# --------------------------------------------------

data["default"].value_counts().sort_index().plot(
    kind="bar"
)

plt.title("Default Distribution")
plt.xlabel("Default")
plt.ylabel("Number of Applicants")
plt.xticks(
    [0, 1],
    ["Non-Default", "Default"],
    rotation=0
)

plt.tight_layout()

plt.savefig(
    "plots/default_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# --------------------------------------------------
# 2. POST-LOAN DTI
# --------------------------------------------------

data.boxplot(
    column="post_loan_dti",
    by="default"
)

plt.title("Post-Loan DTI by Default")
plt.suptitle("")
plt.xlabel("Default")
plt.ylabel("Post-Loan DTI")

plt.xticks(
    [1, 2],
    ["Non-Default", "Default"]
)

plt.tight_layout()

plt.savefig(
    "plots/dti_by_default.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# --------------------------------------------------
# 3. CREDIT UTILIZATION
# --------------------------------------------------

data.boxplot(
    column="credit_utilization",
    by="default"
)

plt.title("Credit Utilization by Default")
plt.suptitle("")
plt.xlabel("Default")
plt.ylabel("Credit Utilization (%)")

plt.xticks(
    [1, 2],
    ["Non-Default", "Default"]
)

plt.tight_layout()

plt.savefig(
    "plots/credit_utilization_by_default.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# --------------------------------------------------
# 4. PREVIOUS MISSED PAYMENTS
# --------------------------------------------------

data.boxplot(
    column="previous_missed_payments",
    by="default"
)

plt.title("Previous Missed Payments by Default")
plt.suptitle("")
plt.xlabel("Default")
plt.ylabel("Missed Payments")

plt.xticks(
    [1, 2],
    ["Non-Default", "Default"]
)

plt.tight_layout()

plt.savefig(
    "plots/missed_payments_by_default.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# --------------------------------------------------
# 5. CASH-FLOW STABILITY
# --------------------------------------------------

data.boxplot(
    column="cash_flow_stability",
    by="default"
)

plt.title("Cash-Flow Stability by Default")
plt.suptitle("")
plt.xlabel("Default")
plt.ylabel("Cash-Flow Stability")

plt.xticks(
    [1, 2],
    ["Non-Default", "Default"]
)

plt.tight_layout()

plt.savefig(
    "plots/cash_flow_stability_by_default.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


print("\nAll plots saved successfully!")
print("Location: plots/")