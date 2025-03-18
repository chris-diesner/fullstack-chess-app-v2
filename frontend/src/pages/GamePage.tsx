import React, { useEffect } from "react";
import ChessGameComponent from "../components/ChessGame";
import { GameProvider, useGame } from "../components/hooks/GameHooks";
import { useParams } from "react-router-dom";

const GamePageContent: React.FC = () => {
  const { gameId } = useParams<{ gameId: string }>();
  const { connectGameWebSocket } = useGame();

  useEffect(() => {
    if (gameId) {
      connectGameWebSocket(gameId);
    }
  }, [gameId]);

  return <ChessGameComponent />;
};

const GamePage: React.FC = () => (
  <GameProvider>
    <GamePageContent />
  </GameProvider>
);

export default GamePage;
