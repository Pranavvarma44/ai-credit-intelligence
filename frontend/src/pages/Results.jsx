import {
    AlertTriangle,
    CheckCircle2,
    ArrowLeft,
    TrendingUp,
    TrendingDown,
    Sparkles,
    ShieldCheck,
    UserRound,
    Info,
    FlaskConical,
  } from "lucide-react";
  
  
  // --------------------------------------------------
  // RESULTS
  // --------------------------------------------------
  
  function Results({
    result,
    applicant,
    onBack,
    onWhatIf,
  }) {
  
    const probability =
      Number(
        result.probability_of_default || 0
      ) * 100;
  
  
    const isReview =
      result.decision === "Review";
  
  
    const isApproved =
      result.decision === "Approve";
  
  
    // --------------------------------------------------
    // NTC DETECTION
    // --------------------------------------------------
  
    const isNTC =
      Number(
        applicant?.ntc_flag
      ) === 1;
  
  
    // --------------------------------------------------
    // FORMAT SHAP IMPACT
    // --------------------------------------------------
  
    const formatImpact = (impact) => {
  
      const value =
        Number(impact || 0);
  
      return value.toFixed(4);
    };
  
  
    // --------------------------------------------------
    // RISK FACTOR
    // --------------------------------------------------
  
    const RiskFactor = ({
      factor,
      type,
    }) => {
  
      const increasing =
        type === "increasing";
  
  
      return (
        <div
          className={`group rounded-xl border p-4 transition ${
            increasing
              ? "border-red-100 bg-red-50/40 hover:border-red-200 hover:bg-red-50/70"
              : "border-emerald-100 bg-emerald-50/40 hover:border-emerald-200 hover:bg-emerald-50/70"
          }`}
        >
  
          <div className="flex items-start justify-between gap-4">
  
  
            {/* LEFT */}
  
            <div className="flex min-w-0 items-start gap-3">
  
              <div
                className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${
                  increasing
                    ? "bg-red-100 text-red-600"
                    : "bg-emerald-100 text-emerald-700"
                }`}
              >
  
                {increasing ? (
                  <TrendingUp size={15} />
                ) : (
                  <TrendingDown size={15} />
                )}
  
              </div>
  
  
              <div className="min-w-0">
  
                <p className="text-sm font-semibold text-slate-800">
  
                  {factor.label ||
                    formatFeatureName(
                      factor.feature
                    )}
  
                </p>
  
  
                {factor.value_display && (
  
                  <p className="mt-1 text-xs text-slate-500">
  
                    Applicant value:{" "}
  
                    <span className="font-medium text-slate-700">
  
                      {factor.value_display}
  
                    </span>
  
                  </p>
  
                )}
  
              </div>
  
            </div>
  
  
            {/* IMPACT */}
  
            <div
              className={`shrink-0 text-right ${
                increasing
                  ? "text-red-600"
                  : "text-emerald-700"
              }`}
            >
  
              <p className="text-xs font-medium opacity-70">
                Impact
              </p>
  
              <p className="text-sm font-bold">
  
                {increasing ? "+" : "-"}
  
                {formatImpact(
                  factor.impact
                )}
  
              </p>
  
            </div>
  
          </div>
  
        </div>
      );
    };
  
  
    // --------------------------------------------------
    // RENDER
    // --------------------------------------------------
  
    return (
  
      <main className="min-h-[calc(100vh-72px)] bg-slate-50">
  
        <div className="mx-auto max-w-5xl px-6 py-10 lg:px-8 lg:py-14">
  
  
          {/* ==================================================
              BACK
          ================================================== */}
  
          <button
            onClick={onBack}
            className="mb-8 flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-emerald-800"
          >
  
            <ArrowLeft size={16} />
  
            Back to applicant details
  
          </button>
  
  
          {/* ==================================================
              HEADER
          ================================================== */}
  
          <div className="mb-8">
  
            <div className="mb-4 flex items-center gap-2">
  
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-100">
  
                <ShieldCheck
                  size={17}
                  className="text-emerald-700"
                />
  
              </div>
  
  
              <p className="text-xs font-bold tracking-[0.16em] text-emerald-700">
  
                RISK ASSESSMENT
  
              </p>
  
            </div>
  
  
            <h1 className="text-3xl font-bold tracking-[-0.03em] text-slate-950 sm:text-4xl">
  
              Assessment Results
  
            </h1>
  
  
            <p className="mt-2 text-sm text-slate-500">
  
              Your application has been evaluated using the
              trained credit-risk model.
  
            </p>
  
          </div>
  
  
          {/* ==================================================
              MAIN RESULT
          ================================================== */}
  
          <section
            className={`relative mb-5 overflow-hidden rounded-2xl border p-7 shadow-sm ${
              isReview
                ? "border-amber-200 bg-gradient-to-br from-amber-50 to-white"
                : "border-emerald-200 bg-gradient-to-br from-emerald-50 to-white"
            }`}
          >
  
            <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
  
  
              {/* PROBABILITY */}
  
              <div>
  
                <div className="flex items-center gap-2">
  
                  <p className="text-sm font-semibold text-slate-500">
  
                    Probability of Default
  
                  </p>
  
  
                  <div className="group relative">
  
                    <Info
                      size={14}
                      className="cursor-help text-slate-400"
                    />
  
                  </div>
  
                </div>
  
  
                <div className="mt-2 flex items-baseline gap-2">
  
                  <span className="text-5xl font-bold tracking-tight text-slate-950">
  
                    {probability.toFixed(2)}%
  
                  </span>
  
                </div>
  
  
                <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">
  
                  Estimated probability that the applicant
                  may default based on the model's assessment.
  
                </p>
  
              </div>
  
  
              {/* DECISION */}
  
              <div
                className={`flex min-w-[210px] items-center gap-4 rounded-2xl px-5 py-5 ${
                  isReview
                    ? "bg-amber-100 text-amber-900"
                    : "bg-emerald-100 text-emerald-900"
                }`}
              >
  
                <div
                  className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl ${
                    isReview
                      ? "bg-amber-200"
                      : "bg-emerald-200"
                  }`}
                >
  
                  {isReview ? (
                    <AlertTriangle size={23} />
                  ) : (
                    <CheckCircle2 size={23} />
                  )}
  
                </div>
  
  
                <div>
  
                  <p className="text-xs font-semibold uppercase tracking-wide opacity-60">
  
                    Decision
  
                  </p>
  
  
                  <p className="mt-0.5 text-2xl font-bold">
  
                    {result.decision}
  
                  </p>
  
  
                  <p className="mt-1 text-xs opacity-70">
  
                    {isReview
                      ? "Additional assessment required"
                      : "Eligible for automatic approval"}
  
                  </p>
  
                </div>
  
              </div>
  
            </div>
  
  
            {/* NTC BADGE */}
  
            {isNTC && (
  
              <div className="mt-7 flex items-start gap-3 rounded-xl border border-amber-200 bg-white/70 px-4 py-3">
  
                <UserRound
                  size={17}
                  className="mt-0.5 shrink-0 text-amber-700"
                />
  
  
                <div>
  
                  <p className="text-sm font-semibold text-slate-800">
  
                    New to Credit (NTC)
  
                  </p>
  
  
                  <p className="mt-1 text-xs leading-5 text-slate-500">
  
                    No established formal credit history is
                    available. The assessment therefore relies
                    more heavily on current financial information.
  
                  </p>
  
                </div>
  
              </div>
  
            )}
  
          </section>
  
  
          {/* ==================================================
              WHAT-IF ANALYSIS
          ================================================== */}
  
          <button
            onClick={onWhatIf}
            className="group mb-5 flex w-full items-center justify-between rounded-2xl border border-violet-200 bg-gradient-to-r from-violet-50/80 to-white px-6 py-4 text-left shadow-sm transition hover:border-violet-300 hover:shadow-md"
          >
  
            <div className="flex items-center gap-4">
  
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-violet-100 text-violet-700 transition group-hover:bg-violet-200">
  
                <FlaskConical size={20} />
  
              </div>
  
  
              <div>
  
                <p className="font-semibold text-slate-900">
  
                  Explore What-If Scenarios
  
                </p>
  
  
                <p className="mt-1 text-xs leading-5 text-slate-500">
  
                  Change loan amount, income, interest rate,
                  or tenure and see how the risk changes.
  
                </p>
  
              </div>
  
            </div>
  
  
            <div className="flex items-center gap-2 text-sm font-semibold text-violet-700">
  
              Explore
  
              <span className="transition-transform group-hover:translate-x-1">
  
                →
  
              </span>
  
            </div>
  
          </button>
  
  
          {/* ==================================================
              MODEL FACTORS
          ================================================== */}
  
          <div className="mb-5 grid grid-cols-1 gap-5 lg:grid-cols-2">
  
  
            {/* ==================================================
                RISK INCREASING
            ================================================== */}
  
            <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
  
              <div className="mb-5 flex items-start justify-between">
  
                <div className="flex items-center gap-3">
  
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-red-50 text-red-600">
  
                    <TrendingUp size={18} />
  
                  </div>
  
  
                  <div>
  
                    <h2 className="font-semibold text-slate-900">
  
                      Factors Increasing Risk
  
                    </h2>
  
  
                    <p className="mt-0.5 text-xs text-slate-400">
  
                      Factors pushing the prediction toward higher risk
  
                    </p>
  
                  </div>
  
                </div>
  
              </div>
  
  
              <div className="space-y-3">
  
                {result.risk_increasing_factors?.length ? (
  
                  result.risk_increasing_factors.map(
                    (factor) => (
  
                      <RiskFactor
                        key={factor.feature}
                        factor={factor}
                        type="increasing"
                      />
  
                    )
                  )
  
                ) : (
  
                  <p className="rounded-xl bg-slate-50 p-4 text-sm text-slate-500">
  
                    No significant risk-increasing factors identified.
  
                  </p>
  
                )}
  
              </div>
  
            </section>
  
  
            {/* ==================================================
                RISK REDUCING
            ================================================== */}
  
            <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
  
              <div className="mb-5 flex items-start gap-3">
  
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
  
                  <TrendingDown size={18} />
  
                </div>
  
  
                <div>
  
                  <h2 className="font-semibold text-slate-900">
  
                    Factors Reducing Risk
  
                  </h2>
  
  
                  <p className="mt-0.5 text-xs text-slate-400">
  
                    Factors pushing the prediction toward lower risk
  
                  </p>
  
                </div>
  
              </div>
  
  
              <div className="space-y-3">
  
                {result.risk_reducing_factors?.length ? (
  
                  result.risk_reducing_factors.map(
                    (factor) => (
  
                      <RiskFactor
                        key={factor.feature}
                        factor={factor}
                        type="reducing"
                      />
  
                    )
                  )
  
                ) : (
  
                  <p className="rounded-xl bg-slate-50 p-4 text-sm text-slate-500">
  
                    No significant risk-reducing factors identified.
  
                  </p>
  
                )}
  
              </div>
  
            </section>
  
          </div>
  
  
          {/* ==================================================
              AI EXPLANATION
          ================================================== */}
  
          <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
  
  
            {/* AI HEADER */}
  
            <div className="border-b border-slate-100 bg-gradient-to-r from-violet-50/70 to-white px-6 py-5">
  
              <div className="flex items-center gap-3">
  
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-100 text-violet-700">
  
                  <Sparkles size={19} />
  
                </div>
  
  
                <div>
  
                  <div className="flex items-center gap-2">
  
                    <h2 className="font-semibold text-slate-900">
  
                      AI Explanation
  
                    </h2>
  
  
                    <span className="rounded-full bg-violet-100 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-violet-700">
  
                      Gemini
  
                    </span>
  
                  </div>
  
  
                  <p className="mt-0.5 text-xs text-slate-400">
  
                    A plain-language explanation based on the model's
                    prediction and SHAP factors.
  
                  </p>
  
                </div>
  
              </div>
  
            </div>
  
  
            {/* AI CONTENT */}
  
            <div className="px-6 py-6">
  
              <div className="prose prose-sm max-w-none prose-headings:text-slate-900 prose-p:text-slate-600 prose-p:leading-7 prose-li:text-slate-600">
  
                {formatExplanation(
                  result.explanation
                )}
  
              </div>
  
            </div>
  
          </section>
  
  
          {/* ==================================================
              FOOTER NOTE
          ================================================== */}
  
          <div className="mt-5 flex items-start gap-3 rounded-xl border border-slate-200 bg-white px-5 py-4">
  
            <ShieldCheck
              size={17}
              className="mt-0.5 shrink-0 text-emerald-600"
            />
  
  
            <p className="text-xs leading-5 text-slate-500">
  
              This assessment is generated by a machine-learning
              model and is intended to support the lending review
              process. A "Review" decision does not represent a
              final rejection.
  
            </p>
  
          </div>
  
  
        </div>
  
      </main>
    );
  }
  
  
  // --------------------------------------------------
  // FORMAT FEATURE NAME
  // --------------------------------------------------
  
  function formatFeatureName(feature) {
  
    const names = {
  
      previous_missed_payments:
        "Previous missed payments",
  
      repayment_consistency:
        "Repayment consistency",
  
      credit_utilization:
        "Credit utilization",
  
      post_loan_dti:
        "Post-loan DTI",
  
      credit_history_months:
        "Credit history",
  
      employment_years:
        "Employment experience",
  
      age:
        "Age",
  
      loan_tenure_months:
        "Loan tenure",
  
      monthly_income:
        "Monthly income",
  
      existing_loans:
        "Existing loans",
  
      average_transaction_amount:
        "Average transaction amount",
  
      monthly_debt_payment:
        "Monthly debt payment",
  
      monthly_transactions:
        "Monthly transactions",
  
      loan_amount:
        "Requested loan amount",
  
      employment_type_Salaried:
        "Salaried employment",
  
      employment_type_Contract:
        "Contract employment",
  
      employment_type_Self_Employed:
        "Self-employed",
  
      ntc_flag:
        "New-to-credit status",
    };
  
  
    return (
      names[feature] ||
      feature
    );
  }
  
  
  // --------------------------------------------------
  // FORMAT GEMINI MARKDOWN
  // --------------------------------------------------
  
  function formatExplanation(text) {
  
    if (!text) {
  
      return (
        <p>
          No AI explanation was returned.
        </p>
      );
    }
  
  
    const lines =
      text.split("\n");
  
  
    return lines.map(
      (line, index) => {
  
        const trimmed =
          line.trim();
  
  
        if (!trimmed) {
  
          return (
            <div
              key={index}
              className="h-3"
            />
          );
        }
  
  
        // Heading
  
        if (
          trimmed.startsWith("### ")
        ) {
  
          return (
            <h3
              key={index}
              className="mb-2 mt-5 text-base font-bold text-slate-900 first:mt-0"
            >
  
              {trimmed.replace(
                "### ",
                ""
              )}
  
            </h3>
          );
        }
  
  
        // Bullet
  
        if (
          trimmed.startsWith("* ")
        ) {
  
          return (
            <div
              key={index}
              className="mb-2 flex gap-2"
            >
  
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-600" />
  
  
              <p>
  
                {formatBoldText(
                  trimmed.substring(2)
                )}
  
              </p>
  
            </div>
          );
        }
  
  
        // Separator
  
        if (
          trimmed === "---"
        ) {
  
          return (
            <hr
              key={index}
              className="my-5 border-slate-100"
            />
          );
        }
  
  
        return (
          <p
            key={index}
            className="mb-3"
          >
  
            {formatBoldText(
              trimmed
            )}
  
          </p>
        );
  
      }
    );
  }
  
  
  // --------------------------------------------------
  // FORMAT BOLD TEXT
  // --------------------------------------------------
  
  function formatBoldText(text) {
  
    const parts =
      text.split(
        /(\*\*.*?\*\*)/g
      );
  
  
    return parts.map(
      (part, index) => {
  
        if (
          part.startsWith("**") &&
          part.endsWith("**")
        ) {
  
          return (
            <strong
              key={index}
              className="font-semibold text-slate-800"
            >
  
              {part.slice(
                2,
                -2
              )}
  
            </strong>
          );
        }
  
  
        return part;
      }
    );
  }
  
  
  export default Results;