import axios from "axios";
import { useState, useEffect, useCallback } from "react";
import secureLocalStorage from "react-secure-storage";

export default function UserHooks() {
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const [user, setUser] = useState<string | null>(secureLocalStorage.getItem("username") as string | null);

    const logout = useCallback(async () => {
        const token = secureLocalStorage.getItem("access_token");
    
        if (!token) {
            console.warn("Kein Token vorhanden, nur localStorage wird geleert.");
        } else {
            try {
                await axios.post(`${BACKEND_URL}/auth/logout`, {}, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                console.log("Logout erfolgreich.");
            } catch {
                console.warn("Fehler beim Logout-Request:");
            }
        }
    
        secureLocalStorage.removeItem("access_token");
        secureLocalStorage.removeItem("user_id");
        secureLocalStorage.removeItem("username");
        setUser(null);
    }, []);
    

    useEffect(() => {
        const checkTokenValidity = async () => {
            const token = secureLocalStorage.getItem("access_token");
            const loggedInUser = secureLocalStorage.getItem("username");

            if (!token || !loggedInUser) {
                logout();
                return;
            }

            try {
                await axios.get(`${BACKEND_URL}/auth/check-token`, {
                    headers: { Authorization: `Bearer ${token}` },
                });

                setUser(loggedInUser as string);
            } catch {
                console.warn("Token abgelaufen oder ungültig. Benutzer wird ausgeloggt.");
                logout();
            }
        };

        checkTokenValidity();
    }, [logout]);

    function register(username: string, password: string) {
        return axios
            .post(`${BACKEND_URL}/users/register`, { username, password })
            .then((response) => {
                setUser(response.data.username);
                secureLocalStorage.setItem("user_id", response.data.user_id);
                secureLocalStorage.setItem("username", response.data.username);
                return response.data;
            })
            .catch((err) => {
                throw new Error(err.response?.data?.detail || "Registrierung fehlgeschlagen.");
            });
    }

    function login(username: string, password: string) {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        return axios
            .post(`${BACKEND_URL}/auth/login`, formData, {
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
            })
            .then((response) => {
                if (response.status === 200) {
                    const { access_token } = response.data;
                    secureLocalStorage.setItem("access_token", access_token);
                    secureLocalStorage.setItem("username", username);
                    setUser(username);
                }
            })
            .catch((error) => {
                console.log("Login Fehler:", error);
                throw new Error(error.response?.data?.detail || "Login fehlgeschlagen.");
            });
    }

    return { register, login, logout, user };
}
