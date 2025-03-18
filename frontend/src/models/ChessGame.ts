import { User } from "./User";
import { ChessBoard } from "./ChessBoard";
import { PlayerColor } from "./User";
import { Figure } from "./Figure";

export enum GameStatus {
    RUNNING = "running",
    ENDED = "ended",
    ABORTED = "aborted"
  }

  export interface MoveData {
    figure: Figure;
    start: [number, number];
    end: [number, number];
    twoSquarePawnMove: boolean;
}

export interface ChessGame {
    gameId: string;
    timeStampStart: string;
    playerWhite: User;
    playerBlack: User;
    currentTurn: PlayerColor;
    board: ChessBoard;
    status: GameStatus;
    lastMove?: MoveData;
  }