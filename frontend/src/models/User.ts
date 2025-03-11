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
  id: string;
  username: string;
  color?: PlayerColor;  // Optional, falls der User in einer Lobby ist
  status?: PlayerStatus;
  capturedFigures: Figure[];
  moveHistory: string[];
};
