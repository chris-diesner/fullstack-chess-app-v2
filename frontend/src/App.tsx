import { Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import HomePage from "./pages/HomePage";
import ChessGame from "./pages/ChessGame";
import AboutPage from "./pages/AboutPage";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/game" element={<ChessGame />} />
      <Route path="/about" element={<AboutPage />} />
    </Routes>
  );
}

export default App;