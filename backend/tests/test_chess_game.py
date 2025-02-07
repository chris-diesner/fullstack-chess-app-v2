import unittest
from chess_game import ChessGame
from typing import List, Optional
from figures.figure import Figure, Bishop, Rook, Queen, Pawn, King, Knight

class TestChessGame(unittest.TestCase):
    
    def setUp(self):
        self.game = ChessGame()
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        
    def test_white_opens_game_should_retrun_string_white(self):
        self.assertEqual(self.game.current_player, "white")
        
    def test_switch_player_should_return_string_switched_color(self):
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "black")
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "white")
    
    def test_convert_to_coordinates_should_return_string_coordinates(self):
        result = self.game.convert_to_coordinates((0, 0))
        self.assertEqual(result, "A8")
        result = self.game.convert_to_coordinates((7, 7))
        self.assertEqual(result, "H1")
        
    def test_is_king_in_check_when_king_is_in_check_should_return_true_and_list_of_attacker_and_its_position(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("black", (0, 0))
        self.game.board.squares[0][7] = Rook("white", (0, 7))
        result, attacking_figures = self.game.is_king_in_check("black")
        self.assertTrue(result)
        self.assertEqual(len(attacking_figures), 1)
        self.assertIsInstance(attacking_figures[0][0], Rook)
        self.assertEqual(attacking_figures[0][0].color, "white")
        self.assertEqual(attacking_figures[0][1], (0, 7))
        
    def test_is_king_in_check_when_king_is_in_check_should_return_true_and_list_of_attackers_and_its_positions(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("black", (0, 0))
        self.game.board.squares[0][7] = Rook("white", (0, 7))
        self.game.board.squares[7][7] = Queen("white", (7, 7))
        result, attacking_figures = self.game.is_king_in_check("black")
        self.assertTrue(result)
        self.assertEqual(len(attacking_figures), 2)
        self.assertIsInstance(attacking_figures[0][0], Rook)
        self.assertEqual(attacking_figures[0][0].color, "white")
        self.assertEqual(attacking_figures[0][1], (0, 7))
        self.assertIsInstance(attacking_figures[1][0], Queen)
        self.assertEqual(attacking_figures[1][0].color, "white")
        self.assertEqual(attacking_figures[1][1], (7, 7))
        
    def test_is_king_in_check_when_king_is_not_in_check_should_return_false_and_empty_list_of_attackers(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][3] = King("black", (0, 3))
        self.game.board.squares[1][5] = Rook("white", (1, 5))
        result, attacking_figures = self.game.is_king_in_check("black")
        self.assertFalse(result)
        self.assertEqual(len(attacking_figures), 0)
        
    def test_is_king_in_checkmate_should_return_true(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("black", (0, 0))
        self.game.board.squares[0][7] = Rook("white", (0, 7))
        self.game.board.squares[1][7] = Queen("white", (1, 7))
        print(self.game.board.get_board_state())
        result = self.game.is_king_in_checkmate("black")
        self.assertTrue(result)

    def test_is_king_in_checkmate_should_return_false_if_king_can_escape(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("black", (0, 0))
        self.game.board.squares[0][7] = Rook("white", (0, 7))
        self.game.board.squares[1][1] = Rook("black", (1, 1))
        result = self.game.is_king_in_checkmate("black")
        self.assertFalse(result)

    def test_is_king_in_checkmate_should_return_false_if_attacker_can_be_taken(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("black", (0, 0))
        self.game.board.squares[0][7] = Rook("white", (0, 7))
        self.game.board.squares[1][7] = Rook("black", (1, 7))
        result = self.game.is_king_in_checkmate("black")
        self.assertFalse(result)
    
    def test_is_king_in_checkmate_should_return_false_if_attacker_can_be_blocked(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("black", (0, 0))
        self.game.board.squares[0][7] = Rook("white", (0, 7))
        #eig. Koenig blockieren
        self.game.board.squares[1][0] = Pawn("black", (1, 0))
        self.game.board.squares[0][1] = Pawn("black", (0, 1))
        self.game.board.squares[1][6] = Rook("black", (1, 6))
        result = self.game.is_king_in_checkmate("black")
        self.assertFalse(result)
        
    def test_is_king_in_checkmate_should_return_false_if_knight_blocks_attacker_and_king_cannot_escape(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("black", (0, 0))
        self.game.board.squares[0][7] = Rook("white", (0, 7))
        #eig. Koenig blockieren
        self.game.board.squares[1][0] = Pawn("black", (1, 0))
        self.game.board.squares[0][1] = Pawn("black", (0, 1))
        self.game.board.squares[2][1] = Knight("black", (2, 1))
        result = self.game.is_king_in_checkmate("black")
        self.assertFalse(result)

    def test_move_no_figure_should_return_string_empty_field(self):
        result = self.game.move_figure((3, 3), (4, 4))
        self.assertEqual(result, "Du hast ein leeres Feld ausgewählt!")

    def test_move_wrong_player_should_return_string_invalid_figure(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[1][3] = King("black", (1, 3))
        result = self.game.move_figure((1, 3), (2, 3))
        self.assertEqual(result, "Es ist white's Zug!")

    def test_invalid_move_should_return_string_invalid_move(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[1][3] = Pawn("white", (1, 3))
        result = self.game.move_figure((1, 3), (5, 1))
        self.assertEqual(result, "Ungültiger Zug!")
        
    def test_valid_move_switches_player_shold_return_string_sitched_color_black(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[6][3] = Pawn("white", (6, 3))
        self.game.move_figure((6, 3), (5, 3)) 
        self.assertEqual(self.game.current_player, "black")

    def test_move_pawn_on_blocked_field_should_return_string_invalid_move(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[6][0] = Pawn("white", (6, 0))
        self.game.board.squares[5][0] = Pawn("white", (5, 0))
        result = self.game.move_figure((6, 0), (5, 0))
        self.assertEqual(result, "Ungültiger Zug!")

    def test_capture_empty_field_should_return_string_invalid_move(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[6][0] = Pawn("white", (6, 0))
        result = self.game.move_figure((6, 0), (5, 1)) 
        self.assertEqual(result, "Ungültiger Zug!")
        
    def test_move_while_in_check_should_return_string_invalid_move_king_check(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[1][0] = King("white", (1, 0))
        self.game.board.squares[0][7] = Rook("black", (0, 7))
        result = self.game.move_figure((1, 0), (0, 0))
        self.assertEqual(result, "ungültiger Zug! king im Schach!")
        
    def test_is_stalemate_should_return_true_if_no_legal_move_possible(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("white", (0, 0))
        self.game.board.squares[1][2] = King("black", (1, 2))
        self.game.board.squares[2][2] = Knight("black", (2, 2))
        self.game.current_player = "black"
        self.game.switch_player()
        self.assertTrue(self.game.check_stalemate())
        
    def test_is_stalemate_should_return_false_if_legal_moves_exist(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("white", (0, 0))
        self.game.board.squares[7][7] = King("black", (7, 7))
        self.game.board.squares[6][6] = Queen("white", (6, 6))
        self.game.board.squares[5][5] = Pawn("black", (5, 5))
        self.game.current_player = "white"
        self.game.switch_player()
        self.assertFalse(self.game.check_stalemate())
        
    def test_fools_mate_should_return_true_for_checkmate_after_four_moves(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.setup_board()
        print(self.game.board.get_board_state())
        
        #Zug 1: weiß f2 -> f3
        self.game.move_figure((6, 5), (5, 5))
        self.assertEqual(self.game.current_player, "black")
        self.assertIsNone(self.game.board.squares[6][5])
        self.assertIsInstance(self.game.board.squares[5][5], Pawn)

        #Zug 2: schwarz e7 -> e5
        self.game.move_figure((1, 4), (3, 4)) 
        self.assertEqual(self.game.current_player, "white")
        self.assertIsNone(self.game.board.squares[1][4])
        self.assertIsInstance(self.game.board.squares[3][4], Pawn)

        #Zug 3: weiß g2 -> g4
        self.game.move_figure((6, 6), (4, 6)) 
        self.assertEqual(self.game.current_player, "black")
        self.assertIsNone(self.game.board.squares[6][6])
        self.assertIsInstance(self.game.board.squares[4][6], Pawn)

        #Zug 4: schwarz d8 -> h4
        self.game.move_figure((0, 3), (4, 7))
        self.assertEqual(self.game.current_player, "white")
        self.assertIsNone(self.game.board.squares[0][3])
        self.assertIsInstance(self.game.board.squares[4][7], Queen)
        
        print(self.game.board.get_board_state())

        is_checkmate = self.game.is_king_in_checkmate("white")
        self.assertTrue(is_checkmate)

    def test_move_with_invalid_uuid_should_return_error_mismatched_figure_ids(self):
        invalid_uuid = "00000000-0000-0000-0000-000000000000"
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[6][0] = Pawn("white", (6, 0))
        result = self.game.move_figure((6, 0), (4, 0), invalid_uuid)
        self.assertEqual(result, "Fehler: Figuren-ID stimmt nicht überein!")

    def test_valid_move_should_return_string_movement_notation(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[6][0] = Pawn("white", (6, 0))
        result = self.game.move_figure((6, 0), (4, 0))
        self.assertTrue(result.startswith("pawn (white"))
        self.assertIn("von A2 auf A4", result)

    def test_valid_move_updates_board_should_return_string_updated_board(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[6][0] = Pawn("white", (6, 0))
        result = self.game.move_figure((6, 0), (4, 0))
        self.assertTrue(result.startswith("pawn (white"))
        self.assertIn("von A2 auf A4", result)
        self.assertIsNone(self.game.board.squares[6][0]) 
        self.assertIsInstance(self.game.board.squares[4][0], Pawn) 

    def test_capture_opponent_with_uuid_check_should_return_string_valid_move(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[2][2] = King("black", (2, 2))
        self.game.board.squares[5][5] = King("white", (5, 5))
        self.game.board.squares[7][7] = Rook("black", (7, 7))
        attacking_pawn = self.game.board.squares[7][0] = Rook("white", (7, 0))
        result = self.game.move_figure((7, 0), (7, 7), attacking_pawn.id)
        self.assertTrue(result.startswith("rook (white"))
        self.assertIn("schlägt rook (black", result)
        self.assertIsNone(self.game.board.squares[7][0]) 
        self.assertIsInstance(self.game.board.squares[7][7], Rook)
        self.assertEqual(self.game.board.squares[7][7].color, "white")
        white_moves = self.game.white_player.move_history
        self.assertEqual(len(white_moves), 1)
        self.assertIn("schlägt rook (black", white_moves[0])
        self.assertIn(attacking_pawn.id, white_moves[0])

    def test_move_with_correct_uuid_should_return_string_valid_move(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[6][0] = Pawn("white", (6, 0))
        valid_uuid = self.game.board.squares[6][0].id
        result = self.game.move_figure((6, 0), (4, 0), valid_uuid)
        self.assertTrue(result.startswith("pawn (white"))
        self.assertIn("von A2 auf A4", result)

    def test_move_history_should_return_list_move_history(self):
        self.game.board.setup_board()
        self.game.move_figure((6, 5), (5, 5))  
        white_moves = self.game.white_player.move_history
        self.assertEqual(len(white_moves), 1)
        self.assertIn("von F2 auf F3", white_moves[0])
        self.game.move_figure((1, 4), (3, 4))
        black_moves = self.game.black_player.move_history
        self.assertEqual(len(black_moves), 1)
        self.assertIn("von E7 auf E5", black_moves[0])
        self.game.move_figure((6, 6), (4, 6))
        white_moves = self.game.white_player.move_history
        self.assertEqual(len(white_moves), 2)
        self.assertIn("von G2 auf G4", white_moves[1])
        self.game.move_figure((1, 3), (3, 3))
        black_moves = self.game.black_player.move_history
        self.assertEqual(len(black_moves), 2)
        self.assertIn("von D7 auf D5", black_moves[1])
    
    def test_move_wrong_player_black_should_return_string_invalid_figure(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[6][0] = Pawn("white", (6, 0))
        self.game.current_player = "black"
        result = self.game.move_figure((6, 0), (4, 0))
        self.assertEqual(result, "Es ist black's Zug!")
        
    def test_target_uuid_mismatch_should_return_error_for_mismatched_ids_in_history(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[6][0] = Pawn("white", (6, 0))
        self.game.board.squares[1][4] = Pawn("black", (1, 4))
        self.game.move_figure((6, 0), (4, 0)) 
        self.game.move_figure((1, 4), (3, 4))
        self.game.board.squares[3][1] = Rook("black", (3, 1))
        self.game.board.squares[4][0] 
        result = self.game.move_figure((4, 0), (3, 1))
        self.assertEqual(result, "Fehler: UUID stimmen nicht überein!")
        
    def test_legal_en_passant_rule_white_should_return_valid_move_history(self):
        self.game.board.setup_board()
        #Zug 1: weiß e2 -> e4
        self.game.move_figure((6, 4), (4, 4)) 
        #Zug 2: schwarz b7 -> b6
        self.game.move_figure((1, 1), (2, 1))
        #Zug 3: weiß e4 -> e5
        self.game.move_figure((4, 4), (3, 4))
        #Zug 4: schwarz d7 -> d5
        self.game.move_figure((1, 3), (3, 3))
        result = self.game.move_figure((3, 4), (2, 3))
        self.assertTrue(result.startswith("pawn (white"))
        self.assertIn("von E5 auf D6", result)
        self.assertIsNone(self.game.board.squares[3][3])
        figure_to_check = self.game.board.squares[2][3]
        self.assertIsInstance(figure_to_check, Pawn)
        if figure_to_check:
            self.assertEqual(figure_to_check.color, "white")

    def test_legal_en_passant_rule_black_should_return_valid_move_history(self):
        self.game.board.setup_board()
        #Zug 1: weiß e2 -> e3
        self.game.move_figure((6, 4), (5, 4))
        #Zug 2: schwarz b7 -> b5
        self.game.move_figure((1, 1), (3, 1))
        #Zug 3: weiß h2 -> h4
        self.game.move_figure((6, 7), (4, 7))
        #Zug 4: schwarz b5 -> b4
        self.game.move_figure((3, 1), (4, 1))
        #Zug 5: weiß e2c2 -> c4
        self.game.move_figure((6, 2), (4, 2))
        result = self.game.move_figure((4, 1), (5, 2))
        self.assertTrue(result.startswith("pawn (black"))
        self.assertIn("von B4 auf C3", result)
        self.assertIsNone(self.game.board.squares[4][2])
        figure_to_check = self.game.board.squares[5][2]
        self.assertIsInstance(figure_to_check, Pawn)
        if figure_to_check:
            self.assertEqual(figure_to_check.color, "black")
        
    def test_white_pawn_promotion_should_return_true_for_converted_queen_with_its_movement_rules(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]

        self.game.board.squares[2][3] = Pawn("white", (2, 3))  #d6
        self.game.board.squares[5][6] = Queen("white", (5, 6)) #g3
        self.game.board.squares[6][5] = Pawn("white", (6, 5))  #f2
        self.game.board.squares[6][6] = Pawn("white", (6, 6))  #g2
        self.game.board.squares[6][7] = Pawn("white", (6, 7))  #h2
        self.game.board.squares[7][6] = King("white", (7, 6))  #g1

        self.game.board.squares[0][6] = King("black", (0, 6))  #g8
        self.game.board.squares[1][6] = Queen("black", (1, 6)) #g7
        self.game.board.squares[1][5] = Pawn("black", (1, 5))  #f7
        self.game.board.squares[1][7] = Pawn("black", (1, 7))  #h7
        self.game.board.squares[2][6] = Pawn("black", (2, 6))  #g6
        
        #d6 -> d7
        self.game.move_figure((2, 3), (1, 3))  
        #g6 -> g5
        self.game.move_figure((2, 6), (3, 6))  
        #d7 -> d8
        self.game.move_figure((1, 3), (0, 3))  
        
        self.assertIsInstance(self.game.board.squares[0][3], Queen)
        last_move = self.game.white_player.move_history[-1]
        self.assertIn("queen", last_move)
        
        result = self.game.is_king_in_check("black")
        
        self.assertTrue(result)
        
        result = self.game.move_figure((1, 6), (0, 5))
        if self.game.board.squares[0][3]:
            valid_uuid = self.game.board.squares[0][3].id
            
        result = self.game.move_figure((0, 3), (0, 5), valid_uuid)
        
    def test_short_rochade_should_return_string_for_valid_rochade(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[7][4] = King("white", (7, 4))  #e1
        self.game.board.squares[7][7] = Rook("white", (7, 7))  #h1
        #Rochade hurz
        result = self.game.move_figure((7, 4), (7, 6))  
        
        self.assertIn("Rochade erfolgreich", result)
        self.assertIsInstance(self.game.board.squares[7][6], King)
        self.assertIsInstance(self.game.board.squares[7][5], Rook)
        
    def test_long_rochade_should_return_string_for_valid_rochade(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[7][4] = King("white", (7, 4))  #e1
        self.game.board.squares[7][0] = Rook("white", (7, 0))  #a1
        #Rochade lang
        result = self.game.move_figure((7, 4), (7, 2))
        
        self.assertIn("Rochade erfolgreich", result)
        self.assertIsInstance(self.game.board.squares[7][2], King)
        self.assertIsInstance(self.game.board.squares[7][3], Rook)
        
    def test_short_rochade_should_return_string_for_invalid_rochade(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[7][4] = King("white", (7, 4))  #e1
        self.game.board.squares[7][0] = Rook("white", (7, 0))  #a1
        self.game.board.squares[2][2] = King("black", (2, 2))  #c6
        
        self.game.move_figure((7, 4), (7, 5))
        self.game.move_figure((2, 2), (2, 3))
        self.game.move_figure((7, 5), (7, 4))
        self.game.move_figure((2, 3), (2, 2))
        result = self.game.move_figure((7, 4), (7, 6)) 
        self.assertIn("Ungültiger Zug: Rochade nicht erlaubt", result)
        
    def test_simulate_move_and_check_king_remains_in_check(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("black", (0, 0))
        self.game.board.squares[0][7] = Rook("white", (0, 7))

        result = self.game.simulate_move_and_check("black", (0, 0), (0, 1))

        self.assertTrue(result, "Der König bleibt im Schach, sollte True zurückgeben.")

    def test_simulate_move_and_check_king_escape(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[0][0] = King("black", (0, 0))
        self.game.board.squares[0][7] = Rook("white", (0, 7))

        result = self.game.simulate_move_and_check("black", (0, 0), (1, 1))

        self.assertFalse(result, "Der König kann sich retten, sollte False zurückgeben.")

    def test_simulate_move_and_check_blocking_piece(self):
        self.game.board.squares = [[None for _ in range(8)] for _ in range(8)]
        self.game.board.squares[1][1] = King("black", (1, 1))
        self.game.board.squares[0][7] = Rook("white", (0, 7))
        self.game.board.squares[0][3] = Queen("black", (0, 3))
        
        result = self.game.simulate_move_and_check("black", (1, 1), (0, 0))

        self.assertFalse(result, "Eine blockierende Figur sollte das Schach aufheben.")
        
if __name__ == "__main__":
    unittest.main()
