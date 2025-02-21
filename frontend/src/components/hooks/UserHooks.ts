import axios from 'axios';
import { useState } from 'react';
import secureLocalStorage from "react-secure-storage";

export default function UserHooks() {
    const [user, setUser] = useState<string>();
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

    function register(username: string, password: string) {
        return axios
            .post(`${BACKEND_URL}/auth/register`, {
                    username,
                    password,
            })
            .then((response) => setUser(response.data))
            .catch((err) => {
                throw new Error(err.response.data.detail);
            });
    }

    function login(username: string, password: string) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        return axios
            .post(`${BACKEND_URL}/auth/login`, formData, {headers:{'Content-Type':'application/x-www-form-urlencoded'}})
            .then((response) => {
                if (response.status === 200) {
                    secureLocalStorage.setItem("access_token", response.data.access_token)
                }
            })
            .catch((error) => {
                    console.log(error)
                }
            )
    }

    function logout() {
        return axios
            .post(`${BACKEND_URL}/auth/logout`)
            .then(() => {
                secureLocalStorage.removeItem("username");
            })
            .catch((err) => {
                throw new Error(err.response.data.detail);
            });
    }
    return { register, login, logout, user };
}