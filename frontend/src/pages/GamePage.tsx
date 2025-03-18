import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { ChessGame } from "../models/ChessGame";
import GameHooks from "../components/hooks/GameHooks";
import ChessBoard from "../components/ChessBoard";
import "../styles/ChessBoard.css";

const GamePage: React.FC = () => {
    const { gameId } = useParams<{ gameId: string }>();
    const [gameState, setGameState] = useState<ChessGame | null>(null);
    const { connectGameWebSocket } = GameHooks(() => {}, setGameState);

    useEffect(() => {
        if (gameId) {
            connectGameWebSocket(gameId);
        }
    }, [gameId]);

    useEffect(() => {
        if (gameState) {
            console.log("🔍 GameState erhalten:", gameState);
            console.log("📋 Board:", gameState.board);
            console.log("🟦 Squares:", gameState.board?.squares);
        }
    }, [gameState]);

    return (
        <div className="chess-game-container">
            {gameState ? (
                <>
                    <div className="players">
                        <div className="player white">
                            <h3>⚪ {gameState.player_white.username || "Weiß"}</h3>
                        </div>
                        <div className="player black">
                            <h3>⚫ {gameState.player_black.username || "Schwarz"}</h3>
                        </div>
                    </div>
                    <ChessBoard gameState={gameState} />
                </>
            ) : (
                <p>⏳ Lade Spiel...</p>
            )}
        </div>
    );
};

export default GamePage;