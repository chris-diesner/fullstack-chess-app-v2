import { useDrop } from "react-dnd";
import ChessFigure from "./ChessFigure.tsx";
import { Figure } from "../models/Figure";

type Props = {
  row: number;
  col: number;
  figure: Figure | null;
  onMove: (from: string, to: string) => void;
};

const ChessSquare = ({ row, col, figure, onMove }: Props) => {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: "FIGURE",
    drop: (item: { position: string }) => onMove(item.position, `${String.fromCharCode(97 + col)}${8 - row}`),
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  }));

  return (
    <div ref={drop} className={`square ${(row + col) % 2 === 0 ? "light" : "dark"} ${isOver ? "highlight" : ""}`}>
      {figure && <ChessFigure figure={figure} />}
    </div>
  );
};

export default ChessSquare;