import unittest

from pytic.core import Move


class MockPlayer(object):
    pass


class MoveTestCase(unittest.TestCase):
    '''Exercise the player.
    '''
    def setUp(self):
        self.player = MockPlayer()

    def tearDown(self):
        pass

    def test_make_move(self):
        '''Test making a move.
        '''
        move = Move(self.player,0,2)
        self.assertEqual(move.player,self.player)
        self.assertEqual(move[1],0)
        self.assertEqual(move[2],2)

    def test_move_equality(self):
        move1 = Move(self.player,0,2)
        move2 = Move(self.player,0,2)
        move3 = Move(self.player,1,2)
        self.assertEqual(move1,move2)
        self.assertNotEqual(move1,move3)
        
