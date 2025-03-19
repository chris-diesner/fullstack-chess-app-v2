export enum FigureColor {
  WHITE = "white",
  BLACK = "black"
}

export interface Figure {
  id: string;
  name: string;
  color: FigureColor;
  position: [number, number];
}

export class Pawn implements Figure {
  id: string;
  name: string = "pawn";
  color: FigureColor;
  position: [number, number];

  constructor(id: string, color: FigureColor, position: [number, number]) {
      this.id = id;
      this.color = color;
      this.position = position;
  }
}

export class Rook implements Figure {
  id: string;
  name: string = "rook";
  color: FigureColor;
  position: [number, number];
  hasMoved: boolean = false;

  constructor(id: string, color: FigureColor, position: [number, number]) {
      this.id = id;
      this.color = color;
      this.position = position;
  }
}

export class Knight implements Figure {
  id: string;
  name: string = "knight";
  color: FigureColor;
  position: [number, number];

  constructor(id: string, color: FigureColor, position: [number, number]) {
      this.id = id;
      this.color = color;
      this.position = position;
  }
}

export class Bishop implements Figure {
  id: string;
  name: string = "bishop";
  color: FigureColor;
  position: [number, number];

  constructor(id: string, color: FigureColor, position: [number, number]) {
      this.id = id;
      this.color = color;
      this.position = position;
  }
}

export class Queen implements Figure {
  id: string;
  name: string = "queen";
  color: FigureColor;
  position: [number, number];

  constructor(id: string, color: FigureColor, position: [number, number]) {
      this.id = id;
      this.color = color;
      this.position = position;
  }
}

export class King implements Figure {
  id: string;
  name: string = "king";
  color: FigureColor;
  position: [number, number];
  hasMoved: boolean = false;

  constructor(id: string, color: FigureColor, position: [number, number]) {
      this.id = id;
      this.color = color;
      this.position = position;
  }
}
