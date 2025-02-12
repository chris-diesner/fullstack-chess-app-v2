import { useState } from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import ChessBoard from "../components/ChessBoard";
import "../styles/chessboard.css";

const ChessGame = () => {
  const [gameId, setGameId] = useState<string | null>(null);
  const [isBoardSet, setIsBoardSet] = useState<boolean>(false);

  const startNewGame = () => {
    console.log(isBoardSet)
    fetch("http://localhost:8000/game/new", { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        setGameId(data.game_id);
        setIsBoardSet(true);
      })
      .catch((err) => console.error("Fehler beim Starten eines neuen Spiels:", err));
  };

  return (
    <div className="game-container">
      <div className="sidebar">
        <button onClick={startNewGame}>Neues Spiel starten</button>
        {gameId && <p>Spiel-ID: {gameId}</p>}
      </div>

      {/* ✅ DndProvider um das ChessBoard gelegt */}
      <DndProvider backend={HTML5Backend}>
        <ChessBoard gameId={gameId} />
      </DndProvider>
    </div>
  );
};

export default ChessGame;
