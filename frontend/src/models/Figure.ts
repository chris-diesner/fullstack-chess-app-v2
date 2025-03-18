export class Figure {
    name: string;
    color: "white" | "black";
    position: string;
    image_path: string;
  
    constructor(type: string, color: "white" | "black", position: string, image_path: string) {
      this.name = type;
      this.color = color;
      this.position = position;
      this.image_path = image_path;
    }
  }
  
  export class King extends Figure {
    constructor(color: "white" | "black", position: string, image_path: string) {
      super("king", color, position, image_path);
    }
  }
  
  export class Queen extends Figure {
    constructor(color: "white" | "black", position: string, image_path: string) {
      super("queen", color, position, image_path);
    }
  }
  
  export class Rook extends Figure {
    constructor(color: "white" | "black", position: string, image_path: string) {
      super("rook", color, position, image_path);
    }
  }
  
  export class Bishop extends Figure {
    constructor(color: "white" | "black", position: string, image_path: string) {
      super("bishop", color, position, image_path);
    }
  }
  
  export class Knight extends Figure {
    constructor(color: "white" | "black", position: string, image_path: string) {
      super("knight", color, position, image_path);
    }
  }
  
  export class Pawn extends Figure {
    constructor(color: "white" | "black", position: string, image_path: string) {
      super("pawn", color, position, image_path);
    }
  }
  