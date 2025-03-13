import axios from 'axios';
import { useCallback } from 'react';
import secureLocalStorage from "react-secure-storage";
import { Lobby } from '../../models/lobby';

export default function GameHooks() {
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

    // 🔹 Spielzug ausführen
    function makeMove(gameId: string, userId: string, moveData: object) {
        const token = secureLocalStorage.getItem("access_token");
        return axios
            .post(`${BACKEND_URL}/game/move/${gameId}/${userId}`, moveData, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(response => response.data)
            .catch(error => {
                throw new Error(error.response?.data?.detail || "Fehler beim Senden des Spielzugs.");
            });
    }

    // 🔹 Neue Lobby erstellen
    function createLobby(userId: string, username: string) {
        const token = secureLocalStorage.getItem("access_token");
        return axios
            .post(`${BACKEND_URL}/lobby/create`, { user_id: userId, username }, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(response => response.data)
            .catch(error => {
                throw new Error(error.response?.data?.detail || "Fehler beim Erstellen der Lobby.");
            });
    }

    const listLobbies = useCallback(async (): Promise<Lobby[]> => {
        try {
            const response = await axios.get(`${BACKEND_URL}/lobby/list`);
            return response.data.lobbies || [];
        } catch (error) {
            console.error("Fehler in listLobbies:", error);
            throw new Error("Fehler beim Abrufen der Lobbys.");
        }
    }, [BACKEND_URL]); // ✅ Jetzt ist listLobbies stabil!

    // 🔹 Lobby beitreten
    function joinLobby(gameId: string, userId: string, username: string) {
        const token = secureLocalStorage.getItem("access_token");
        return axios
            .post(`${BACKEND_URL}/lobby/join/${gameId}`, { user_id: userId, username }, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(response => response.data)
            .catch(error => {
                throw new Error(error.response?.data?.detail || "Fehler beim Beitreten zur Lobby.");
            });
    }

    // 🔹 Lobby verlassen
    function leaveLobby(gameId: string, userId: string) {
        const token = secureLocalStorage.getItem("access_token");
        return axios
            .post(`${BACKEND_URL}/lobby/leave/${gameId}/${userId}`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(response => response.data)
            .catch(error => {
                throw new Error(error.response?.data?.detail || "Fehler beim Verlassen der Lobby.");
            });
    }

    // 🔹 Spielerfarbe setzen
    function setPlayerColor(gameId: string, userId: string, color: "white" | "black") {
        const token = secureLocalStorage.getItem("access_token");
        return axios
            .post(`${BACKEND_URL}/lobby/set_color/${gameId}/${userId}/${color}`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(response => response.data)
            .catch(error => {
                throw new Error(error.response?.data?.detail || "Fehler beim Setzen der Spielerfarbe.");
            });
    }

    // 🔹 Spielerstatus setzen (bereit / nicht bereit)
    function setPlayerStatus(gameId: string, userId: string, status: "ready" | "not_ready") {
        const token = secureLocalStorage.getItem("access_token");
        return axios
            .post(`${BACKEND_URL}/lobby/set_status/${gameId}/${userId}/${status}`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(response => response.data)
            .catch(error => {
                throw new Error(error.response?.data?.detail || "Fehler beim Setzen des Spielerstatus.");
            });
    }

    // 🔹 Spiel starten
    function startGame(gameId: string, userId: string) {
        const token = secureLocalStorage.getItem("access_token");
        return axios
            .post(`${BACKEND_URL}/lobby/start_game/${gameId}/${userId}`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(response => response.data)
            .catch(error => {
                throw new Error(error.response?.data?.detail || "Fehler beim Starten des Spiels.");
            });
    }

    return { makeMove, createLobby, listLobbies, joinLobby, leaveLobby, setPlayerColor, setPlayerStatus, startGame };
    
}
