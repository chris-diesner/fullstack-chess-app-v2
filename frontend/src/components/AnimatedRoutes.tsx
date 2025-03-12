import { AnimatePresence } from "framer-motion";
import { Routes, Route, useLocation } from "react-router-dom";
import ProtectedRoutes from "./ProtectedRoutes";
import HomePage from "../pages/HomePage";
import ChessGame from "../pages/ChessGame";
import AboutPage from "../pages/AboutPage";
import Layout from "./Layout";

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence>
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="about" element={<AboutPage />} />

          <Route element={<ProtectedRoutes />}>
            <Route path="game" element={<ChessGame />} />
          </Route>
        </Route>
      </Routes>
    </AnimatePresence>
  );
}

export default AnimatedRoutes;
