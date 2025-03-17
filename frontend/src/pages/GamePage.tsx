import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { ChessGame } from "../models/ChessGame";
import GameHooks from "../components/hooks/GameHooks";
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

                    <div className="chess-board">
                        {gameState.board.squares.map((row, rowIndex) => (
                            <div key={rowIndex} className="row">
                                {row.map((square, colIndex) => (
                                    <div 
                                        key={`${rowIndex}-${colIndex}`} 
                                        className={`square ${(rowIndex + colIndex) % 2 === 0 ? "light" : "dark"}`}
                                    >
                                        {square && square.figure && (
                                            <img
                                                src={square.figure.image_path}
                                                alt={square.figure.type} 
                                                className="chess-piece"
                                            />
                                        )}
                                    </div>
                                ))}
                            </div>
                        ))}
                    </div>
                </>
            ) : (
                <p>⏳ Lade Spiel...</p>
            )}
        </div>
    );
};

export default GamePage;
