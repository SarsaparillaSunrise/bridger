import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <header className="page-header">
      <a href="/">Bridger</a>
    </header>
    <App />
  </React.StrictMode>,
);
