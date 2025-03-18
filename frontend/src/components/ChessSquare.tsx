import { Figure } from "../models/Figure";

type Props = {
  row: number;
  col: number;
  figure: Figure | null;
};

const ChessSquare = ({ row, col, figure }: Props) => {
  return (
    <div className={`square ${(row + col) % 2 === 0 ? "light" : "dark"}`}>
      {figure && (
        <img
          src={`/assets/${figure.color}_${figure.name.toLowerCase()}.png`} // ✅ Korrekte Pfadangabe
          alt={figure.name}
          className="chess-piece"
        />
      )}
    </div>
  );
};

export default ChessSquare;
