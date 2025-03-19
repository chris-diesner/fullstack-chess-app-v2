import React, { createContext, useContext, useEffect, useState } from "react";
import { ChessGame } from "../../models/ChessGame";

interface GameContextType {
    gameState: ChessGame | null;
    connectGameWebSocket: (gameId: string) => void;
    makeMove: (gameId: string, userId: string, start: [number, number], end: [number, number]) => void;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

export const GameProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const [gameState, setGameState] = useState<ChessGame | null>(null);
    const [gameSocket, setGameSocket] = useState<WebSocket | null>(null);

    const connectGameWebSocket = (gameId: string) => {
        const socket = new WebSocket(`${BACKEND_URL.replace("http", "ws")}/game/ws/${gameId}`);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === "game_state") {
                setGameState(data.data);
            }
        };

        setGameSocket(socket);
    };

    const makeMove = (gameId: string, userId: string, start: [number, number], end: [number, number]) => {
        if (gameSocket && gameSocket.readyState === WebSocket.OPEN) {
            const moveData = {
                action: "move",
                game_id: gameId,
                start_pos: start,
                end_pos: end,
                user_id: userId,
            };
            gameSocket.send(JSON.stringify(moveData));
        }
    };

    useEffect(() => {
        return () => gameSocket?.close();
    }, []);

    return <GameContext.Provider value={{ gameState, connectGameWebSocket, makeMove }}>
        {children}
    </GameContext.Provider>;
};

export const useGame = () => {
    const context = useContext(GameContext);
    if (!context) {
        throw new Error("useGame must be used within a GameProvider");
    }
    return context;
};
