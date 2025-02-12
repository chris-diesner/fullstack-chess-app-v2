import { useEffect, useState, useRef } from "react";
import { Figure } from "../models/Figure";
import "../styles/chessboard.css";
import ChessSquare from "./ChessSquare";

type Props = {
  gameId: string | null;
};

const ChessBoard = ({ gameId }: Props) => {
  const [board, setBoard] = useState<(Figure | null)[][]>(Array(8).fill(Array(8).fill(null)));
  const gameIdRef = useRef<string | null>(gameId); // ✅ Speichert immer die aktuelle gameId

  console.log("🔍 ChessBoard.tsx gerendert mit gameId:", gameId);

  useEffect(() => {
    if (!gameId) {
      console.error("🚨 Fehler: gameId ist null in ChessBoard.tsx!");
      return;
    }

    gameIdRef.current = gameId; // ✅ `useRef` wird bei jeder gameId-Änderung aktualisiert!

    fetch(`http://localhost:8000/game/${gameId}/board`)
      .then((response) => response.json())
      .then((data) => {
        console.log("📥 Board-Daten erhalten:", data);
        const newBoard = data.board.map((row: (Figure | null)[]) =>
          row.map((fig) => (fig ? new Figure(fig.type, fig.color, fig.position) : null))
        );
        setBoard(newBoard);
      })
      .catch((err) => console.error("Fehler beim Laden des Schachbretts:", err));
  }, [gameId]);

  const handleMove = (from: string, to: string) => {
    const currentGameId = gameIdRef.current; // ✅ Holt IMMER die aktuelle gameId

    if (!currentGameId) {
      console.error("Fehler: gameId ist null!");
      return;
    }

    fetch(`http://localhost:8000/game/${currentGameId}/move?start_pos=${from}&end_pos=${to}`, { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
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
            onMove={handleMove} // ✅ Jetzt bekommt ChessSquare IMMER die aktuelle gameId
          />
        ))
      )}
    </div>
  );
};

export default ChessBoard;
