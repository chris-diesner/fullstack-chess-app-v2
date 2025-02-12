import { useEffect, useState } from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import ChessBoard from "../components/ChessBoard";
import "../styles/chessboard.css";

type Figure = {
  type: string;
  color: string;
};

const ChessGame = () => {
  const [gameId, setGameId] = useState<string | null>(null);
  const [isBoardSet, setIsBoardSet] = useState<boolean>(false);
  const [boardState, setBoardState] = useState<(Figure | null)[][]>(Array(8).fill(Array(8).fill(null)));
  const [moveHistory, setMoveHistory] = useState<{white_moves: {figure: string, start: string, end: string}[], black_moves: {figure: string, start: string, end: string}[]}>({white_moves: [], black_moves: []});

  const startNewGame = () => {
    console.log(isBoardSet)
    fetch("http://localhost:8000/game/new", { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        setGameId(data.game_id);
        setIsBoardSet(true);
        setMoveHistory({white_moves: [], black_moves: []});
      })
      .catch((err) => console.error("Fehler beim Starten eines neuen Spiels:", err));
  };

  useEffect(() => {
    if (!gameId || !boardState) return;

    const fetchMoveHistory = () => {
      fetch(`http://localhost:8000/game/${gameId}/history`)
        .then((res) => res.json())
        .then((data) => setMoveHistory(data))
        .catch((err) => console.error("Fehler beim Laden der Zug-Historie:", err));
    };

    fetchMoveHistory();
  }, [gameId, boardState]);

  return (
    <div className="game-container">
      <div className="sidebar">
        <button onClick={startNewGame}>Neues Spiel starten</button>
        {gameId && <p>Spiel-ID: {gameId}</p>}
      </div>
      <h3>Zug-Historie</h3>
      <div className="move-list">
  <strong>Weiß:</strong>
  <ul>
    {moveHistory.white_moves.map((move, index) => (
      <li key={`w${index}`}>
        {move.figure} von {move.start.toUpperCase()} nach {move.end.toUpperCase()}
      </li>
    ))}
  </ul>

  <strong>Schwarz:</strong>
  <ul>
    {moveHistory.black_moves.map((move, index) => (
      <li key={`b${index}`}>
        {move.figure} von {move.start.toUpperCase()} nach {move.end.toUpperCase()}
      </li>
    ))}
  </ul>
</div>
      <DndProvider backend={HTML5Backend}>
        <ChessBoard gameId={gameId} onBoardChange={setBoardState} />
      </DndProvider>
    </div>
  );
};

export default ChessGame;
