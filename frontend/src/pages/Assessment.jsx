import { useState } from "react";

import {
  UserRound,
  Landmark,
  WalletCards,
  CreditCard,
  Activity,
  ArrowRight,
} from "lucide-react";

import FormSection from "../components/FormSection";
import InputField from "../components/InputField";


function Assessment({ onResult }) {

  const [formData, setFormData] = useState({
    // Personal
    age: "",
    employment_type: "Salaried",
    employment_years: "",

    // Income
    monthly_income: "",

    // Loan
    loan_amount: "",
    loan_tenure_months: "",
    interest_rate: "",
    existing_loans: "",
    existing_monthly_debt_payment: "",

    // Credit
    credit_history_months: "",
    credit_utilization: "",
    repayment_consistency: "",
    previous_missed_payments: "",

    // Transactions
    monthly_transactions: "",

    // Financial behaviour
    average_transaction_amount: "",
    spending_volatility: "",
    cash_flow_stability: "",
    income_stability: "",
  });


  // --------------------------------------------------
  // CALCULATE NEW LOAN EMI
  // --------------------------------------------------

  const calculateEMI = () => {

    const P = Number(formData.loan_amount);
    const annualRate = Number(formData.interest_rate);
    const n = Number(formData.loan_tenure_months);

    if (!P || !annualRate || !n) {
      return 0;
    }

    const r = annualRate / 12 / 100;

    const emi =
      (P * r * Math.pow(1 + r, n)) /
      (Math.pow(1 + r, n) - 1);

    return emi;
  };


  // --------------------------------------------------
  // CALCULATE TOTAL MONTHLY DEBT
  // --------------------------------------------------

  const calculateMonthlyDebt = () => {

    const emi = calculateEMI();

    const existingDebt =
      Number(
        formData.existing_monthly_debt_payment
      ) || 0;

    return emi + existingDebt;
  };


  // --------------------------------------------------
  // CALCULATE POST-LOAN DTI
  // --------------------------------------------------

  const calculatePostLoanDTI = () => {

    const income =
      Number(formData.monthly_income);

    if (!income) {
      return 0;
    }

    const monthlyDebt =
      calculateMonthlyDebt();

    return monthlyDebt / income;
  };


  // --------------------------------------------------
  // HANDLE INPUT CHANGES
  // --------------------------------------------------

  const handleChange = (event) => {

    const {
      name,
      value,
    } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };


  // --------------------------------------------------
  // SUBMIT
  // --------------------------------------------------

  const handleSubmit = async (event) => {

    event.preventDefault();


    /*
      These are the fields that the model actually expects.
      The user does NOT directly enter monthly_debt_payment
      or post_loan_dti.
    */

    const payload = {

      // Personal
      age: Number(formData.age),

      employment_type:
        formData.employment_type,

      employment_years:
        Number(formData.employment_years),


      // Income
      monthly_income:
        Number(formData.monthly_income),


      // Loan
      loan_amount:
        Number(formData.loan_amount),

      loan_tenure_months:
        Number(formData.loan_tenure_months),

      existing_loans:
        Number(formData.existing_loans),


      // Calculated model features
      monthly_debt_payment:
        calculateMonthlyDebt(),

      post_loan_dti:
        calculatePostLoanDTI(),


      // Credit
      credit_history_months:
        Number(formData.credit_history_months),

      credit_utilization:
        Number(formData.credit_utilization),

      repayment_consistency:
        Number(formData.repayment_consistency),

      previous_missed_payments:
        Number(formData.previous_missed_payments),


      // Transactions
      monthly_transactions:
        Number(formData.monthly_transactions),

      average_transaction_amount:
        Number(formData.average_transaction_amount),

      spending_volatility:
        Number(formData.spending_volatility),

      cash_flow_stability:
        Number(formData.cash_flow_stability),

      income_stability:
        Number(formData.income_stability),
    };


    console.log(
      "Final prediction payload:",
      payload
    );


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify(payload),
        }
      );


      if (!response.ok) {

        throw new Error(
          `Request failed: ${response.status}`
        );

      }


      const result =
        await response.json();


      console.log(
        "Prediction result:",
        result
      );


      onResult(result);


    } catch (error) {

      console.error(
        "Prediction failed:",
        error
      );

    }
  };


  return (
    <main className="min-h-[calc(100vh-72px)]">

      <div className="mx-auto max-w-5xl px-6 py-14 lg:px-8 lg:py-18">


        {/* ==================================================
            HERO
        ================================================== */}

        <div className="mb-10 max-w-2xl">

          <p className="mb-3 text-xs font-bold tracking-[0.16em] text-emerald-700">
            CREDIT RISK ASSESSMENT
          </p>

          <h1 className="text-4xl font-bold tracking-[-0.04em] text-slate-950 sm:text-5xl">

            Assess applicant

            <span className="block text-emerald-800">
              default risk.
            </span>

          </h1>

          <p className="mt-5 max-w-xl text-base leading-7 text-slate-500">

            Enter the applicant's financial and
            credit information to generate an
            explainable, AI-powered risk assessment.

          </p>

        </div>


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

              <div className="rounded-xl border border-emerald-100 bg-emerald-50/60 p-4">

                <p className="text-xs font-medium text-emerald-700">
                  Estimated New Loan EMI
                </p>

                <p className="mt-1 text-xl font-bold text-slate-900">

                  ₹
                  {calculateEMI().toLocaleString(
                    "en-IN",
                    {
                      maximumFractionDigits: 0,
                    }
                  )}

                </p>

                <p className="mt-1 text-xs text-slate-400">
                  Calculated from loan amount, tenure and interest rate.
                </p>

              </div>


              {/* DTI */}

              <div className="rounded-xl border border-emerald-100 bg-emerald-50/60 p-4">

                <p className="text-xs font-medium text-emerald-700">
                  Post-loan DTI
                </p>

                <p className="mt-1 text-xl font-bold text-slate-900">

                  {(calculatePostLoanDTI() * 100).toFixed(1)}%

                </p>

                <p className="mt-1 text-xs text-slate-400">
                  Total monthly debt relative to income.
                </p>

              </div>

            </div>

          </FormSection>


          {/* ==================================================
              INCOME & FINANCIAL STABILITY
          ================================================== */}

          <FormSection
            icon={WalletCards}
            title="Income & Financial Stability"
            description="Income and cash-flow characteristics."
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
              label="Income Stability"
              name="income_stability"
              value={formData.income_stability}
              onChange={handleChange}
              placeholder="0.90"
              min="0"
              max="1"
              step="0.01"
              help="Value between 0 and 1."
              required
            />


            <InputField
              label="Cash-flow Stability"
              name="cash_flow_stability"
              value={formData.cash_flow_stability}
              onChange={handleChange}
              placeholder="0.90"
              min="0"
              max="1"
              step="0.01"
              help="Value between 0 and 1."
              required
            />

          </FormSection>


          {/* ==================================================
              CREDIT HISTORY
          ================================================== */}

          <FormSection
            icon={CreditCard}
            title="Credit History"
            description="Credit behavior and repayment history."
          >

            <InputField
              label="Credit History"
              name="credit_history_months"
              value={formData.credit_history_months}
              onChange={handleChange}
              placeholder="48"
              min="0"
              required
            />


            <InputField
              label="Credit Utilization"
              name="credit_utilization"
              value={formData.credit_utilization}
              onChange={handleChange}
              placeholder="20"
              min="0"
              max="100"
              step="0.1"
              help="Percentage of available credit being used."
              required
            />


            <InputField
              label="Repayment Consistency"
              name="repayment_consistency"
              value={formData.repayment_consistency}
              onChange={handleChange}
              placeholder="90"
              min="0"
              max="100"
              step="0.1"
              help="Percentage of on-time payments."
              required
            />


            <InputField
              label="Previous Missed Payments"
              name="previous_missed_payments"
              value={formData.previous_missed_payments}
              onChange={handleChange}
              placeholder="0"
              min="0"
              required
            />

          </FormSection>


          {/* ==================================================
              TRANSACTION BEHAVIOUR
          ================================================== */}

          <FormSection
            icon={Activity}
            title="Transaction Behaviour"
            description="Patterns in the applicant's financial activity."
          >

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
              required
            />


            <InputField
              label="Spending Volatility"
              name="spending_volatility"
              value={formData.spending_volatility}
              onChange={handleChange}
              placeholder="0.10"
              min="0"
              max="1"
              step="0.01"
              help="Value between 0 and 1."
              required
            />

          </FormSection>


          {/* ==================================================
              SUBMIT
          ================================================== */}

          <div className="flex flex-col items-start justify-between gap-5 pt-3 sm:flex-row sm:items-center">

            <p className="max-w-lg text-xs leading-5 text-slate-400">

              The information provided will be processed
              by the credit-risk model to generate an
              assessment.

            </p>


            <button
              type="submit"
              className="group flex items-center gap-3 rounded-xl bg-emerald-900 px-6 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-800 hover:shadow-md"
            >

              Analyze Risk

              <ArrowRight
                size={17}
                className="transition-transform group-hover:translate-x-1"
              />

            </button>

          </div>

        </form>

      </div>

    </main>
  );
}


export default Assessment;