import shelve
import json

from django.http import HttpResponse
from django.shortcuts import render

from pytic import core

ERROR_400 = "400 Bad Request"
ERROR_404 = "404 Not Found"
ERROR_405 = "405 Method Not Allowed"
ERROR_500 = "500 Server Error"

# TODO: Make logic for explicit HTTP method use into a decorator to use on the
# view functions.

def home(request):
    '''Home for the the game app.
    '''
    if request.method == 'GET':
        game_db = shelve.open('game')
        try:
            game = game_db['game']
        except KeyError:
            game = core.Game()
            game_db['game'] = game
        moves = {
            '0_0':'',
            '1_0':'',
            '2_0':'',
            '0_1':'',
            '1_1':'',
            '2_1':'',
            '0_2':'',
            '1_2':'',
            '2_2':'',
            }

        for each in game:
            key = '%s_%s' % (each.x, each.y)
            moves[key] = each.player.name
        return render(request, 'game/board.html', {'board':moves})
    else:
        response = HttpResponse(ERROR_405)
        response.status_code = 405
        return response

def lure(request):
    '''Ajax view that loads the board in the favor of AI.
    '''
    if request.method == "POST" and request.is_ajax():  # Explicitly use HTTP methods.
        game_db = shelve.open('game')
        try: # Get an existing game or make a new one.
            game = game_db['game']
        except KeyError:
            game = core.Game()

        player_ai = game.player_x('X')
        game.make_move(player_ai, 1, 1)  # Load the board
        
        # Save the altered game back and close the DB
        game_db['game'] = game
        game_db.close()
        response = HttpResponse(json.dumps({"ai_move":"%s%s" % (1,1),
                                            "player_move":"",
                                            "status":"Your Move"}),
                                content_type='application/json')
        return response

def make_move(request):
    '''Accepts Ajax request for making a move on the game board.
    '''
    if request.method == "POST" and request.is_ajax():  # Explicitly use HTTP methods.
        game_db = shelve.open('game')
        try: # Get an existing game or make a new one.
            game = game_db['game']
        except KeyError:
            game = core.Game()

        player = game.player_o('O')
        x_ord, y_ord = request.POST['ordinal'].split(',')
        try:  # Be prepared to catch the GameOver exception.
            game.make_move(player, int(x_ord), int(y_ord))
        except core.GameOver, e:
            game_db.pop('game')
            response = HttpResponse(json.dumps({'ai_move':None,
                                                'player_move': "%s%s" % (x_ord,y_ord),
                                                'status':"Game Over"}),
                                    content_type='application/json')
            return response
        except core.GameException, e:
            response = HttpResponse(json.dumps({'ai_move':None,
                                                'player_move': "%s%s" % (x_ord,y_ord),
                                                'status':"Oops! That One is Already Taken."}),
                                    content_type='application/json')
            return response
        
        player_ai = game.player_x('X')
        move = game.next_move_wizard(player_ai)
        try: # Be prepared to catch the GameOver exception.
            game.make_move(player_ai, move.x, move.y)  # Wow, some poor encapsulation.
        except core.GameOver, e:
            game_db.pop('game')
            response = HttpResponse(json.dumps({'ai_move':"%s%s" % (move.x,move.y),
                                                'player_move': "%s%s" % (x_ord,y_ord),
                                                'status':"Game Over"}),
                                    content_type='application/json')
            return response
        except core.GameException, e:
            response = HttpResponse(json.dumps({'ai_move':"%s%s" % (move.x,move.y),
                                                'player_move': "%s%s" % (x_ord,y_ord),
                                                'status':"Oops! That One is Already Taken."}),
                                    content_type='application/json')
            return response

        # Save the altered game back and close the DB
        game_db['game'] = game
        game_db.close()
        response = HttpResponse(json.dumps({"ai_move":"%s%s" % (move.x,move.y),
                                            "player_move":"%s%s" % (x_ord,y_ord),
                                            "status":"Still Playing"}),
                                content_type='application/json')
        return response
    else:
        response = HttpResponse(ERROR_405)
        response.status_code = 405
        return response
