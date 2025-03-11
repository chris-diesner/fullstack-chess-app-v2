import axios from 'axios';
import { useState } from 'react';
import secureLocalStorage from "react-secure-storage";

export default function UserHooks() {
    const [user, setUser] = useState<string | null>(null);
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

    function register(username: string, password: string) {
        return axios
            .post(`${BACKEND_URL}/users/register`, { username, password })
            .then((response) => {
                setUser(response.data.username);
                secureLocalStorage.setItem("username", response.data.username);
                return response.data;
            })
            .catch((err) => {
                throw new Error(err.response?.data?.detail || "Registrierung fehlgeschlagen.");
            });
    }

    function login(username: string, password: string) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('grant_type', 'password');

        return axios
            .post(`${BACKEND_URL}/auth/login`, formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
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

    function logout() {
        const token = secureLocalStorage.getItem("access_token");
        return axios
            .post(`${BACKEND_URL}/auth/logout`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(() => {
                secureLocalStorage.removeItem("access_token");
                secureLocalStorage.removeItem("username");
                setUser(null);
            })
            .catch((err) => {
                throw new Error(err.response?.data?.detail || "Logout fehlgeschlagen.");
            });
    }

    return { register, login, logout, user };
}
