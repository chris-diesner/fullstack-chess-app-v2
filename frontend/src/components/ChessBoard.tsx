import { ChessGame } from "../models/ChessGame";
import ChessSquare from "./ChessSquare";

type Props = {
  gameState: ChessGame;
};

const ChessBoard = ({ gameState }: Props) => {
  return (
    <div className="chess-board">
      {gameState.board.squares.map((row, rowIndex) => (
        <div key={rowIndex} className="row">
          {row.map((square, colIndex) => (
            <ChessSquare key={`${rowIndex}-${colIndex}`} row={rowIndex} col={colIndex} figure={square?.figure || null} />
          ))}
        </div>
      ))}
    </div>
  );
};

export default ChessBoard;
