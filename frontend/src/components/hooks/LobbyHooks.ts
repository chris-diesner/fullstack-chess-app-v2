import axios from 'axios';
import { useCallback, useEffect, useState } from 'react';
import secureLocalStorage from "react-secure-storage";
import { useNavigate } from 'react-router-dom';
import { Lobby } from '../../models/Lobby';
import { ChessGame } from '../../models/ChessGame';
import { useGame } from './GameHooks';

export default function LobbyHooks(
    updateLobbies: (lobbies: Lobby[]) => void,
    updateGameState: (gameState: ChessGame | null) => void
) {
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const [lobbySocket, setLobbySocket] = useState<WebSocket | null>(null);
    const navigate = useNavigate();
    const { connectGameWebSocket } = useGame();

    const connectLobbyWebSocket = (gameId: string) => {
        if (lobbySocket?.readyState === WebSocket.OPEN) {
            console.log("Lobby WebSocket bereits offen.");
            return;
        }
    
        console.log("Lobby WebSocket wird (re-)verbunden für", gameId);
        const lobbyWebSocket = new WebSocket(`${BACKEND_URL.replace("http", "ws")}/lobby/ws/${gameId}`);
    
        lobbyWebSocket.onopen = () => console.log("Lobby WebSocket verbunden.");
        
        lobbyWebSocket.onmessage = async (event) => {
            const data = JSON.parse(event.data);
            console.log("Lobby Nachricht erhalten:", data);
    
            if (data.type === "lobby_update") {
                updateLobbies([data]);
            }
    
            if (data.type === "game_start") {
                console.log("Spiel gestartet, navigiere zur Spielseite...");
                connectGameWebSocket(data.game_id);
                navigate(`/game/${data.game_id}`);
            }
        };
    
        lobbyWebSocket.onclose = () => console.log("Lobby WebSocket geschlossen.");
        setLobbySocket(lobbyWebSocket);
    }; 

    const createLobby = async (userId: string, username: string) => {
        const token = secureLocalStorage.getItem("access_token");
    
        try {
            const response = await axios.post(`${BACKEND_URL}/lobby/create`, { user_id: userId, username }, {
                headers: { Authorization: `Bearer ${token}` }
            });
    
            const gameId = response.data.game_id;
            await listLobbies();
            connectLobbyWebSocket(gameId);
            console.log("Aktiver WebSocket nach createLobby:", lobbySocket);
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
            connectLobbyWebSocket(gameId);
    }

    const leaveLobby = async (gameId: string, userId: string) => {
        await axios.post(`${BACKEND_URL}/lobby/leave/${gameId}/${userId}`);
        await listLobbies();
        lobbySocket?.close();
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

    const startGame = async (gameId: string, userId: string) => {
        const token = secureLocalStorage.getItem("access_token");
        const response = await fetch(`${BACKEND_URL}/game/start_game/${gameId}/${userId}`, {
            method: "POST",
            headers: { Authorization: `Bearer ${token}` },
        });

        const data = await response.json();
        if (data) {
            updateGameState(data);

            setTimeout(() => {
                connectLobbyWebSocket(gameId);
            }, 500);
        }
    };

    useEffect(() => {
        return () => {
            lobbySocket?.close();
        };
    }, []);

    return { createLobby, listLobbies, joinLobby, leaveLobby, setPlayerColor, setPlayerStatus, startGame, connectLobbyWebSocket };
    
}
