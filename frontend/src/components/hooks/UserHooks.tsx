import axios from "axios";
import { createContext, useContext, useState, useEffect, useCallback } from "react";
import secureLocalStorage from "react-secure-storage";
import { User } from "../../models/User";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

// ✅ UserContext erstellen
const UserContext = createContext<{ user: User | null; login: (username: string, password: string) => Promise<void>; register: (username: string, password: string) => Promise<void>; logout: () => void; }>({
    user: null,
    login: async () => {},
    register: async () => {},
    logout: () => {},
});

// ✅ UserProvider für globale User-Daten
export function UserProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);

    const logout = useCallback(async () => {
        const token = secureLocalStorage.getItem("access_token");

        if (token) {
            try {
                await axios.post(`${BACKEND_URL}/auth/logout`, {}, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                console.log("Logout erfolgreich.");
            } catch {
                console.warn("Fehler beim Logout-Request.");
            }
        }

        secureLocalStorage.removeItem("access_token");
        setUser(null);
    }, []);

    // 🔹 Holt die User-Daten aus `/me` API und speichert sie in State
    const fetchUserData = useCallback(async () => {
        const token = secureLocalStorage.getItem("access_token");

        if (!token) {
            logout();
            return;
        }

        try {
            const response = await axios.get(`${BACKEND_URL}/users/me`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            setUser({
                user_id: response.data.user_id,
                username: response.data.username,
                color: response.data.color ?? undefined,
                status: response.data.status ?? undefined,
                capturedFigures: response.data.capturedFigures ?? [],
                moveHistory: response.data.moveHistory ?? [],
            });
        } catch {
            console.warn("Token abgelaufen oder ungültig. Benutzer wird ausgeloggt.");
            logout();
        }
    }, [logout]);

    // 🔹 Checkt beim Seitenstart, ob der Token noch gültig ist
    useEffect(() => {
        const checkTokenValidity = async () => {
            const token = secureLocalStorage.getItem("access_token");

            if (!token) {
                logout();
                return;
            }

            try {
                await axios.get(`${BACKEND_URL}/auth/check-token`, {
                    headers: { Authorization: `Bearer ${token}` },
                });

                fetchUserData();
            } catch {
                console.warn("Token ungültig oder abgelaufen. Benutzer wird ausgeloggt.");
                logout();
            }
        };

        checkTokenValidity();
    }, [fetchUserData, logout]);

    // 🔹 Benutzerregistrierung
    const register = async (username: string, password: string) => {
        try {
            const response = await axios.post(`${BACKEND_URL}/users/register`, { username, password });

            // ✅ Direkt einloggen nach Registrierung
            await login(username, password);
            return response.data;
        } catch (err) {
            if (axios.isAxiosError(err) && err.response) {
                throw new Error(err.response.data?.detail || "Registrierung fehlgeschlagen.");
            } else {
                throw new Error("Registrierung fehlgeschlagen.");
            }
        }
    };

    // 🔹 Benutzerlogin
    const login = async (username: string, password: string) => {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        try {
            const response = await axios.post(`${BACKEND_URL}/auth/login`, formData, {
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
            });

            if (response.status === 200) {
                const { access_token } = response.data;
                secureLocalStorage.setItem("access_token", access_token);
                await fetchUserData(); // ✅ Direkt User-Daten abrufen
            }
        } catch (error) {
            console.log("Login Fehler:", error);
            if (axios.isAxiosError(error) && error.response) {
                throw new Error(error.response.data?.detail || "Login fehlgeschlagen.");
            } else {
                throw new Error("Login fehlgeschlagen.");
            }
        }
    };

    return (
        <UserContext.Provider value={{ user, login, register, logout }}>
            {children}
        </UserContext.Provider>
    );
}

// ✅ Custom Hook für globale Nutzung
export function useUser() {
    return useContext(UserContext);
}
