import { Figure } from './Figure';

export type User = {
  id: string;
  username: string;
  capturedFigures: Figure[];
  moveHistory: string[];
}