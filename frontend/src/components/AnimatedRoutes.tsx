import { AnimatePresence } from "framer-motion";
import { Routes, Route, useLocation } from "react-router-dom";
import ProtectedRoutes from "./ProtectedRoutes";
import HomePage from "../pages/HomePage";
import LobbyPage from "../pages/LobbyPage";
import GamePage from "../pages/GamePage";
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
            <Route path="lobby" element={<LobbyPage />} />
            <Route path="game/:gameId" element={<GamePage />} />
          </Route>
        </Route>
      </Routes>
    </AnimatePresence>
  );
}

export default AnimatedRoutes;
