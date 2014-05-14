import unittest

from pytic import core
from pytic.core import Game
from pytic.core import GameOver


class MockPlayer(object):

    def __init__(self,is_x=True):
        self.name = "Mock Player"
        self.is_x = is_x


class GameTestCase(unittest.TestCase):
    '''Exercise the Game class.
    '''
    def setUp(self):
        self.player_x = MockPlayer(is_x=True)
        self.player_o = MockPlayer(is_x=False)
        self.game = Game()

    def tearDown(self):
        pass

    def test_make_move(self):
        '''A player makes a move.
        '''
        self.game.make_move(self.player_x,1,1)

    def test_make_bad_move(self):
        '''A player makes a bad move.
        '''
        self.game.make_move(self.player_o,2,1)
        self.assertRaises(core.GameException,self.game.make_move,self.player_x,2,1)

    def test_win_game(self):
        '''Player wins game.
        '''
        self.game.make_move(self.player_o,0,0)
        self.game.make_move(self.player_o,0,1)
        self.assertRaises(GameOver,self.game.make_move,
                          self.player_o,0,2)

    def test_iter_game(self):
        '''Test that you can iterage over the
        moves in the game.
        '''
        self.game.make_move(self.player_o,0,0)
        self.game.make_move(self.player_x,1,0)
        self.game.make_move(self.player_o,0,1)
        self.game.make_move(self.player_x,1,1)
        try:
            self.game.make_move(self.player_o,0,2)
            self.assertFalse(True)
        except GameOver:
            self.assertEqual(len(self.game),5)
            for move in self.game:
                pass
        else:
            raise AssertionError('Game should be over.')

        
