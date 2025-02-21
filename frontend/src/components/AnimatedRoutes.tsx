import { AnimatePresence } from 'framer-motion';
import { Routes, Route, useLocation } from 'react-router-dom';
import ProtectedRoutes from './ProtectedRoutes';
import UserHook from './hooks/UserHooks';
import Register from '../pages/Register';
import LoginPage from '../pages/LoginPage';
import HomePage from '../pages/HomePage';
import ChessGame from '../pages/ChessGame';
import AboutPage from '../pages/AboutPage';

function AnimatedRoutes() {
    const {login, register} = UserHook();
    const location = useLocation();

    return (
        <AnimatePresence>
            <Routes location={location} key={location.pathname}>
                <Route path={"/"} element={<HomePage />} />
                <Route element={<ProtectedRoutes />}>
                    <Route path={"/game"} element={<ChessGame />} />
                </Route>
                <Route path={"/register"} element={<Register register={register} />} />
                <Route path={"/login"} element={<LoginPage login={login} />} />
                <Route path={"/about"} element={<AboutPage />} />
            </Routes>
        </AnimatePresence>
    );
}

export default AnimatedRoutes;