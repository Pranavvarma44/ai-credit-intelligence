import { useState } from "react";

import Header from "./components/Header";
import Assessment from "./pages/Assessment";
import Results from "./pages/Results";


function App() {

  const [result, setResult] = useState(null);


  return (
    <>
      <Header />

      {result ? (

        <Results
          result={result}
          onBack={() => setResult(null)}
        />

      ) : (

        <Assessment
          onResult={setResult}
        />

      )}

    </>
  );
}


export default App;