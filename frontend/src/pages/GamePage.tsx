import React, { useEffect, useState } from "react";
import { ChessGame } from "../models/ChessGame";
import { ChessBoard } from "../models/ChessBoard";
import "../styles/ChessBoard.css";

interface ChessGameProps {
    gameState: ChessGame | null;
}

const GamePage: React.FC<ChessGameProps> = ({ gameState }) => {
    const [board, setBoard] = useState<ChessBoard | null>(null);

    useEffect(() => {
        if (gameState) {
            setBoard(gameState.board);
        }
    }, [gameState]);

    return (
        <div className="chess-game-container">
            <div className="players">
                <div className="player white">
                    <h3>⚪ {gameState?.player_white.username || "Weiß"}</h3>
                </div>
                <div className="player black">
                    <h3>⚫ {gameState?.player_black.username || "Schwarz"}</h3>
                </div>
            </div>

            <div className="chess-board">
                {board?.squares.map((row, rowIndex) => (
                    <div key={rowIndex} className="row">
                        {row.map((square, colIndex) => (
                            <div 
                                key={`${rowIndex}-${colIndex}`} 
                                className={`square ${(rowIndex + colIndex) % 2 === 0 ? "light" : "dark"}`}
                            >
                                {square.figure && (
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
        </div>
    );
};

export default GamePage;
