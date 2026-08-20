import { useState } from "react";
import {
  UserRound,
  Mail,
  Lock,
  ArrowRight,
  ShieldCheck,
  AlertCircle,
} from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL;
function Register({ onLogin }) {

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  const handleChange = (e) => {

    const {
      name,
      value,
    } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    setError("");
  };


  const handleSubmit = async (e) => {

    e.preventDefault();

    setError("");


    if (
      formData.password !==
      formData.confirmPassword
    ) {

      setError(
        "Passwords do not match."
      );

      return;
    }


    if (
      formData.password.length < 6
    ) {

      setError(
        "Password must contain at least 6 characters."
      );

      return;
    }


    setLoading(true);


    try {

      const response = await fetch(
        "{API_URL}/auth/register",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            name: formData.name,
            email: formData.email,
            password: formData.password,
          }),
        }
      );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Registration failed."
        );
      }


      // Registration successful
      onLogin();

    } catch (error) {

      setError(
        error.message ||
        "Unable to register."
      );

    } finally {

      setLoading(false);

    }
  };


  return (

    <main className="min-h-[calc(100vh-72px)] bg-slate-50">

      <div className="flex min-h-[calc(100vh-72px)] items-center justify-center px-6 py-12">

        <div className="w-full max-w-md">


          {/* LOGO */}

          <div className="mb-8 text-center">

            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-900">

              <ShieldCheck
                size={25}
                className="text-white"
              />

            </div>


            <h1 className="text-3xl font-bold tracking-tight text-slate-950">

              Create your account

            </h1>


            <p className="mt-2 text-sm text-slate-500">

              Get started with CreditRisk.

            </p>

          </div>


          {/* CARD */}

          <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm">


            {/* ERROR */}

            {error && (

              <div className="mb-5 flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">

                <AlertCircle
                  size={17}
                  className="mt-0.5 shrink-0"
                />

                <p>{error}</p>

              </div>

            )}


            <form
              onSubmit={handleSubmit}
              className="space-y-5"
            >


              {/* NAME */}

              <div>

                <label className="mb-2 block text-sm font-medium text-slate-700">

                  Full name

                </label>


                <div className="relative">

                  <UserRound
                    size={17}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                  />


                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Your name"
                    required
                    className="w-full rounded-xl border border-slate-200 bg-white py-3 pl-10 pr-4 text-sm outline-none transition focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
                  />

                </div>

              </div>


              {/* EMAIL */}

              <div>

                <label className="mb-2 block text-sm font-medium text-slate-700">

                  Email address

                </label>


                <div className="relative">

                  <Mail
                    size={17}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                  />


                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="you@example.com"
                    required
                    className="w-full rounded-xl border border-slate-200 bg-white py-3 pl-10 pr-4 text-sm outline-none transition focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
                  />

                </div>

              </div>


              {/* PASSWORD */}

              <div>

                <label className="mb-2 block text-sm font-medium text-slate-700">

                  Password

                </label>


                <div className="relative">

                  <Lock
                    size={17}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                  />


                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Minimum 6 characters"
                    required
                    className="w-full rounded-xl border border-slate-200 bg-white py-3 pl-10 pr-4 text-sm outline-none transition focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
                  />

                </div>

              </div>


              {/* CONFIRM PASSWORD */}

              <div>

                <label className="mb-2 block text-sm font-medium text-slate-700">

                  Confirm password

                </label>


                <div className="relative">

                  <Lock
                    size={17}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                  />


                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder="Re-enter your password"
                    required
                    className="w-full rounded-xl border border-slate-200 bg-white py-3 pl-10 pr-4 text-sm outline-none transition focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
                  />

                </div>

              </div>


              {/* SUBMIT */}

              <button
                type="submit"
                disabled={loading}
                className={`group flex w-full items-center justify-center gap-2 rounded-xl px-5 py-3.5 text-sm font-semibold text-white transition ${
                  loading
                    ? "cursor-not-allowed bg-slate-400"
                    : "bg-emerald-900 hover:bg-emerald-800"
                }`}
              >

                {loading
                  ? "Creating account..."
                  : "Create account"}

                {!loading && (
                  <ArrowRight
                    size={17}
                    className="transition-transform group-hover:translate-x-1"
                  />
                )}

              </button>

            </form>


            {/* LOGIN */}

            <div className="mt-6 border-t border-slate-100 pt-6 text-center">

              <p className="text-sm text-slate-500">

                Already have an account?

                <button
                  type="button"
                  onClick={onLogin}
                  className="ml-1 font-semibold text-emerald-800 hover:text-emerald-700"
                >

                  Sign in

                </button>

              </p>

            </div>

          </div>


          <p className="mt-6 text-center text-xs text-slate-400">

            CreditRisk • Explainable AI-powered risk assessment

          </p>

        </div>

      </div>

    </main>
  );
}


export default Register;