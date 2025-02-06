import { useEffect, useState } from "react";
import { Figure, King, Queen, Rook, Bishop, Knight, Pawn } from "../models/Figure";
import "../styles/chessboard.css";

const ChessBoard = () => {
  const [board, setBoard] = useState<(Figure | null)[][]>(Array(8).fill(Array(8).fill(null)));

  useEffect(() => {
    fetch("http://localhost:10000/game/board")
      .then((res) => res.json())
      .then((data) => {
        const newBoard = data.board.map((row: { type: string; color: "white" | "black"; position: string }[]) =>
          row.map((fig) => (fig ? createFigure(fig.type, fig.color, fig.position) : null))
        );
        setBoard(newBoard);
      })
      .catch((err) => console.error("Fehler beim Laden des Schachbretts:", err));
  }, []);

  return (
    <div className="chessboard">
      {board.map((row, rowIndex) =>
        row.map((figure, colIndex) => (
          <div key={`${rowIndex}-${colIndex}`} className={`square ${(rowIndex + colIndex) % 2 === 0 ? "light" : "dark"}`}>
            {figure ? figure.getUnicode() : ""}
          </div>
        ))
      )}
    </div>
  );
};

const createFigure = (type: string, color: "white" | "black", position: string): Figure => {
  switch (type) {
    case "king":
      return new King(color, position);
    case "queen":
      return new Queen(color, position);
    case "rook":
      return new Rook(color, position);
    case "bishop":
      return new Bishop(color, position);
    case "knight":
      return new Knight(color, position);
    case "pawn":
      return new Pawn(color, position);
    default:
      throw new Error(`Unbekannte Figur: ${type}`);
  }
};

export default ChessBoard;
