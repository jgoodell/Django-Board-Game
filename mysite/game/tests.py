import json

from django.test import TestCase

from game import views


class MockRequest(object):
    def __init__(self, method="POST", data='', is_ajax=True):
        self.method = method
        self.data = data
        self._is_ajax = is_ajax
        self.POST = {'ordinal':data}

    def is_ajax(self):
        return self._is_ajax

def decide_on_move():
    '''Automates the trial and error method of picking a next move returning
    an HttpResponse object when a legitimate move is made.

    Arguments:
    None
    '''
    response = None
    for x_ord in range(3):
        for y_ord in range(3):
            response = views.make_move(MockRequest(data='%s,%s' % (x_ord,y_ord)))
        json_data = json.loads(response.content)
        if json_data['status'] != 'Oops! That One is Already Taken.':
            break
    return response

class CompleteGameTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        import os
        os.remove('game.db')

    def test_complete_game(self):
        '''Test of a complete game.
        '''
        response = views.make_move(MockRequest(data="0,0"))
        # Move 2
        response = decide_on_move()
        # Move 3
        response = decide_on_move()
        # Move 4
        response = decide_on_move()
        # Move 5
        response = decide_on_move()
        # Move 6
        response = decide_on_move()
        # Move 7
        response = decide_on_move()
        # Move 8
        response = decide_on_move()
        json_data = json.loads(response.content)
        self.assertTrue(json_data.has_key('status'))
        

class LureTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        import os
        os.remove('game.db')
        
    def test_lure(self):
        '''Test that a move can be made on an open game board
        '''
        response = views.lure(MockRequest(data=""))
        self.assertEqual(response.status_code, 200)
        try:
            json.loads(response.content)
        except:
            self.assertFalse(True)
        json_data = json.loads(response.content)
        self.assertTrue(json_data.has_key('ai_move'))
        self.assertEqual(json_data['ai_move'],"11")
        self.assertTrue(json_data.has_key('player_move'))
        self.assertEqual(json_data['player_move'],"")
        self.assertTrue(json_data.has_key('status'))


class MakeMoveTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        import os
        os.remove('game.db')

    def test_legitimate_move(self):
        '''Test that a move can be made on an open game board
        '''
        response = views.make_move(MockRequest(data="1,1"))
        self.assertEqual(response.status_code, 200)
        try:
            json.loads(response.content)
        except:
            self.assertFalse(True)
        json_data = json.loads(response.content)
        self.assertTrue(json_data.has_key('ai_move'))
        self.assertTrue(json_data.has_key('player_move'))
        self.assertTrue(json_data.has_key('status'))

    def test_illegitimate_move(self):
        '''Test that an error is returned if a move has already been made.

        I might enforce this on the client side, but I am still going to
        implement it server side.
        '''
        response = views.make_move(MockRequest(data='0,0'))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertTrue(json_data.has_key('ai_move'))
        self.assertTrue(json_data.has_key('player_move'))
        self.assertTrue(json_data.has_key('status'))

        response = views.make_move(MockRequest(data='0,0'))
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertTrue(json_data.has_key('ai_move'))
        self.assertEqual(json_data['ai_move'],None)
        self.assertTrue(json_data.has_key('player_move'))
        self.assertTrue(json_data.has_key('status'))
        self.assertEqual(json_data['status'],'Oops! That One is Already Taken.')
