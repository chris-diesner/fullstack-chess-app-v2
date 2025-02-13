import unittest
from typing import List, Optional
from figures.figure import Figure, Bishop, Rook, Queen, Pawn, King, Knight

class TestKing(unittest.TestCase):
    def setUp(self):
        self.board: List[List[Optional[Figure]]] = [[None for _ in range(8)] for _ in range(8)]  
        self.white_king = King("white", (0, 4))
        self.black_king = King("black", (7, 4))

    def test_valid_king_moves_should_return_true(self):
        self.assertTrue(self.white_king.is_move_valid((0, 4), (1, 4), self.board))
        self.assertTrue(self.white_king.is_move_valid((0, 4), (1, 5), self.board))
        self.assertTrue(self.black_king.is_move_valid((7, 4), (6, 4), self.board))

    def test_invalid_king_moves_should_return_false(self):
        self.assertFalse(self.white_king.is_move_valid((0, 4), (2, 4), self.board))
        self.assertFalse(self.black_king.is_move_valid((7, 4), (5, 4), self.board))

    def test_capture_opponent_should_return_true(self):
        self.board[1][4] = King("black", (1, 4))
        self.assertTrue(self.white_king.is_move_valid((0, 4), (1, 4), self.board))

    def test_out_of_bounds_move_should_return_false(self):
        self.assertFalse(self.white_king.is_move_valid((0, 4), (-1, 4), self.board))

class TestRook(unittest.TestCase):
    def setUp(self):
        self.board: List[List[Optional[Figure]]] = [[None for _ in range(8)] for _ in range(8)]
        self.white_rook = Rook("white", (0, 0))
        self.black_rook = Rook("black", (7, 7))

    def test_valid_move_horizontal_should_return_true(self):
        self.assertTrue(self.black_rook.is_move_valid((0, 7), (0, 0), self.board))

    def test_valid_vertical_move_should_return_true(self):
        self.assertTrue(self.black_rook.is_move_valid((7, 7), (0, 7), self.board))

    def test_blocked_move_should_return_false(self):
        self.board[0][4] = Rook("white", (0, 4))
        self.assertFalse(self.white_rook.is_move_valid((0, 0), (0, 7), self.board))

    def test_capture_opponent_should_return_true(self):
        self.board[0][7] = Rook("black", (0, 7))
        self.assertTrue(self.white_rook.is_move_valid((0, 0), (0, 7), self.board))

    def test_invalid_diagonal_move_should_return_false(self):
        self.assertFalse(self.white_rook.is_move_valid((0, 0), (7, 7), self.board))

    def test_out_of_bounds_move_should_return_false(self):
        self.assertFalse(self.white_rook.is_move_valid((0, 3), (8, 3), self.board))


class TestQueen(unittest.TestCase):
    def setUp(self):
        self.board: List[List[Optional[Figure]]] = [[None for _ in range(8)] for _ in range(8)]
        self.white_queen = Queen("white", (0, 3))
        self.black_queen = Queen("black", (7, 3))

    def test_valid_horizontal_move_should_return_true(self):
        self.assertTrue(self.white_queen.is_move_valid((0, 3), (0, 7), self.board))
        self.assertTrue(self.black_queen.is_move_valid((7, 3), (7, 0), self.board))

    def test_valid_vertical_move_should_return_true(self):
        self.assertTrue(self.white_queen.is_move_valid((0, 3), (7, 3), self.board))
        self.assertTrue(self.black_queen.is_move_valid((7, 3), (0, 3), self.board))

    def test_valid_diagonal_move_should_return_true(self):
        self.assertTrue(self.white_queen.is_move_valid((0, 3), (4, 7), self.board))
        self.assertTrue(self.black_queen.is_move_valid((7, 3), (3, 7), self.board))

    def test_blocked_horizontal_move_should_return_false(self):
        self.board[0][5] = Queen("white", (0, 5))
        self.assertFalse(self.white_queen.is_move_valid((0, 3), (0, 7), self.board))

    def test_blocked_diagonal_move_should_return_false(self):
        self.board[4][4] = Queen("white", (4, 4))
        self.assertFalse(self.white_queen.is_move_valid((0, 3), (7, 0), self.board))

    def test_capture_opponent_should_return_true(self):
        self.board[0][7] = Queen("black", (0, 7))
        self.assertTrue(self.white_queen.is_move_valid((0, 3), (0, 7), self.board))

    def test_invalid_move_should_return_false(self):
        self.assertFalse(self.white_queen.is_move_valid((0, 3), (1, 5), self.board))

    def test_out_of_bounds_move_should_return_false(self):
        self.assertFalse(self.white_queen.is_move_valid((0, 3), (8, 3), self.board))
        self.assertFalse(self.white_queen.is_move_valid((0, 3), (-1, 3), self.board))

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.board: List[List[Optional[Figure]]] = [[None for _ in range(8)] for _ in range(8)]
        self.white_pawn = Pawn("white", (6, 1))
        self.black_pawn = Pawn("black", (1, 1))

    def test_single_forward_move_should_return_true(self):
        result = self.white_pawn.is_move_valid((6, 1), (5, 1), self.board)
        self.assertTrue(result)
        result = self.black_pawn.is_move_valid((1, 1), (2, 1), self.board)
        self.assertTrue(result)

    def test_double_forward_move_first_turn_should_return_true(self):
        result = self.white_pawn.is_move_valid((6, 1), (4, 1), self.board)
        self.assertTrue(result)

        result = self.black_pawn.is_move_valid((1, 1), (3, 1), self.board)
        self.assertTrue(result)

    def test_blocked_double_forward_move_should_return_false(self):
        self.board[5][1] = Pawn("white", (5, 1))
        result = self.white_pawn.is_move_valid((6, 1), (4, 1), self.board)
        self.assertFalse(result)

    def test_diagonal_capture_should_return_true(self):
        self.board[5][2] = Pawn("black", (5, 2))
        result = self.white_pawn.is_move_valid((6, 1), (5, 2), self.board)
        self.assertTrue(result)

    def test_invalid_diagonal_capture_empty_field_should_return_false(self):
        result = self.white_pawn.is_move_valid((6, 1), (5, 2), self.board)
        self.assertFalse(result)

    def test_invalid_diagonal_capture_own_piece_should_return_false(self):
        self.board[5][2] = Pawn("white", (5, 2))
        result = self.white_pawn.is_move_valid((6, 1), (5, 2), self.board)
        self.assertFalse(result)

    def test_blocked_forward_move(self):
        self.board[5][1] = Pawn("white", (5, 1))
        result = self.white_pawn.is_move_valid((6, 1), (5, 1), self.board)
        self.assertFalse(result)

    def test_out_of_bounds_move_should_return_false(self):
        result = self.white_pawn.is_move_valid((6, 1), (8, 1), self.board)
        self.assertFalse(result)

        result = self.white_pawn.is_move_valid((6, 1), (-1, 1), self.board)
        self.assertFalse(result)

    def test_invalid_direction_should_return_false(self):
        result = self.white_pawn.is_move_valid((6, 1), (7, 1), self.board)
        self.assertFalse(result)

    def test_capture_own_piece_should_return_false(self):
        self.board[5][2] = Rook("white", (5, 2))
        result = self.white_pawn.is_move_valid((6, 1), (5, 2), self.board)
        self.assertFalse(result)
        
class TestBishop(unittest.TestCase):
    def setUp(self):
        self.board: List[List[Optional[Figure]]] = [[None for _ in range(8)] for _ in range(8)]
        self.white_bishop = Bishop("white", (0, 2))
        self.black_bishop = Bishop("black", (7, 5))
        
    def test_valid_move_diagonal_should_return_true(self):
        self.assertTrue(self.white_bishop.is_move_valid((0, 2), (2, 0), self.board))
        self.assertTrue(self.black_bishop.is_move_valid((7, 5), (5, 7), self.board))
    
    def test_invalid_move_not_diagonal_should_return_false(self):
        self.assertFalse(self.white_bishop.is_move_valid((0, 2), (0, 0), self.board))
        self.assertFalse(self.black_bishop.is_move_valid((7, 5), (7, 7), self.board))
        
    def test_blocked_move_should_return_false(self):
        self.board[1][1] = Bishop("white", (1, 1))
        self.assertFalse(self.white_bishop.is_move_valid((0, 2), (2, 0), self.board))
        self.board[6][4] = Bishop("black", (6, 4))
        self.assertFalse(self.black_bishop.is_move_valid((7, 5), (5, 3), self.board))
        
    def test_capture_opponent_should_return_true(self):
        self.board[2][0] = Bishop("black", (2, 0))
        self.assertTrue(self.white_bishop.is_move_valid((0, 2), (2, 0), self.board))
        self.board[5][7] = Bishop("white", (5, 7))
        self.assertTrue(self.black_bishop.is_move_valid((7, 5), (5, 7), self.board))
        
    def test_out_of_bounds_move_should_return_false(self):
        self.assertFalse(self.white_bishop.is_move_valid((0, 2), (8, 2), self.board))
        self.assertFalse(self.black_bishop.is_move_valid((7, 5), (-1, 5), self.board))
        
class TestKnight(unittest.TestCase):
    def setUp(self):
        self.board: List[List[Optional[Figure]]] = [[None for _ in range(8)] for _ in range(8)]
        self.white_knight = Knight("white", (0, 1))
        self.black_knight = Knight("black", (7, 1))

    def test_valid_knight_moves_should_return_true(self):
        self.assertTrue(self.white_knight.is_move_valid((0, 1), (2, 0), self.board))
        self.assertTrue(self.white_knight.is_move_valid((0, 1), (2, 2), self.board))
        self.assertTrue(self.white_knight.is_move_valid((0, 1), (1, 3), self.board))

    def test_invalid_knight_moves_should_return_false(self):
        self.assertFalse(self.white_knight.is_move_valid((0, 1), (0, 3), self.board))
        self.assertFalse(self.black_knight.is_move_valid((7, 1), (5, 3), self.board))

    def test_capture_opponent_should_return_true(self):
        self.board[2][0] = Knight("black", (2, 0))
        self.assertTrue(self.white_knight.is_move_valid((0, 1), (2, 0), self.board))

    def test_out_of_bounds_move_should_return_false(self):
        self.assertFalse(self.white_knight.is_move_valid((0, 1), (2, -1), self.board))


if __name__ == "__main__":
    unittest.main()
