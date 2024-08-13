import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <header>
      <a
        href="/"
        className="flex items-center bg-gradient-to-br from-sky-500 to-cyan-400 bg-clip-text text-4xl p-3 font-bold text-transparent"
      >
        Bridger
      </a>
    </header>
    <App />
  </React.StrictMode>,
);
