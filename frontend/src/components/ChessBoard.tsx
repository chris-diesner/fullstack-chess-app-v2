import { useEffect, useState } from "react";
import { Figure } from "../models/Figure";
import "../styles/chessboard.css";
import ChessSquare from "./ChessSquare";

const ChessBoard = () => {
  const [board, setBoard] = useState<(Figure | null)[][]>(Array(8).fill(Array(8).fill(null)));
  const gameId = "1234"; 

  useEffect(() => {
    fetch(`http://localhost:10000/game/${gameId}/board`)
      .then((response) => response.json())
      .then((data) => {
        const newBoard = data.board.map((row: (Figure | null)[]) =>
          row.map((fig) => (fig ? new Figure(fig.type, fig.color, fig.position) : null))
        );
        setBoard(newBoard);
      })
      .catch((err) => console.error("Fehler beim Laden des Schachbretts:", err));
  }, []);

  const handleMove = (from: string, to: string) => {
    fetch(`http://localhost:10000/game/${gameId}/move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start_pos: from, end_pos: to }),
    })
      .then((response) => response.json())
      .then((data) => setBoard(data.game_state.board))
      .catch((err) => console.error("Fehler beim Zug:", err));
  };

  return (
    <div className="chessboard">
      {board.map((row, rowIndex) =>
        row.map((figure, colIndex) => (
          <ChessSquare
            key={`${rowIndex}-${colIndex}`}
            row={rowIndex}
            col={colIndex}
            figure={figure}
            onMove={handleMove}
          />
        ))
      )}
    </div>
  );
};

export default ChessBoard;
