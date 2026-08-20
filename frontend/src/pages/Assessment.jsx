import { useState } from "react";

import {
  UserRound,
  Landmark,
  WalletCards,
  CreditCard,
  Activity,
  ArrowRight,
  Sparkles,
  ShieldCheck,
  AlertCircle,
} from "lucide-react";

import FormSection from "../components/FormSection";
import InputField from "../components/InputField";

const API_URL = import.meta.env.VITE_API_URL;
function Assessment({ onResult }) {


  const [formData, setFormData] = useState({

    // ------------------------------------------
    // PERSONAL
    // ------------------------------------------

    age: "",
    employment_type: "Salaried",
    employment_years: "",


    // ------------------------------------------
    // INCOME
    // ------------------------------------------

    monthly_income: "",


    // ------------------------------------------
    // LOAN
    // ------------------------------------------

    loan_amount: "",
    loan_tenure_months: "",
    interest_rate: "",
    existing_loans: "",
    existing_monthly_debt_payment: "",


    // ------------------------------------------
    // CREDIT
    // ------------------------------------------

    credit_history_months: "",
    credit_utilization: "",
    repayment_consistency: "",
    previous_missed_payments: "",


    // ------------------------------------------
    // TRANSACTIONS
    // ------------------------------------------

    monthly_transactions: "",
    average_transaction_amount: "",

  });


  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  // --------------------------------------------------
  // NTC STATUS
  // --------------------------------------------------

  const isNTC =
    formData.credit_history_months !== "" &&
    Number(formData.credit_history_months) === 0;


  // --------------------------------------------------
  // CALCULATE NEW LOAN EMI
  // --------------------------------------------------

  const calculateEMI = () => {

    const P =
      Number(formData.loan_amount);

    const annualRate =
      Number(formData.interest_rate);

    const n =
      Number(formData.loan_tenure_months);


    if (
      !P ||
      !annualRate ||
      !n
    ) {

      return 0;
    }


    const r =
      annualRate / 12 / 100;


    const emi =
      (
        P *
        r *
        Math.pow(
          1 + r,
          n
        )
      ) /
      (
        Math.pow(
          1 + r,
          n
        ) - 1
      );


    return emi;
  };


  // --------------------------------------------------
  // CALCULATE TOTAL MONTHLY DEBT
  // --------------------------------------------------

  const calculateMonthlyDebt = () => {

    const emi =
      calculateEMI();


    const existingDebt =
      Number(
        formData.existing_monthly_debt_payment
      ) || 0;


    return (
      emi +
      existingDebt
    );
  };


  // --------------------------------------------------
  // CALCULATE POST-LOAN DTI
  // --------------------------------------------------

  const calculatePostLoanDTI = () => {

    const income =
      Number(
        formData.monthly_income
      );


    if (!income) {

      return 0;
    }


    return (
      calculateMonthlyDebt() /
      income
    );
  };


  // --------------------------------------------------
  // HANDLE INPUT CHANGES
  // --------------------------------------------------

  const handleChange = (event) => {

    const {
      name,
      value,
    } = event.target;


    setFormData(
      (previous) => ({
        ...previous,
        [name]: value,
      })
    );


    setError("");
  };


  // --------------------------------------------------
  // HANDLE NTC TOGGLE
  // --------------------------------------------------

  const handleNTCToggle = () => {

    if (isNTC) {

      setFormData(
        (previous) => ({
          ...previous,

          credit_history_months: "",

          credit_utilization: "",

          repayment_consistency: "",

          previous_missed_payments: "",

          existing_loans: "",

          existing_monthly_debt_payment: "",
        })
      );

    } else {

      setFormData(
        (previous) => ({
          ...previous,

          credit_history_months: "0",

          credit_utilization: "0",

          repayment_consistency: "0",

          previous_missed_payments: "0",

          existing_loans: "0",

          existing_monthly_debt_payment: "0",
        })
      );
    }

    setError("");
  };


  // --------------------------------------------------
  // VALIDATION
  // --------------------------------------------------

  const validateForm = () => {

    const income =
      Number(
        formData.monthly_income
      );

    const loan =
      Number(
        formData.loan_amount
      );

    const tenure =
      Number(
        formData.loan_tenure_months
      );

    const interest =
      Number(
        formData.interest_rate
      );


    if (income <= 0) {

      return "Monthly income must be greater than zero.";
    }


    if (loan <= 0) {

      return "Loan amount must be greater than zero.";
    }


    if (tenure <= 0) {

      return "Loan tenure must be greater than zero.";
    }


    if (interest <= 0) {

      return "Interest rate must be greater than zero.";
    }


    if (
      Number(
        formData.credit_history_months
      ) === 0 &&
      Number(
        formData.existing_loans
      ) !== 0
    ) {

      return (
        "An applicant with no credit history cannot have existing loans."
      );
    }


    if (
      Number(
        formData.credit_history_months
      ) === 0 &&
      (
        Number(
          formData.credit_utilization
        ) !== 0 ||

        Number(
          formData.previous_missed_payments
        ) !== 0
      )
    ) {

      return (
        "For an NTC applicant, credit utilization and previous missed payments must be zero."
      );
    }


    return null;
  };


  // --------------------------------------------------
  // SUBMIT
  // --------------------------------------------------

  const handleSubmit = async (event) => {

    event.preventDefault();


    setError("");


    const validationError =
      validateForm();


    if (validationError) {

      setError(
        validationError
      );

      return;
    }


    setLoading(true);


    // --------------------------------------------------
    // DETERMINE NTC FLAG
    // --------------------------------------------------

    const ntcFlag =
      Number(
        formData.credit_history_months
      ) === 0
        ? 1
        : 0;


    // --------------------------------------------------
    // FINAL MODEL PAYLOAD
    // --------------------------------------------------

    const payload = {

      age:
        Number(
          formData.age
        ),

      employment_type:
        formData.employment_type,

      employment_years:
        Number(
          formData.employment_years
        ),

      monthly_income:
        Number(
          formData.monthly_income
        ),

      loan_amount:
        Number(
          formData.loan_amount
        ),

      loan_tenure_months:
        Number(
          formData.loan_tenure_months
        ),

      existing_loans:
        Number(
          formData.existing_loans
        ),

      monthly_debt_payment:
        calculateMonthlyDebt(),

      post_loan_dti:
        calculatePostLoanDTI(),

      credit_history_months:
        Number(
          formData.credit_history_months
        ),

      credit_utilization:
        Number(
          formData.credit_utilization
        ),

      repayment_consistency:
        Number(
          formData.repayment_consistency
        ),

      previous_missed_payments:
        Number(
          formData.previous_missed_payments
        ),

      monthly_transactions:
        Number(
          formData.monthly_transactions
        ),

      average_transaction_amount:
        Number(
          formData.average_transaction_amount
        ),

      ntc_flag:
        ntcFlag,
    };


    console.log(
      "Final prediction payload:",
      payload
    );


    try {

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
                payload
              ),
          }
        );


      // --------------------------------------------------
      // HANDLE API ERROR
      // --------------------------------------------------

      if (!response.ok) {

        let message =
          `Request failed: ${response.status}`;


        try {

          const errorData =
            await response.json();


          if (errorData.detail) {

            message =
              errorData.detail;
          }

        } catch {

          // Ignore JSON parsing error

        }


        throw new Error(
          message
        );
      }


      // --------------------------------------------------
      // GET RESULT
      // --------------------------------------------------

      const result =
        await response.json();


      console.log(
        "Prediction result:",
        result
      );


      // --------------------------------------------------
      // SEND RESULT + APPLICANT
      //
      // The model payload is preserved exactly.
      //
      // We additionally keep:
      //
      // interest_rate
      // existing_monthly_debt_payment
      //
      // These are needed by What-If Analysis.
      // --------------------------------------------------

      onResult({

        result: result,

        applicant: {

          ...payload,

          interest_rate:
            Number(
              formData.interest_rate
            ),

          existing_monthly_debt_payment:
            Number(
              formData.existing_monthly_debt_payment
            ) || 0,

        },

      });


    } catch (error) {

      console.error(
        "Prediction failed:",
        error
      );


      setError(
        error.message ||
        "Unable to complete the assessment."
      );

    } finally {

      setLoading(false);
    }
  };


  // --------------------------------------------------
  // RENDER
  // --------------------------------------------------

  return (

    <main className="min-h-[calc(100vh-72px)] bg-slate-50">


      <div className="mx-auto max-w-5xl px-6 py-12 lg:px-8 lg:py-16">


        {/* ==================================================
            HERO
        ================================================== */}

        <div className="mb-10">

          <div className="mb-4 flex items-center gap-2">

            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-100">

              <ShieldCheck
                size={17}
                className="text-emerald-700"
              />

            </div>


            <p className="text-xs font-bold tracking-[0.16em] text-emerald-700">

              CREDIT RISK ASSESSMENT

            </p>

          </div>


          <h1 className="text-4xl font-bold tracking-[-0.04em] text-slate-950 sm:text-5xl">

            Assess applicant

            <span className="block text-emerald-800">

              default risk.

            </span>

          </h1>


          <p className="mt-5 max-w-2xl text-base leading-7 text-slate-500">

            Enter the applicant's financial and credit
            information to generate an explainable,
            AI-powered risk assessment.

          </p>


          {/* AI BADGE */}

          <div className="mt-6 inline-flex items-center gap-2 rounded-full border border-emerald-100 bg-white px-4 py-2 text-xs font-medium text-slate-600 shadow-sm">

            <Sparkles
              size={14}
              className="text-emerald-600"
            />

            XGBoost + SHAP + AI Explanation

          </div>

        </div>


        {/* ==================================================
            ERROR
        ================================================== */}

        {error && (

          <div className="mb-6 flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-4 text-sm text-red-700">

            <AlertCircle
              size={18}
              className="mt-0.5 shrink-0"
            />

            <div>

              <p className="font-semibold">

                Assessment could not be completed

              </p>

              <p className="mt-1">

                {error}

              </p>

            </div>

          </div>

        )}


        {/* ==================================================
            FORM
        ================================================== */}

        <form
          onSubmit={handleSubmit}
          className="space-y-5"
        >


          {/* ==================================================
              PERSONAL & EMPLOYMENT
          ================================================== */}

          <FormSection
            icon={UserRound}
            title="Personal & Employment"
            description="Basic information about the applicant."
          >

            <InputField
              label="Age"
              name="age"
              value={formData.age}
              onChange={handleChange}
              placeholder="35"
              min="18"
              max="100"
              required
            />


            <InputField
              label="Employment Type"
              name="employment_type"
              value={formData.employment_type}
              onChange={handleChange}
              type="text"
              options={[
                "Salaried",
                "Self-Employed",
                "Contract",
              ]}
              required
            />


            <InputField
              label="Employment Years"
              name="employment_years"
              value={formData.employment_years}
              onChange={handleChange}
              placeholder="8"
              min="0"
              step="0.1"
              required
            />

          </FormSection>


          {/* ==================================================
              LOAN DETAILS
          ================================================== */}

          <FormSection
            icon={Landmark}
            title="Loan Details"
            description="Requested loan and existing debt information."
          >

            <InputField
              label="Loan Amount"
              name="loan_amount"
              value={formData.loan_amount}
              onChange={handleChange}
              placeholder="200000"
              min="0"
              required
            />


            <InputField
              label="Loan Tenure"
              name="loan_tenure_months"
              value={formData.loan_tenure_months}
              onChange={handleChange}
              placeholder="36"
              min="1"
              required
            />


            <InputField
              label="Interest Rate"
              name="interest_rate"
              value={formData.interest_rate}
              onChange={handleChange}
              placeholder="12"
              min="0.1"
              max="50"
              step="0.1"
              help="Annual interest rate for the requested loan."
              required
            />


            <InputField
              label="Existing Loans"
              name="existing_loans"
              value={formData.existing_loans}
              onChange={handleChange}
              placeholder="1"
              min="0"
              required
            />


            <InputField
              label="Existing Monthly Debt Payment"
              name="existing_monthly_debt_payment"
              value={
                formData.existing_monthly_debt_payment
              }
              onChange={handleChange}
              placeholder="10000"
              min="0"
              help="Current monthly payments before the new loan."
              required
            />


            {/* CALCULATED VALUES */}

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 md:col-span-2">


              {/* EMI */}

              <div className="rounded-xl border border-emerald-100 bg-gradient-to-br from-emerald-50 to-white p-4">

                <div className="flex items-center justify-between">

                  <p className="text-xs font-semibold uppercase tracking-wide text-emerald-700">

                    Estimated EMI

                  </p>

                  <WalletCards
                    size={16}
                    className="text-emerald-600"
                  />

                </div>


                <p className="mt-2 text-2xl font-bold text-slate-900">

                  ₹
                  {calculateEMI().toLocaleString(
                    "en-IN",
                    {
                      maximumFractionDigits: 0,
                    }
                  )}

                </p>


                <p className="mt-1 text-xs text-slate-400">

                  Estimated monthly payment for the new loan.

                </p>

              </div>


              {/* DTI */}

              <div className="rounded-xl border border-emerald-100 bg-gradient-to-br from-emerald-50 to-white p-4">

                <div className="flex items-center justify-between">

                  <p className="text-xs font-semibold uppercase tracking-wide text-emerald-700">

                    Post-loan DTI

                  </p>

                  <Activity
                    size={16}
                    className="text-emerald-600"
                  />

                </div>


                <p className="mt-2 text-2xl font-bold text-slate-900">

                  {
                    (
                      calculatePostLoanDTI() *
                      100
                    ).toFixed(1)
                  }%

                </p>


                <p className="mt-1 text-xs text-slate-400">

                  Total monthly debt relative to income.

                </p>

              </div>

            </div>

          </FormSection>


          {/* ==================================================
              INCOME
          ================================================== */}

          <FormSection
            icon={WalletCards}
            title="Income & Financial Stability"
            description="Current income and financial activity."
          >

            <InputField
              label="Monthly Income"
              name="monthly_income"
              value={formData.monthly_income}
              onChange={handleChange}
              placeholder="50000"
              min="0"
              required
            />


            <InputField
              label="Monthly Transactions"
              name="monthly_transactions"
              value={formData.monthly_transactions}
              onChange={handleChange}
              placeholder="40"
              min="0"
              required
            />


            <InputField
              label="Average Transaction Amount"
              name="average_transaction_amount"
              value={
                formData.average_transaction_amount
              }
              onChange={handleChange}
              placeholder="800"
              min="0"
              help="Typical value of a monthly transaction."
              required
            />

          </FormSection>


          {/* ==================================================
              CREDIT
          ================================================== */}

          <FormSection
            icon={CreditCard}
            title="Credit Profile"
            description="Credit history and repayment information."
          >


            {/* NTC TOGGLE */}

            <div className="md:col-span-2">

              <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4">

                <div className="flex items-start gap-3">

                  <div
                    className={`mt-0.5 flex h-9 w-9 items-center justify-center rounded-lg ${
                      isNTC
                        ? "bg-amber-100"
                        : "bg-emerald-100"
                    }`}
                  >

                    <CreditCard
                      size={17}
                      className={
                        isNTC
                          ? "text-amber-700"
                          : "text-emerald-700"
                      }
                    />

                  </div>


                  <div>

                    <p className="text-sm font-semibold text-slate-900">

                      New to Credit

                    </p>

                    <p className="mt-0.5 text-xs text-slate-500">

                      Applicant has no established formal credit history.

                    </p>

                  </div>

                </div>


                <button
                  type="button"
                  onClick={handleNTCToggle}
                  className={`relative h-6 w-11 rounded-full transition ${
                    isNTC
                      ? "bg-emerald-700"
                      : "bg-slate-300"
                  }`}
                >

                  <span
                    className={`absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition ${
                      isNTC
                        ? "left-6"
                        : "left-1"
                    }`}
                  />

                </button>

              </div>


              {isNTC && (

                <div className="mt-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3">

                  <p className="text-sm font-semibold text-amber-900">

                    NTC applicant

                  </p>

                  <p className="mt-1 text-xs leading-5 text-amber-800">

                    Historical credit information is unavailable.
                    The assessment will rely more heavily on current
                    income, employment, affordability and financial activity.

                  </p>

                </div>

              )}

            </div>


            <InputField
              label="Credit History"
              name="credit_history_months"
              value={
                formData.credit_history_months
              }
              onChange={handleChange}
              placeholder="48"
              min="0"
              disabled={isNTC}
              help={
                isNTC
                  ? "NTC applicants have 0 months of formal credit history."
                  : "Length of established formal credit history."
              }
              required
            />


            <InputField
              label="Credit Utilization"
              name="credit_utilization"
              value={
                formData.credit_utilization
              }
              onChange={handleChange}
              placeholder="20"
              min="0"
              max="100"
              step="0.1"
              disabled={isNTC}
              help={
                isNTC
                  ? "No previous revolving-credit utilization."
                  : "Percentage of available credit being used."
              }
              required
            />


            <InputField
              label="Repayment Consistency"
              name="repayment_consistency"
              value={
                formData.repayment_consistency
              }
              onChange={handleChange}
              placeholder="90"
              min="0"
              max="100"
              step="0.1"
              disabled={isNTC}
              help={
                isNTC
                  ? "No established formal repayment history."
                  : "Percentage of on-time payments."
              }
              required
            />


            <InputField
              label="Previous Missed Payments"
              name="previous_missed_payments"
              value={
                formData.previous_missed_payments
              }
              onChange={handleChange}
              placeholder="0"
              min="0"
              disabled={isNTC}
              required
            />

          </FormSection>


          {/* ==================================================
              SUBMIT
          ================================================== */}

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">

            <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

              <div>

                <div className="flex items-center gap-2">

                  <ShieldCheck
                    size={17}
                    className="text-emerald-700"
                  />

                  <p className="text-sm font-semibold text-slate-900">

                    Ready for assessment

                  </p>

                </div>


                <p className="mt-1 max-w-xl text-xs leading-5 text-slate-500">

                  Your information will be evaluated using the
                  credit-risk model and explained using AI.

                </p>

              </div>


              <button
                type="submit"
                disabled={loading}
                className={`group flex min-w-[180px] items-center justify-center gap-3 rounded-xl px-6 py-3.5 text-sm font-semibold text-white shadow-sm transition ${
                  loading
                    ? "cursor-not-allowed bg-slate-400"
                    : "bg-emerald-900 hover:bg-emerald-800 hover:shadow-md"
                }`}
              >

                {loading ? (

                  <>

                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />

                    Assessing...

                  </>

                ) : (

                  <>

                    Analyze Risk

                    <ArrowRight
                      size={17}
                      className="transition-transform group-hover:translate-x-1"
                    />

                  </>

                )}

              </button>

            </div>

          </div>


        </form>

      </div>

    </main>
  );
}


export default Assessment;