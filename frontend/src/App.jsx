import { useState } from "react";

import Header from "./components/Header";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Assessment from "./pages/Assessment";
import Results from "./pages/Results";
import WhatIf from "./pages/whatif";


function App() {

  const [page, setPage] =
    useState("login");

  const [result, setResult] =
    useState(null);

  const [applicant, setApplicant] =
    useState(null);


  // --------------------------------------------------
  // AFTER LOGIN
  // --------------------------------------------------

  const handleLogin = () => {

    setPage("assessment");
  };


  // --------------------------------------------------
  // AFTER ASSESSMENT
  // --------------------------------------------------

  const handleResult = ({
    result,
    applicant,
  }) => {

    setResult(result);

    setApplicant(applicant);

    setPage("results");
  };


  return (
    <>

      <Header />


      {/* LOGIN */}

      {page === "login" && (

        <Login
          onLogin={handleLogin}

          onRegister={() =>
            setPage("register")
          }
        />

      )}


      {/* REGISTER */}

      {page === "register" && (

        <Register
          onLogin={() =>
            setPage("login")
          }
        />

      )}


      {/* ASSESSMENT */}

      {page === "assessment" && (

        <Assessment
          onResult={handleResult}
        />

      )}


      {/* RESULTS */}

      {page === "results" && result && (

        <Results
          result={result}

          applicant={applicant}

          onBack={() => {
            setResult(null);
            setApplicant(null);
            setPage("assessment");
          }}

          onWhatIf={() =>
            setPage("whatif")
          }

        />

      )}


      {/* WHAT-IF */}

      {page === "whatif" && applicant && (

        <WhatIf
          applicant={applicant}

          result={result}

          onBack={() =>
            setPage("results")
          }

        />

      )}

    </>
  );
}


export default App;