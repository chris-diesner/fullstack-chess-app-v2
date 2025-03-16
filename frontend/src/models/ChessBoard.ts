import { Figure } from "./Figure";

export interface ChessBoard {
    squares: { position: [number, number]; figure: Figure | null }[][];
}
