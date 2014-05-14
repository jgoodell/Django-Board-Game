import unittest
from pprint import pprint

from pytic.core import Board, Move, Player, GameOver


class BoardTestCase(unittest.TestCase):
    '''Exercise the player.
    '''
    def setUp(self):
        self.board = Board()

    def tearDown(self):
        self.board = None

    def test_iter_vector01(self):
        '''Iterate over the first vector on the board.
        '''
        self.board.add_move(Move('',0,0))
        self.assertEqual(len(self.board),1)
        for move in self.board:
            self.assertEqual(type(move),Move)

    def test_ai_first(self):
        '''Test that AI will make the second move as expected.
        '''
        player_x  = Player('X')
        player_ai = Player("AI",is_x=False)
        self.board.add_move(Move(player_x,0,0))
        self.board.add_move(Move(player_ai,2,1))
        self.board.add_move(Move(player_x,0,2))
        move = self.board.next_move_analyzer(player_ai)
        self.assertEqual(move,Move('',0,1))

    def test_ai_second(self):
        '''Test that AI will make the correct move when there are more than one moves possible.
        '''
        player_x  = Player('X')
        player_ai = Player('AI',is_x=False)
        self.board.add_move(Move(player_x,0,0))
        self.board.add_move(Move(player_ai,2,2))
        self.board.add_move(Move(player_x,0,1))
        move = self.board.next_move_analyzer(player_ai)
        self.assertEqual(move,Move('',0,2))

    def test_ai_alt(self):
        '''Test that AI will make the correct move when there are more than one moves possible.
        '''
        player_x  = Player('X')
        player_ai = Player('AI',is_x=False)
        self.board.add_move(Move(player_x,0,0))
        self.board.add_move(Move(player_ai,2,1))
        self.board.add_move(Move(player_x,0,2))
        move = self.board.next_move_analyzer(player_ai)
        self.assertEqual(move,Move('',0,1))

    def test_ai_game(self):
        '''Test that an AI game will end in a tie.
        '''
        player_aix = Player('X', is_x=True)
        player_aio = Player('O', is_x=False)
        move = self.board.next_move_analyzer(player_aix)
        self.board.add_move(move)
        move = self.board.next_move_analyzer(player_aio)
        self.board.add_move(move)
        move = self.board.next_move_analyzer(player_aix)
        self.board.add_move(move)
        move = self.board.next_move_analyzer(player_aio)
        self.board.add_move(move)
        move = self.board.next_move_analyzer(player_aix)
        self.board.add_move(move)
        move = self.board.next_move_analyzer(player_aio)
        self.board.add_move(move)
        move = self.board.next_move_analyzer(player_aix)
        self.board.add_move(move)
        move = self.board.next_move_analyzer(player_aio)
        self.board.add_move(move)
        move = self.board.next_move_analyzer(player_aix)
        #self.board.add_move(move)
        self.assertRaises(GameOver,self.board.add_move,move)
