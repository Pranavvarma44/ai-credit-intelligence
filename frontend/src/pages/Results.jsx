import {
    AlertTriangle,
    CheckCircle2,
    ArrowLeft,
    TrendingUp,
    TrendingDown,
    Sparkles,
  } from "lucide-react";
  
  
  function formatFeatureName(feature) {
    const names = {
      previous_missed_payments: "Previous missed payments",
      repayment_consistency: "Repayment consistency",
      credit_utilization: "Credit utilization",
      spending_volatility: "Spending volatility",
      cash_flow_stability: "Cash-flow stability",
      income_stability: "Income stability",
      post_loan_dti: "Post-loan DTI",
      credit_history_months: "Credit history",
      employment_years: "Employment experience",
      age: "Age",
      loan_tenure_months: "Loan tenure",
      monthly_income: "Monthly income",
      existing_loans: "Existing loans",
      average_transaction_amount: "Average transaction amount",
      monthly_debt_payment: "Monthly debt payment",
      monthly_transactions: "Monthly transactions",
      employment_type_Salaried: "Salaried employment",
    };
  
    return names[feature] || feature;
  }
  
  
  function Results({ result, onBack }) {
  
    const probability =
      result.probability_of_default * 100;
  
    const isReview =
      result.decision === "Review";
  
    return (
      <main className="min-h-[calc(100vh-72px)]">
  
        <div className="mx-auto max-w-5xl px-6 py-12 lg:px-8">
  
  
          {/* BACK */}
  
          <button
            onClick={onBack}
            className="mb-8 flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-emerald-800"
          >
            <ArrowLeft size={16} />
            Back to applicant details
          </button>
  
  
          {/* HEADER */}
  
          <div className="mb-8">
  
            <p className="mb-2 text-xs font-bold tracking-[0.16em] text-emerald-700">
              RISK ASSESSMENT
            </p>
  
            <h1 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
              Assessment Results
            </h1>
  
            <p className="mt-2 text-sm text-slate-500">
              Prediction generated using the trained credit-risk model.
            </p>
  
          </div>
  
  
          {/* MAIN RESULT */}
  
          <section
            className={`mb-5 overflow-hidden rounded-2xl border p-7 ${
              isReview
                ? "border-amber-200 bg-amber-50/50"
                : "border-emerald-200 bg-emerald-50/50"
            }`}
          >
  
            <div className="flex flex-col gap-7 sm:flex-row sm:items-center sm:justify-between">
  
              <div>
  
                <p className="text-sm font-medium text-slate-500">
                  Probability of Default
                </p>
  
                <div className="mt-2 flex items-baseline gap-2">
  
                  <span className="text-5xl font-bold tracking-tight text-slate-950">
                    {probability.toFixed(2)}%
                  </span>
  
                </div>
  
                <p className="mt-2 text-sm text-slate-500">
                  Model-estimated probability of default.
                </p>
  
              </div>
  
  
              {/* DECISION */}
  
              <div
                className={`flex items-center gap-3 rounded-xl px-5 py-4 ${
                  isReview
                    ? "bg-amber-100 text-amber-800"
                    : "bg-emerald-100 text-emerald-800"
                }`}
              >
  
                {isReview ? (
                  <AlertTriangle size={25} />
                ) : (
                  <CheckCircle2 size={25} />
                )}
  
                <div>
  
                  <p className="text-xs font-medium opacity-70">
                    Decision
                  </p>
  
                  <p className="text-xl font-bold">
                    {result.decision}
                  </p>
  
                </div>
  
              </div>
  
            </div>
  
          </section>
  
  
          {/* FACTORS */}
  
          <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
  
  
            {/* RISK INCREASING */}
  
            <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
  
              <div className="mb-5 flex items-center gap-3">
  
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-red-50 text-red-600">
                  <TrendingUp size={18} />
                </div>
  
                <div>
                  <h2 className="font-semibold text-slate-900">
                    Factors Increasing Risk
                  </h2>
  
                  <p className="text-xs text-slate-400">
                    Strongest positive model influences
                  </p>
                </div>
  
              </div>
  
  
              <div className="space-y-3">
  
                {result.risk_increasing_factors.map(
                  (factor) => (
  
                    <div
                      key={factor.feature}
                      className="flex items-center justify-between rounded-xl bg-red-50/60 px-4 py-3"
                    >
  
                      <div className="flex items-center gap-3">
  
                        <TrendingUp
                          size={15}
                          className="text-red-500"
                        />
  
                        <span className="text-sm font-medium text-slate-700">
                          {formatFeatureName(
                            factor.feature
                          )}
                        </span>
  
                      </div>
  
                      <span className="text-xs font-semibold text-red-600">
                        +{factor.impact.toFixed(4)}
                      </span>
  
                    </div>
  
                  )
                )}
  
              </div>
  
            </section>
  
  
            {/* RISK REDUCING */}
  
            <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
  
              <div className="mb-5 flex items-center gap-3">
  
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
                  <TrendingDown size={18} />
                </div>
  
                <div>
                  <h2 className="font-semibold text-slate-900">
                    Factors Reducing Risk
                  </h2>
  
                  <p className="text-xs text-slate-400">
                    Factors that lowered the prediction
                  </p>
                </div>
  
              </div>
  
  
              <div className="space-y-3">
  
                {result.risk_reducing_factors.map(
                  (factor) => (
  
                    <div
                      key={factor.feature}
                      className="flex items-center justify-between rounded-xl bg-emerald-50/60 px-4 py-3"
                    >
  
                      <div className="flex items-center gap-3">
  
                        <TrendingDown
                          size={15}
                          className="text-emerald-600"
                        />
  
                        <span className="text-sm font-medium text-slate-700">
                          {formatFeatureName(
                            factor.feature
                          )}
                        </span>
  
                      </div>
  
                      <span className="text-xs font-semibold text-emerald-600">
                        -{factor.impact.toFixed(4)}
                      </span>
  
                    </div>
  
                  )
                )}
  
              </div>
  
            </section>
  
          </div>
  
  
          {/* GEMINI */}
  
          <section className="mt-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
  
            <div className="mb-5 flex items-center gap-3">
  
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-violet-50 text-violet-700">
                <Sparkles size={18} />
              </div>
  
              <div>
  
                <h2 className="font-semibold text-slate-900">
                  AI Explanation
                </h2>
  
                <p className="text-xs text-slate-400">
                  Explanation generated from the model's SHAP factors
                </p>
  
              </div>
  
            </div>
  
  
            <p className="text-sm leading-7 text-slate-600">
              {result.explanation}
            </p>
  
          </section>
  
        </div>
  
      </main>
    );
  }
  
  export default Results;