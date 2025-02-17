import { useEffect, useState, useRef } from "react";
import { Figure } from "../models/Figure";
import "../styles/chessboard.css";
import ChessSquare from "./ChessSquare";
import ChessModal from "./ChessModal";

type Props = {
  gameId: string | null;
  onBoardChange: (board: (Figure | null)[][]) => void;
};

const ChessBoard = ({ gameId, onBoardChange }: Props) => {
  const [board, setBoard] = useState<(Figure | null)[][]>(Array(8).fill(Array(8).fill(null)));
  const gameIdRef = useRef<string | null>(gameId);
  const [showModal, setShowModal] = useState<boolean>(false);
  const [modalMessage, setModalMessage] = useState<string | null>(null);

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  useEffect(() => {
    if (!gameId) {
      return;
    }

    gameIdRef.current = gameId;

    fetch(`${BACKEND_URL}/game/${gameId}/board`)
      .then((response) => response.json())
      .then((data) => {
        const newBoard = data.board.map((row: (Figure | null)[]) =>
          row.map((fig) => (fig ? new Figure(fig.type, fig.color, fig.position) : null))
        );
        setBoard(newBoard);
        onBoardChange(newBoard);
      })
      .catch((err) => console.error("Fehler beim Laden des Schachbretts:", err));
  }, [gameId, onBoardChange, BACKEND_URL]);

  const handleMove = (from: string, to: string) => {
    const currentGameId = gameIdRef.current;

    if (!currentGameId) {
      return;
    }

    fetch(`${BACKEND_URL}/game/${currentGameId}/move?start_pos=${from}&end_pos=${to}`, { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then(async(response) => {
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }
        return response.json();
      })
      .then((data) => {
        setBoard(data.game_state.board);
        onBoardChange(data.game_state.board);
        const status = data.game_state.check_mate_status; 
        console.log(status);
        if (status === "check") {
          setModalMessage("Achtung: Schach!");
          setShowModal(true);
        } else if (status === "mate") {
          setModalMessage("Spiel vorbei: Schachmatt!");
          setShowModal(true);
        } else if (status === "stalemate") {
          setModalMessage("Spiel vorbei: Patt!");
          setShowModal(true);
        }
      })
  
      .catch((err) => {
        console.error("Fehler beim Zug:", err.message);
        setModalMessage(err.message);
        setShowModal(true);
      });
  };

  const x = ["a", "b", "c", "d", "e", "f", "g", "h"];
  const y = ["8", "7", "6", "5", "4", "3", "2", "1"];

  return (
    <div className="board-container">
      <ChessModal show={showModal} handleClose={() => setShowModal(false)} message={modalMessage || ""} />
      
      <div className="coordinates-left">
        {y.map((y, index) => (
          <div key={index} className="y-label">{y}</div>
        ))}
      </div>

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

      <div className="coordinates-bottom">
        {x.map((x, index) => (
          <div key={index} className="x-label">{x}</div>
        ))}
      </div>
    </div>
  );
};

export default ChessBoard;
