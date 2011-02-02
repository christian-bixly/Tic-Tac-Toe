from django.test import TestCase
from django.core.urlresolvers import reverse
from views import x_char, o_char, char_move_order, board_winner, board_has_move
import json

class MoveOrderTest(TestCase):
    def test_x_first_move(self):
        """
        Tests that X moves first given a blank board
        """
        board = [[None, None, None],
                 [None, None, None],
                 [None, None, None]]
        
        self.assertEqual(char_move_order(board), (x_char, o_char))

    def test_o_second_move(self):
        """
        Tests that O moves next after X
        """
        board = [[None, None, None],
                 [None, None, None],
                 [None, x_char, None]]
        
        self.assertEqual(char_move_order(board), (o_char, x_char))

class WinnerTest(TestCase):
    def test_win_1(self):
        board = [[o_char, None, None],
                 [x_char, x_char, x_char],
                 [o_char, None, None]]
        
        self.assertEqual(board_winner(board), x_char)
    
    def test_win_2(self):
        board = [[o_char, x_char, x_char],
                 [o_char, x_char, o_char],
                 [None, x_char, None]]
        
        self.assertEqual(board_winner(board), x_char)
    
    def test_win_3(self):
        board = [[o_char, None, x_char],
                 [o_char, x_char, o_char],
                 [x_char, x_char, None]]
        
        self.assertEqual(board_winner(board), x_char)
    
    # The next three tests are same as the above three only with the pieces reversed
    def test_win_4(self):
        board = [[x_char, None, None],
                 [o_char, o_char, o_char],
                 [x_char, None, None]]
        
        self.assertEqual(board_winner(board), o_char)
    
    def test_win_5(self):
        board = [[x_char, o_char, o_char],
                 [x_char, o_char, x_char],
                 [None, o_char, None]]
        
        self.assertEqual(board_winner(board), o_char)
    
    def test_win_6(self):
        board = [[x_char, None, o_char],
                 [x_char, o_char, x_char],
                 [o_char, o_char, None]]
        
        self.assertEqual(board_winner(board), o_char)

class HasMoveTest(TestCase):
    def test_has_move(self):
        board = [[x_char, o_char, x_char],
                 [x_char, o_char, x_char],
                 [o_char, None, o_char]]
        
        self.assertTrue(board_has_move(board))
    
    def test_has_no_move(self):
        board = [[x_char, o_char, x_char],
                 [x_char, o_char, x_char],
                 [o_char, x_char, o_char]]
        
        self.assertFalse(board_has_move(board))

class UnbeatableTest(TestCase):
    def test_unbeatability(self):
        def make_move(board, move, ch):
            """
            Puts ch on board as dictated by move.
            Returns (game_decided, winner)
            """
            board[move['row']][move['col']] = ch
            
            winner = board_winner(board)
            
            if winner is not None:
                return True, winner
            
            if not board_has_move(board):
                return True, None
            
            return False, None
        
        def make_ai_move(session, board, ch):
            response = self.client.post(reverse('ai_move'), {'session': session, 'board': json.dumps(board)})
            self.assertEqual(response.status_code, 200)
    
            ai_move = json.loads(response.content)['move']
            
            return make_move(board, ai_move, ch)
        
        def start_game():
            response = self.client.get(reverse('start_game'))
            self.assertEqual(response.status_code, 200)
            
            return json.loads(response.content)['session']
        
        def end_game(session):
            response = self.client.post(reverse('end_game'), {'session': session})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content), 'ok')
        
        def next_move(moves):
            session = start_game()

            board = [[None, None, None],
                     [None, None, None],
                     [None, None, None]]
            
            if ai_char == x_char:
                decided, winner = make_ai_move(session, board, ai_char)
                
                #It's the first move, it should be impossible for the game to end at this point
                self.assertEqual((decided, winner), (False, None))
            
            # Simulate all moves to get current board state
            for move in moves:
                decided, winner = make_move(board, move, player_char)
                if decided:
                    end_game(session)
                    self.assertNotEqual(winner, player_char)
                    return
                             
                decided, winner = make_ai_move(session, board, ai_char)
                if decided:
                    end_game(session)
                    self.assertNotEqual(winner, player_char)
                    return
            
            end_game(session)
            
            for i, row in enumerate(board):
                for j, cell in enumerate(row):
                    if cell is None:
                        move_n = moves[0:len(moves)]
                        move_n.append({'row': i, 'col': j})
                        next_move(move_n)
        
        player_char = x_char
        ai_char = o_char
        next_move([])
        
        player_char = o_char
        ai_char = x_char
        next_move([])
