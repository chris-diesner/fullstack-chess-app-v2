import axios from 'axios';
import { useCallback, useEffect, useState } from 'react';
import secureLocalStorage from "react-secure-storage";
import { Lobby } from '../../models/Lobby';

export default function GameHooks(updateLobbies: (lobbies: Lobby[]) => void) {
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const [socket, setSocket] = useState<WebSocket | null>(null);

    const connectWebSocket = (gameId: string) => {
        const webSocket = new WebSocket(`${BACKEND_URL.replace("http", "ws")}/lobby/ws/${gameId}`);

        webSocket.onopen = () => {
            console.log("WebSocket connected.");
        };

        webSocket.onmessage = async (event) => {
            console.log(event.data);
            const data = JSON.parse(event.data);
            updateLobbies([data]); 
        };

        webSocket.onclose = () => {
            console.log("WebSocket closed.");
        };
        setSocket(webSocket);
    };
    
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

    const createLobby = async (userId: string, username: string) => {
        const token = secureLocalStorage.getItem("access_token");
    
        try {
            const response = await axios.post(`${BACKEND_URL}/lobby/create`, { user_id: userId, username }, {
                headers: { Authorization: `Bearer ${token}` }
            });
    
            const gameId = response.data.game_id;
            await listLobbies();
            connectWebSocket(gameId);
            console.log("Aktiver WebSocket nach createLobby:", socket);
        } catch (error) {
            if (axios.isAxiosError(error) && error.response) {
                throw new Error(error.response.data?.detail || "Fehler beim Erstellen der Lobby.");
            } else {
                throw new Error("Fehler beim Erstellen der Lobby.");
            }
        }
    };
    

    const listLobbies = useCallback(async (): Promise<Lobby[]> => {
        try {
            const response = await axios.get(`${BACKEND_URL}/lobby/list`);
            return response.data.lobbies || [];
        } catch (error) {
            console.error("Fehler in listLobbies:", error);
            throw new Error("Fehler beim Abrufen der Lobbys.");
        }
    }, [BACKEND_URL]);

    const joinLobby = async (gameId: string, userId: string, username: string) => {
        const token = secureLocalStorage.getItem("access_token");
        await axios
            .post(`${BACKEND_URL}/lobby/join/${gameId}`, { user_id: userId, username }, {
                headers: { Authorization: `Bearer ${token}` }
            })
            await listLobbies();
            connectWebSocket(gameId);
    }

    const leaveLobby = async (gameId: string, userId: string) => {
        await axios.post(`${BACKEND_URL}/lobby/leave/${gameId}/${userId}`);
        await listLobbies();
        socket?.close();
    };

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

    useEffect(() => {
        listLobbies();
    }, [listLobbies]);

    return { makeMove, createLobby, listLobbies, joinLobby, leaveLobby, setPlayerColor, setPlayerStatus, startGame };
    
}
