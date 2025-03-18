import { Figure } from "./Figure";

export class ChessBoard {
    squares: (Figure | null)[][];

    constructor() {
        this.squares = Array(8).fill(null).map(() => Array(8).fill(null));
    }

    static createEmptyBoard(): ChessBoard {
        return new ChessBoard();
    }
}
