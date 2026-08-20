import { useState } from "react";
import {
  ArrowLeft,
  FlaskConical,
  TrendingDown,
  TrendingUp,
  RefreshCcw,
  IndianRupee,
  Percent,
  CalendarDays,
  Wallet,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";


// --------------------------------------------------
// EMI CALCULATION
// --------------------------------------------------
const API_URL = import.meta.env.VITE_API_URL;
function calculateEMI(
  principal,
  annualRate,
  tenureMonths
) {

  if (
    !principal ||
    !annualRate ||
    !tenureMonths
  ) {
    return 0;
  }

  const monthlyRate =
    annualRate / 12 / 100;

  const emi =
    principal *
    monthlyRate *
    Math.pow(
      1 + monthlyRate,
      tenureMonths
    ) /
    (
      Math.pow(
        1 + monthlyRate,
        tenureMonths
      ) - 1
    );

  return emi;
}


// --------------------------------------------------
// FORMAT CURRENCY
// --------------------------------------------------

function formatCurrency(value) {
  return new Intl.NumberFormat(
    "en-IN",
    {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }
  ).format(value);
}


// --------------------------------------------------
// WHAT IF PAGE
// --------------------------------------------------

function WhatIf({
  applicant,
  result,
  onBack,
}) {

  // ------------------------------------------------
  // INITIAL VALUES
  // ------------------------------------------------

  const initialEMI = calculateEMI(
    applicant.loan_amount,
    applicant.interest_rate,
    applicant.loan_tenure_months
  );


  // ------------------------------------------------
  // STATE
  // ------------------------------------------------

  const [
    loanAmount,
    setLoanAmount,
  ] = useState(
    applicant.loan_amount
  );


  const [
    interestRate,
    setInterestRate,
  ] = useState(
    applicant.interest_rate
  );


  const [
    loanTenure,
    setLoanTenure,
  ] = useState(
    applicant.loan_tenure_months
  );


  const [
    monthlyIncome,
    setMonthlyIncome,
  ] = useState(
    applicant.monthly_income
  );


  const [
    existingDebt,
    setExistingDebt,
  ] = useState(
    applicant.existing_monthly_debt_payment || 0
  );


  const [
    scenarioResult,
    setScenarioResult,
  ] = useState(null);


  const [
    loading,
    setLoading,
  ] = useState(false);


  const [
    error,
    setError,
  ] = useState("");


  // ------------------------------------------------
  // CALCULATE CURRENT SCENARIO
  // ------------------------------------------------

  const currentEMI =
    initialEMI;


  const currentDTI =
    applicant.post_loan_dti;


  // ------------------------------------------------
  // CALCULATE WHAT-IF VALUES
  // ------------------------------------------------

  const scenarioEMI =
    calculateEMI(
      Number(loanAmount),
      Number(interestRate),
      Number(loanTenure)
    );


  const scenarioTotalDebt =
    Number(existingDebt) +
    scenarioEMI;


  const scenarioDTI =
    monthlyIncome > 0
      ? scenarioTotalDebt /
        Number(monthlyIncome)
      : 0;


  // ------------------------------------------------
  // RUN WHAT-IF
  // ------------------------------------------------

  async function runWhatIf() {

    setLoading(true);
    setError("");

    try {

      const updatedApplicant = {

        ...applicant,

        loan_amount:
          Number(loanAmount),

        interest_rate:
          Number(interestRate),

        loan_tenure_months:
          Number(loanTenure),

        monthly_income:
          Number(monthlyIncome),

        existing_monthly_debt_payment:
          Number(existingDebt),

        monthly_debt_payment:
          Math.round(
            scenarioTotalDebt
          ),

        post_loan_dti:
          Number(
            scenarioDTI.toFixed(4)
          ),
      };


      const response =
        await fetch(
            `${API_URL}/predict`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body:
              JSON.stringify(
                updatedApplicant
              ),
          }
        );


      if (!response.ok) {

        const errorData =
          await response.json();

        throw new Error(
          errorData.detail ||
          "Unable to run what-if analysis"
        );
      }


      const data =
        await response.json();


      setScenarioResult({
        ...data,

        applicant:
          updatedApplicant,

        emi:
          scenarioEMI,

        dti:
          scenarioDTI,
      });

    } catch (err) {

      console.error(err);

      setError(
        err.message ||
        "Something went wrong."
      );

    } finally {

      setLoading(false);

    }
  }


  // ------------------------------------------------
  // RESET
  // ------------------------------------------------

  function resetScenario() {

    setLoanAmount(
      applicant.loan_amount
    );

    setInterestRate(
      applicant.interest_rate
    );

    setLoanTenure(
      applicant.loan_tenure_months
    );

    setMonthlyIncome(
      applicant.monthly_income
    );

    setExistingDebt(
      applicant.existing_monthly_debt_payment || 0
    );

    setScenarioResult(null);

    setError("");
  }


  // ------------------------------------------------
  // PROBABILITY COMPARISON
  // ------------------------------------------------

  const currentProbability =
    Number(
      result.probability_of_default
    ) * 100;


  const scenarioProbability =
    scenarioResult
      ? Number(
          scenarioResult
            .probability_of_default
        ) * 100
      : null;


  const probabilityChange =
    scenarioResult
      ? scenarioProbability -
        currentProbability
      : null;


  const riskImproved =
    probabilityChange < 0;


  // ------------------------------------------------
  // RENDER
  // ------------------------------------------------

  return (

    <main className="min-h-[calc(100vh-72px)] bg-slate-50">

      <div className="mx-auto max-w-6xl px-6 py-10 lg:px-8 lg:py-14">


        {/* ==========================================
            BACK
        ========================================== */}

        <button
          onClick={onBack}
          className="mb-8 flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-emerald-800"
        >

          <ArrowLeft size={16} />

          Back to assessment

        </button>


        {/* ==========================================
            HEADER
        ========================================== */}

        <div className="mb-8">

          <div className="mb-4 flex items-center gap-2">

            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-violet-100">

              <FlaskConical
                size={18}
                className="text-violet-700"
              />

            </div>


            <p className="text-xs font-bold tracking-[0.16em] text-violet-700">

              WHAT-IF ANALYSIS

            </p>

          </div>


          <h1 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">

            Explore Different Scenarios

          </h1>


          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">

            Adjust the applicant's financial details to
            see how changes could affect the model's
            risk assessment.

          </p>

        </div>


        {/* ==========================================
            CURRENT VS SCENARIO
        ========================================== */}

        <div className="mb-5 grid grid-cols-1 gap-5 lg:grid-cols-2">


          {/* CURRENT */}

          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

            <div className="mb-5">

              <p className="text-xs font-bold tracking-wider text-slate-400">

                CURRENT ASSESSMENT

              </p>

              <h2 className="mt-1 text-lg font-semibold text-slate-900">

                Existing application

              </h2>

            </div>


            <div className="grid grid-cols-2 gap-4">

              <Metric
                label="Default probability"
                value={`${currentProbability.toFixed(2)}%`}
              />

              <Metric
                label="Decision"
                value={result.decision}
                decision={result.decision}
              />

              <Metric
                label="Loan amount"
                value={formatCurrency(
                  applicant.loan_amount
                )}
              />

              <Metric
                label="Post-loan DTI"
                value={`${(
                  currentDTI * 100
                ).toFixed(1)}%`}
              />

            </div>

          </section>


          {/* WHAT IF */}

          <section className="rounded-2xl border border-violet-200 bg-violet-50/40 p-6 shadow-sm">

            <div className="mb-5">

              <p className="text-xs font-bold tracking-wider text-violet-600">

                WHAT-IF SCENARIO

              </p>

              <h2 className="mt-1 text-lg font-semibold text-slate-900">

                Modified application

              </h2>

            </div>


            <div className="grid grid-cols-2 gap-4">

              <Metric
                label="Default probability"
                value={
                  scenarioResult
                    ? `${scenarioProbability.toFixed(2)}%`
                    : "—"
                }
              />

              <Metric
                label="Decision"
                value={
                  scenarioResult
                    ? scenarioResult.decision
                    : "—"
                  }
                decision={
                  scenarioResult?.decision
                }
              />

              <Metric
                label="Loan amount"
                value={formatCurrency(
                  Number(loanAmount)
                )}
              />

              <Metric
                label="Post-loan DTI"
                value={`${(
                  scenarioDTI * 100
                ).toFixed(1)}%`}
              />

            </div>

          </section>

        </div>


        {/* ==========================================
            CONTROLS + RESULT
        ========================================== */}

        <div className="grid grid-cols-1 gap-5 lg:grid-cols-[1.05fr_0.95fr]">


          {/* ========================================
              CONTROLS
          ======================================== */}

          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

            <div className="mb-6">

              <h2 className="font-semibold text-slate-900">

                Scenario Controls

              </h2>

              <p className="mt-1 text-xs text-slate-400">

                Change the values below and run the
                model again.

              </p>

            </div>


            <div className="space-y-6">


              {/* LOAN AMOUNT */}

              <SliderField
                label="Loan amount"
                value={loanAmount}
                min={25000}
                max={2000000}
                step={5000}
                display={formatCurrency(
                  Number(loanAmount)
                )}
                icon={
                  <IndianRupee size={16} />
                }
                onChange={
                  setLoanAmount
                }
              />


              {/* INTEREST RATE */}

              <SliderField
                label="Interest rate"
                value={interestRate}
                min={6}
                max={24}
                step={0.5}
                display={`${Number(
                  interestRate
                ).toFixed(1)}%`}
                icon={
                  <Percent size={16} />
                }
                onChange={
                  setInterestRate
                }
              />


              {/* TENURE */}

              <SliderField
                label="Loan tenure"
                value={loanTenure}
                min={6}
                max={84}
                step={6}
                display={`${loanTenure} months`}
                icon={
                  <CalendarDays size={16} />
                }
                onChange={
                  setLoanTenure
                }
              />


              {/* INCOME */}

              <SliderField
                label="Monthly income"
                value={monthlyIncome}
                min={15000}
                max={500000}
                step={5000}
                display={formatCurrency(
                  Number(monthlyIncome)
                )}
                icon={
                  <Wallet size={16} />
                }
                onChange={
                  setMonthlyIncome
                }
              />


              {/* EXISTING DEBT */}

              <SliderField
                label="Existing monthly debt"
                value={existingDebt}
                min={0}
                max={100000}
                step={1000}
                display={formatCurrency(
                  Number(existingDebt)
                )}
                icon={
                  <Wallet size={16} />
                }
                onChange={
                  setExistingDebt
                }
              />


              {/* DERIVED VALUES */}

              <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">

                <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400">

                  Calculated values

                </p>


                <div className="grid grid-cols-2 gap-4">

                  <div>

                    <p className="text-xs text-slate-400">

                      Estimated EMI

                    </p>

                    <p className="mt-1 text-sm font-bold text-slate-800">

                      {formatCurrency(
                        scenarioEMI
                      )}

                    </p>

                  </div>


                  <div>

                    <p className="text-xs text-slate-400">

                      Post-loan DTI

                    </p>

                    <p
                      className={`mt-1 text-sm font-bold ${
                        scenarioDTI >= 0.7
                          ? "text-red-600"
                          : scenarioDTI >= 0.5
                          ? "text-amber-600"
                          : "text-emerald-600"
                      }`}
                    >

                      {(
                        scenarioDTI * 100
                      ).toFixed(1)}%

                    </p>

                  </div>

                </div>

              </div>


              {/* ERROR */}

              {error && (

                <div className="flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-4">

                  <AlertTriangle
                    size={17}
                    className="mt-0.5 shrink-0 text-red-600"
                  />

                  <p className="text-sm text-red-700">

                    {error}

                  </p>

                </div>

              )}


              {/* BUTTONS */}

              <div className="flex gap-3 pt-2">

                <button
                  onClick={runWhatIf}
                  disabled={loading}
                  className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:opacity-50"
                >

                  {loading ? (

                    <>
                      <RefreshCcw
                        size={16}
                        className="animate-spin"
                      />

                      Running model...

                    </>

                  ) : (

                    <>
                      <FlaskConical size={16} />

                      Run What-If Analysis

                    </>

                  )}

                </button>


                <button
                  onClick={resetScenario}
                  className="flex items-center justify-center rounded-xl border border-slate-200 px-4 text-slate-500 transition hover:bg-slate-50 hover:text-slate-800"
                  title="Reset"
                >

                  <RefreshCcw size={17} />

                </button>

              </div>

            </div>

          </section>


          {/* ========================================
              COMPARISON
          ======================================== */}

          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

            <div className="mb-6">

              <h2 className="font-semibold text-slate-900">

                Risk Comparison

              </h2>

              <p className="mt-1 text-xs text-slate-400">

                See how your changes affect the model.

              </p>

            </div>


            {!scenarioResult ? (

              <div className="flex min-h-[360px] flex-col items-center justify-center text-center">

                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-violet-50 text-violet-600">

                  <FlaskConical size={25} />

                </div>


                <h3 className="mt-4 font-semibold text-slate-800">

                  No scenario yet

                </h3>


                <p className="mt-2 max-w-xs text-sm leading-6 text-slate-400">

                  Change one or more values and run
                  the analysis to compare the result.

                </p>

              </div>

            ) : (

              <div className="space-y-5">


                {/* PROBABILITY CHANGE */}

                <div
                  className={`rounded-2xl border p-5 ${
                    riskImproved
                      ? "border-emerald-200 bg-emerald-50/60"
                      : probabilityChange > 0
                      ? "border-red-200 bg-red-50/60"
                      : "border-slate-200 bg-slate-50"
                  }`}
                >

                  <div className="flex items-center justify-between">

                    <div>

                      <p className="text-xs font-medium text-slate-500">

                        Default probability

                      </p>

                      <div className="mt-2 flex items-baseline gap-2">

                        <span className="text-3xl font-bold text-slate-950">

                          {scenarioProbability.toFixed(2)}%

                        </span>

                      </div>

                    </div>


                    <div
                      className={`flex items-center gap-1 rounded-lg px-3 py-2 text-sm font-bold ${
                        riskImproved
                          ? "bg-emerald-100 text-emerald-700"
                          : probabilityChange > 0
                          ? "bg-red-100 text-red-700"
                          : "bg-slate-100 text-slate-600"
                      }`}
                    >

                      {riskImproved ? (
                        <TrendingDown size={15} />
                      ) : (
                        <TrendingUp size={15} />
                      )}

                      {probabilityChange > 0
                        ? "+"
                        : ""}

                      {probabilityChange.toFixed(
                        2
                      )}

                      %

                    </div>

                  </div>


                  <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-200">

                    <div
                      className={`h-full rounded-full ${
                        riskImproved
                          ? "bg-emerald-500"
                          : "bg-red-500"
                      }`}
                      style={{
                        width: `${Math.min(
                          scenarioProbability,
                          100
                        )}%`,
                      }}
                    />

                  </div>


                  <p className="mt-3 text-xs text-slate-500">

                    Current:{" "}
                    <strong>
                      {currentProbability.toFixed(
                        2
                      )}%
                    </strong>

                    {" → "}

                    What-if:{" "}
                    <strong>
                      {scenarioProbability.toFixed(
                        2
                      )}%
                    </strong>

                  </p>

                </div>


                {/* DECISION */}

                <ComparisonRow
                  label="Decision"
                  current={
                    result.decision
                  }
                  scenario={
                    scenarioResult.decision
                  }
                />


                {/* EMI */}

                <ComparisonRow
                  label="Monthly EMI"
                  current={formatCurrency(
                    currentEMI
                  )}
                  scenario={formatCurrency(
                    scenarioEMI
                  )}
                />


                {/* DTI */}

                <ComparisonRow
                  label="Post-loan DTI"
                  current={`${(
                    currentDTI * 100
                  ).toFixed(1)}%`}
                  scenario={`${(
                    scenarioDTI * 100
                  ).toFixed(1)}%`}
                />


                {/* LOAN */}

                <ComparisonRow
                  label="Loan amount"
                  current={formatCurrency(
                    applicant.loan_amount
                  )}
                  scenario={formatCurrency(
                    Number(loanAmount)
                  )}
                />


                {/* INTEREST */}

                <ComparisonRow
                  label="Interest rate"
                  current={`${Number(
                    applicant.interest_rate
                  ).toFixed(1)}%`}
                  scenario={`${Number(
                    interestRate
                  ).toFixed(1)}%`}
                />

              </div>

            )}

          </section>

        </div>


        {/* ==========================================
            SHAP CHANGES
        ========================================== */}

        {scenarioResult && (

          <section className="mt-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

            <div className="mb-5">

              <h2 className="font-semibold text-slate-900">

                What Changed?

              </h2>

              <p className="mt-1 text-xs text-slate-400">

                The model's strongest factors for the
                new scenario.

              </p>

            </div>


            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">

              {scenarioResult
                .risk_increasing_factors
                ?.slice(0, 3)
                .map((factor) => (

                  <div
                    key={factor.feature}
                    className="flex items-center justify-between rounded-xl bg-red-50 px-4 py-3"
                  >

                    <div className="flex items-center gap-3">

                      <TrendingUp
                        size={15}
                        className="text-red-500"
                      />

                      <span className="text-sm font-medium text-slate-700">

                        {factor.label ||
                          factor.feature}

                      </span>

                    </div>

                    <span className="text-xs font-bold text-red-600">

                      +{Number(
                        factor.impact
                      ).toFixed(4)}

                    </span>

                  </div>

                ))}


              {scenarioResult
                .risk_reducing_factors
                ?.slice(0, 3)
                .map((factor) => (

                  <div
                    key={factor.feature}
                    className="flex items-center justify-between rounded-xl bg-emerald-50 px-4 py-3"
                  >

                    <div className="flex items-center gap-3">

                      <TrendingDown
                        size={15}
                        className="text-emerald-600"
                      />

                      <span className="text-sm font-medium text-slate-700">

                        {factor.label ||
                          factor.feature}

                      </span>

                    </div>

                    <span className="text-xs font-bold text-emerald-600">

                      -{Number(
                        factor.impact
                      ).toFixed(4)}

                    </span>

                  </div>

                ))}

            </div>

          </section>

        )}

      </div>

    </main>
  );
}


// ==================================================
// METRIC
// ==================================================

function Metric({
  label,
  value,
  decision,
}) {

  return (

    <div className="rounded-xl bg-slate-50 p-4">

      <p className="text-xs text-slate-400">

        {label}

      </p>

      <p
        className={`mt-1 text-lg font-bold ${
          decision === "Approve"
            ? "text-emerald-700"
            : decision === "Review"
            ? "text-amber-700"
            : "text-slate-900"
        }`}
      >

        {value}

      </p>

    </div>

  );
}


// ==================================================
// SLIDER
// ==================================================

function SliderField({
  label,
  value,
  min,
  max,
  step,
  display,
  icon,
  onChange,
}) {

  return (

    <div>

      <div className="mb-2 flex items-center justify-between">

        <div className="flex items-center gap-2">

          <span className="text-slate-400">

            {icon}

          </span>

          <label className="text-sm font-medium text-slate-700">

            {label}

          </label>

        </div>


        <span className="text-sm font-bold text-slate-900">

          {display}

        </span>

      </div>


      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) =>
          onChange(
            Number(e.target.value)
          )
        }
        className="h-2 w-full cursor-pointer appearance-none rounded-lg bg-slate-200 accent-emerald-700"
      />

    </div>

  );
}


// ==================================================
// COMPARISON ROW
// ==================================================

function ComparisonRow({
  label,
  current,
  scenario,
}) {

  return (

    <div className="flex items-center justify-between border-b border-slate-100 pb-4">

      <p className="text-sm text-slate-500">

        {label}

      </p>


      <div className="flex items-center gap-5 text-right">

        <div>

          <p className="text-[10px] uppercase tracking-wide text-slate-400">

            Current

          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">

            {current}

          </p>

        </div>


        <span className="text-slate-300">

          →

        </span>


        <div>

          <p className="text-[10px] uppercase tracking-wide text-violet-500">

            What-if

          </p>

          <p className="mt-1 text-sm font-bold text-slate-900">

            {scenario}

          </p>

        </div>

      </div>

    </div>

  );
}


export default WhatIf;