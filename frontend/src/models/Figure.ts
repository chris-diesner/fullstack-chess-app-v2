export class Figure {
    type: string;
    color: "white" | "black";
    position: string;
  
    constructor(type: string, color: "white" | "black", position: string) {
      this.type = type;
      this.color = color;
      this.position = position;
    }
  
    getUnicode(): string {
      const unicodeFigures: Record<string, string> = {
        king: this.color === "white" ? "♔" : "♚",
        queen: this.color === "white" ? "♕" : "♛",
        rook: this.color === "white" ? "♖" : "♜",
        bishop: this.color === "white" ? "♗" : "♝",
        knight: this.color === "white" ? "♘" : "♞",
        pawn: this.color === "white" ? "♙" : "♟",
      };
      return unicodeFigures[this.type] || "?";
    }
  }
  
  export class King extends Figure {
    constructor(color: "white" | "black", position: string) {
      super("king", color, position);
    }
  }
  
  export class Queen extends Figure {
    constructor(color: "white" | "black", position: string) {
      super("queen", color, position);
    }
  }
  
  export class Rook extends Figure {
    constructor(color: "white" | "black", position: string) {
      super("rook", color, position);
    }
  }
  
  export class Bishop extends Figure {
    constructor(color: "white" | "black", position: string) {
      super("bishop", color, position);
    }
  }
  
  export class Knight extends Figure {
    constructor(color: "white" | "black", position: string) {
      super("knight", color, position);
    }
  }
  
  export class Pawn extends Figure {
    constructor(color: "white" | "black", position: string) {
      super("pawn", color, position);
    }
  }
  