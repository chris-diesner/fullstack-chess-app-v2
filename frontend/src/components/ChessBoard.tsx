import React, { useState } from "react";
import { ChessBoard as BoardModel } from "../models/ChessBoard";
import { useGame } from "./hooks/GameHooks";
import { useUser } from "./hooks/UserHooks";
import "../styles/ChessBoard.css";

interface ChessBoardProps {
  board: BoardModel;
}

const ChessBoard: React.FC<ChessBoardProps> = ({ board }) => {
  const [selectedSquare, setSelectedSquare] = useState<[number, number] | null>(null);
  const { gameState, makeMove } = useGame();
  const { user } = useUser();
  
  const files = ["a", "b", "c", "d", "e", "f", "g", "h"];
  const ranks = ["8", "7", "6", "5", "4", "3", "2", "1"];

  const handleSquareClick = (row: number, col: number) => {
    if (!gameState || !gameState.game_id || !user?.user_id) {
      return;
    }
  
    if (!selectedSquare) {
      if (board.squares[row][col]) { 
        setSelectedSquare([row, col]); 
      }
    } else {
  
      makeMove(
        gameState.game_id,
        user?.user_id,
        selectedSquare,
        [row, col],
      );
  
      setSelectedSquare(null);
    }
  };

  return (
    <div className="chess-container">
      <div className="coordinates">
        <div className="corner"></div>
        {files.map((file) => (
          <div key={file} className="file">{file}</div>
        ))}
        <div className="corner"></div>
      </div>

      <div className="board-container">
        <div className="rank-container">
          {ranks.map((rank) => (
            <div key={rank} className="rank">{rank}</div>
          ))}
        </div>

        <div className="chess-board">
          {board.squares.map((row, rowIndex) =>
            row.map((figure, colIndex) => (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={`square ${selectedSquare?.[0] === rowIndex && selectedSquare?.[1] === colIndex ? "selected" : ""} ${((rowIndex + colIndex) % 2 === 0 ? "light" : "dark")}`}
                onClick={() => handleSquareClick(rowIndex, colIndex)}
              >
                {figure ? <img src={`/assets/${figure.color}_${figure.name}.png`} alt={figure.name} /> : ""}
              </div>
            ))
          )}
        </div>

        <div className="rank-container">
          {ranks.map((rank) => (
            <div key={rank} className="rank">{rank}</div>
          ))}
        </div>
      </div>

      <div className="coordinates">
        <div className="corner"></div>
        {files.map((file) => (
          <div key={file} className="file">{file}</div>
        ))}
        <div className="corner"></div>
      </div>
    </div>
  );
};

export default ChessBoard;
