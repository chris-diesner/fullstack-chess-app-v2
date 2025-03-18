import React from "react";
import ChessBoard from "./ChessBoard";
import { useGame } from "./hooks/GameHooks";

const ChessGameComponent: React.FC = () => {
  const { gameState, makeMove } = useGame();

  if (!gameState) return <div>Lädt...</div>;

  const handleMove = (start: [number, number], end: [number, number]) => {
    makeMove(gameState.gameId, gameState.currentTurn, start, end);
  };

  return (
    <div>
      <h2>Spielstatus: {gameState.status}</h2>
      <ChessBoard board={gameState.board} onMove={handleMove} />
    </div>
  );
};

export default ChessGameComponent;
