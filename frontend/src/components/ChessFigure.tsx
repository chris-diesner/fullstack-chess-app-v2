import { useDrag } from "react-dnd";
import { Figure } from "../models/Figure";

type Props = {
  figure: Figure;
};

const ChessFigure = ({ figure }: Props) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "FIGURE",
    item: { position: figure.position },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }));

  return (
    <img
      ref={drag}
      src={`/assets/${figure.color}_${figure.type}.png`}
      alt={figure.type}
      className="chess-figure"
      style={{ opacity: isDragging ? 0.5 : 1 }}
    />
  );
};

export default ChessFigure;