import { Navigate, Outlet } from "react-router-dom";
import secureLocalStorage from "react-secure-storage";

function ProtectedRoutes() {
    const token = secureLocalStorage.getItem("access_token");

    const authenticated = !!token;

    return authenticated ? <Outlet /> : <Navigate to="/" />;
}

export default ProtectedRoutes;