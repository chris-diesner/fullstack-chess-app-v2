import uuid
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User:
    def __init__(self, username: str, password: str, color):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password_hash = self.hash_password(password)
        self.color = color 
        self.captured_figures = []
        self.move_history = []
        
    def hash_password(self, password: str) -> str:
        return password_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        return password_context.verify(password, self.password_hash)

    def add_captured_piece(self, figure):
        self.captured_figures.append(figure)

    def record_move(self, move):
        self.move_history.append(move)

    def __str__(self):
        return f"Spieler {self.username} ({self.color})"

    def get_captured_pieces_summary(self):
        return ", ".join(f"{piece.name} ({piece.color})" for piece in self.captured_figures)
    
    def choose_promotion(self):
        #queen vor definiert bis user eingabe kommt
        return "queen"