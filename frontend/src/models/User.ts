import { Figure } from './Figure';

export enum PlayerColor {
  WHITE = "white",
  BLACK = "black",
}

export enum PlayerStatus {
  READY = "ready",
  NOT_READY = "not_ready",
}

export type User = {
  user_id: string;
  username: string;
  color?: PlayerColor;  
  status?: PlayerStatus;
  capturedFigures: Figure[];
  moveHistory: string[];
};
