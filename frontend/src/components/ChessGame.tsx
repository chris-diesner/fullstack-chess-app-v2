import React from "react";
import ChessBoard from "./ChessBoard";
import { useGame } from "./hooks/GameHooks";

const ChessGameComponent: React.FC = () => {
  const { gameState } = useGame();

  if (!gameState) return <div>Lädt...</div>;

  return (
    <div>
      <h2>Spielstatus: {gameState.status}</h2>
      <ChessBoard board={gameState.board} />
    </div>
  );
};

export default ChessGameComponent;
