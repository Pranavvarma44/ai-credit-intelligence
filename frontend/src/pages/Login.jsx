import { useState } from "react";

import {
  Mail,
  Lock,
  ArrowRight,
  ShieldCheck,
  AlertCircle,
} from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL;
function Login({
  onLogin,
  onRegister,
}) {
 
  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  const handleSubmit = async (e) => {

    e.preventDefault();

    setError("");
    setLoading(true);


    try {

      const response =
        await fetch(
          "{API_URL}/auth/login",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              email,
              password,
            }),
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Invalid email or password."
        );
      }


      // Save authentication token
      if (data.access_token) {

        localStorage.setItem(
          "access_token",
          data.access_token
        );
      }


      // Save user if backend returns it
      if (data.user) {

        localStorage.setItem(
          "user",
          JSON.stringify(data.user)
        );
      }


      onLogin();

    } catch (error) {

      setError(
        error.message ||
        "Unable to login."
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

              Welcome back

            </h1>


            <p className="mt-2 text-sm text-slate-500">

              Sign in to continue to CreditRisk.

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
                    value={email}
                    onChange={(e) => {
                      setEmail(
                        e.target.value
                      );
                      setError("");
                    }}
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
                    value={password}
                    onChange={(e) => {
                      setPassword(
                        e.target.value
                      );
                      setError("");
                    }}
                    placeholder="Enter your password"
                    required
                    className="w-full rounded-xl border border-slate-200 bg-white py-3 pl-10 pr-4 text-sm outline-none transition focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
                  />

                </div>

              </div>


              {/* LOGIN */}

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
                  ? "Signing in..."
                  : "Sign in"}

                {!loading && (
                  <ArrowRight
                    size={17}
                    className="transition-transform group-hover:translate-x-1"
                  />
                )}

              </button>

            </form>


            {/* REGISTER */}

            <div className="mt-6 border-t border-slate-100 pt-6 text-center">

              <p className="text-sm text-slate-500">

                Don't have an account?

                <button
                  type="button"
                  onClick={onRegister}
                  className="ml-1 font-semibold text-emerald-800 hover:text-emerald-700"
                >

                  Create account

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


export default Login;