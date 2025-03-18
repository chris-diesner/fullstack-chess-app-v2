import React, { useState } from "react";
import { ChessBoard as BoardModel } from "../models/ChessBoard";
import "../styles/ChessBoard.css";

interface ChessBoardProps {
  board: BoardModel;
  onMove: (start: [number, number], end: [number, number]) => void;
}

const ChessBoard: React.FC<ChessBoardProps> = ({ board, onMove }) => {
  const [selectedSquare, setSelectedSquare] = useState<[number, number] | null>(null);
  
  const files = ["a", "b", "c", "d", "e", "f", "g", "h"];
  const ranks = ["8", "7", "6", "5", "4", "3", "2", "1"];

  const handleSquareClick = (row: number, col: number) => {
    if (!selectedSquare) {
      setSelectedSquare([row, col]);
    } else {
      onMove(selectedSquare, [row, col]);
      setSelectedSquare(null);
    }
  };

  return (
    <div className="chess-container">
      {/* Obere Koordinaten */}
      <div className="coordinates">
        <div className="corner"></div>
        {files.map((file) => (
          <div key={file} className="file">{file}</div>
        ))}
        <div className="corner"></div>
      </div>

      <div className="board-container">
        {/* Linke Zahlen */}
        <div className="rank-container">
          {ranks.map((rank) => (
            <div key={rank} className="rank">{rank}</div>
          ))}
        </div>

        {/* Schachbrett */}
        <div className="chess-board">
          {board.squares.map((row, rowIndex) =>
            row.map((figure, colIndex) => (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={`square ${selectedSquare?.[0] === rowIndex && selectedSquare?.[1] === colIndex ? "selected" : ""} ${((rowIndex + colIndex) % 2 === 0 ? "light" : "dark")}`}
                onClick={() => handleSquareClick(rowIndex, colIndex)}
              >
                {figure ? <img src={figure.imagePath} alt={figure.name} /> : ""}
              </div>
            ))
          )}
        </div>

        {/* Rechte Zahlen */}
        <div className="rank-container">
          {ranks.map((rank) => (
            <div key={rank} className="rank">{rank}</div>
          ))}
        </div>
      </div>

      {/* Untere Koordinaten */}
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
