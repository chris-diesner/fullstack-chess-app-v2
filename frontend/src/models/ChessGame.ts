import { User } from "./User";
import { ChessBoard } from "./ChessBoard";
import { PlayerColor } from "./User";

export enum GameStatus {
    RUNNING = "running",
    ENDED = "ended",
    ABORTED = "aborted"
  }

export interface MoveData {
  start: [number, number];
  end: [number, number];
}

export interface ChessGame {
    game_id: string;
    time_stamp_start: string;
    player_white: User;
    player_black: User;
    current_turn: PlayerColor;
    board: ChessBoard;
    status: GameStatus;
    last_move?: MoveData;
  }