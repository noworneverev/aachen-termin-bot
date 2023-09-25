import React from "react";
import logo from "./logo.svg";
import "./App.css";
import "semantic-ui-css/semantic.min.css";
import { Container, Header } from "semantic-ui-react";
import Home from "./Home";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <Router basename="/frontend">
      <Routes>
        <Route path="/" Component={Home} />
      </Routes>
    </Router>
  );
  // return <Home />;
}

export default App;
