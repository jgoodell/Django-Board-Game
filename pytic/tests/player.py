import unittest

from pytic.core import Player


class PlayerTestCase(unittest.TestCase):
    '''Exercise the player.
    '''
    def setUp(self):
        self.player = Player("Name",is_x=True)

    def tearDown(self):
        pass

    def test_player_symbol(self):
        '''Test that you can tell what symbol
        a player is using
        '''
        self.assertTrue(self.player.is_x)

    def test_player_no_moves(self):
        '''Test that you can tell if a player
        has made no moves.
        '''
        self.assertEqual(len(self.player),0)

    def test_player_moves(self):
        '''Test that you can tell how many moves
        a player has made.
        '''
        self.player += 1
        self.assertEqual(len(self.player),1)
        self.player += 1
        self.assertEqual(len(self.player),2)
        self.player += 1
        self.assertEqual(len(self.player),3)
        self.player += 1
        self.assertEqual(len(self.player),4)
        self.player += 1
        self.assertEqual(len(self.player),5)

