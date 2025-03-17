import axios from 'axios';
import { useCallback, useEffect, useState } from 'react';
import secureLocalStorage from "react-secure-storage";
import { Lobby } from '../../models/Lobby';
import { ChessGame } from '../../models/ChessGame';
import { MoveData } from '../../models/ChessGame';

export default function GameHooks(
    updateLobbies: (lobbies: Lobby[]) => void,
    updateGameState: (gameState: ChessGame | null) => void
) {
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const [lobbySocket, setLobbySocket] = useState<WebSocket | null>(null);
    const [gameSocket, setGameSocket] = useState<WebSocket | null>(null);

    const connectLobbyWebSocket = (gameId: string) => {
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
        setLobbySocket(webSocket);
    };

    const connectGameWebSocket = (gameId: string) => {
        const webSocket = new WebSocket(`${BACKEND_URL.replace("http", "ws")}/game/ws/${gameId}`);

        webSocket.onopen = () => console.log("Game WebSocket connected.");
        webSocket.onmessage = (event) => {
            console.log("Game Update:", event.data);
            const data = JSON.parse(event.data);
            if (data.type === "game_state") {
                updateGameState(data.data);
            } else if (data.type === "error") {
                alert(`Fehler: ${data.message}`);
            }
        };
        webSocket.onclose = () => console.log("Game WebSocket closed.");

        setGameSocket(webSocket);
    };
    
    const makeMove = (gameId: string, userId: string, moveData: MoveData) => {
        if (gameSocket && gameSocket.readyState === WebSocket.OPEN) {
            const message = {
                action: "move",
                game_id: gameId,
                user_id: userId,
                start_pos: moveData.start,
                end_pos: moveData.end,
            };
            gameSocket.send(JSON.stringify(message));
        } else {
            console.error("WebSocket nicht verbunden!");
        }
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
            connectGameWebSocket(gameId);
        }
    };

    useEffect(() => {
        return () => {
            lobbySocket?.close();
            gameSocket?.close();
        };
    }, []);

    return { makeMove, createLobby, listLobbies, joinLobby, leaveLobby, setPlayerColor, setPlayerStatus, startGame, connectLobbyWebSocket, connectGameWebSocket };
    
}
