import unittest

from pytic.core import (Game,
                        GameOver,
                        )


class FullGameTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_game(self):
        game = Game()
        player_x = game.player_x('Bill')
        player_o = game.player_o('Mike')

        '''
        (0,2)|(1,2)|(2,2)
        -----------------
        (0,1)|(1,1)|(2,1)
        -----------------
        (0,0)|(1,0)|(2,0)'''

        self.assertEqual(len(game),0)
        game.make_move(player_x,1,1)
        self.assertEqual(len(game),1)
        game.make_move(player_o,0,0)
        self.assertEqual(len(game),2)
        game.make_move(player_x,0,1)
        self.assertEqual(len(game),3)
        game.make_move(player_o,0,2)
        self.assertEqual(len(game),4)
        self.assertRaises(GameOver,game.make_move,player_x,2,1)
