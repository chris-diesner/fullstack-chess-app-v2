import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/Homepage";
import AboutPage from "./pages/AboutPage";
import "./App.css";
function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/about" element={<AboutPage />} />
    </Routes>
  );
}

export default App;
