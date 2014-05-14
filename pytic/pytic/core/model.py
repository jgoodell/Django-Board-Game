from random import randint

class Move(object):
    '''Class representing a move on the tic tac toe board.
    '''

    def __init__(self,player,x,y):
        self.player = player
        self.x = x
        self.y = y
        self._move = [self.player,self.x,self.y]

    def __getitem__(self,index):
        return self._move[index]

    def __repr__(self):
        return "<Move(%s,%s,%s)>" % (self.player,self.x,self.y)

    def __eq__(self,other):
        try:
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        except AttributeError:
            # If you are comparing and the don't have the same attributes.
            return False

    def __ne__(self,other):
        try:
            if self.x != other.x or self.y != other.y:
                return True
            else:
                return False
        except AttributeError:
            # If you are comparing and the don't have the same attributes.
            return False


class Board(object):
    '''Class representing the board of the tic tac toe game. The cells
    of the board a laid out and indexed as pictured below.

     |
     |[(0,2),(1,2),(2,2)]
    Y|[(0,1),(1,1),(2,1)]
     |[(0,0),(1,0),(2,0)]
     +--------------------
               X
    '''

    _winning_vectors = [
        [Move(None,0,0),Move(None,1,0),Move(None,2,0)],
        [Move(None,0,1),Move(None,1,1),Move(None,2,1)],
        [Move(None,0,2),Move(None,1,2),Move(None,2,2)],
        [Move(None,0,0),Move(None,0,1),Move(None,0,2)],
        [Move(None,1,0),Move(None,1,1),Move(None,1,2)],
        [Move(None,2,0),Move(None,2,1),Move(None,2,2)],
        [Move(None,0,0),Move(None,1,1),Move(None,2,2)],
        [Move(None,0,2),Move(None,1,1),Move(None,2,0)]
        ]

    def _check_for_winner(self):
        '''Checks the board to see if there is a winner.
        '''
        for vector in self._winning_vectors:
            players = list()
            for move in vector:
                try: #If no move has been made the cell will be empty.
                    if hasattr(self._matrix[move[1]][move[2]][0],'name'):
                        players.append(self._matrix[move[1]][move[2]][0])
                except IndexError:
                    pass

            try:  #If the board cell is emplty and entry won't exist in players.
                if len(players) == 3 and players[0] == players[1] and players[0] == players[2]:
                    raise GameOver("Player %s is the winner!" % players[0])
                elif len(self._moves) == 9:
                    raise GameOver("C.A.T.")
            except IndexError:
                pass
    
    def next_move_analyzer(self,player):
        '''Given the analyzing player, provides the next move.
        '''
        total_open_moves = list()
        for vector in self._winning_vectors:
            opponent_moves = list()
            my_moves = list()
            open_moves = list()

            for move in vector:
                cell = self._matrix[move[1]][move[2]]
                if cell == (): # if an empty tuple then it is an open move
                    open_moves.append(move)
                elif cell.player != player: # if player that made move is not me
                    opponent_moves.append(move)
                else: # all other moves are me
                    my_moves.append(move)

            if len(opponent_moves) == 2 and len(my_moves) == 0: # if there is an open move take it
                move = open_moves[0]
                move.player = player
                return move
            else: # else add open moves to pool of potential moves
                for move in open_moves:
                    if not move in total_open_moves: # add move if it is not already there
                        total_open_moves.append(move)
        move = total_open_moves[randint(0,len(total_open_moves) - 1)]
        move.player = player
        return move

    def add_move(self,move):
        '''Add a move instance to the board.

        Arguments
        move,   A tic tac toe Move instance.
        '''
        self._moves.append(move)
        if not self._matrix[move[1]][move[2]]: #if there is no move there
            self._matrix[move[1]][move[2]] = move
        else: #otherwise a move has already been made there.
            raise GameException('This move has already beeen made.')
        self._check_for_winner()

    def __init__(self):
        self._moves = list()
        self._matrix = [
            [(),(),()],
            [(),(),()],
            [(),(),()]
            ]

    def __len__(self):
        return len(self._moves)

    def __getitem__(self,index):
        return self._moves[index]


class Game(object):
    '''Class representing the game of tic tic toe.
    '''
    _winning_vectors = [
        
        ]
    @staticmethod
    def player_x(name):
        '''Returns a Player instance for O.

        Arguments:
        name,  String with players name.
        '''
        return Player(name,is_x=True)

    @staticmethod
    def player_o(name):
        '''Returns a Player instance for X.

        Arguments:
        name,  String with players name.
        '''
        return Player(name,is_x=False)

    def make_move(self,player,x,y):
        '''Make a move in game play.
        '''
        try:
            self._board.add_move(Move(player,x,y))
        except GameException:
            raise

    def next_move_wizard(self, player):
        """Get the player's next move in response to the board..
        """
        return self._board.next_move_analyzer(player)

    def __init__(self):
        self._board = Board()

    def __len__(self):
        return len(self._board._moves)

    def __getitem__(self,index):
        return self._board[index]


class Player(object):
    '''Class representing a player of tic tac toe
    '''
    def __init__(self,name, is_x=True):
        self.name = name
        self.is_x = is_x
        self._moves = 0

    def __len__(self):
        return self._moves

    def __add__(self, other):
        self._moves += other
        return self

    def __eq__(self,other):
        try:
            if self.is_x == other.is_x:
                return True
            else:
                return False
        except AttributeError:
            #definitely not equal if they don't have
            #the same attributes
            return False

    def __ne__(self,other):
        try:
            if self.is_x != other.is_x:
                return True
            else:
                return False
        except AttributeError:
            #definitely not equal if they don't have
            #the same attributes
            return False

    def __repr__(self):
        return "<Player('%s')>" % self.name


class GameOver(Exception):
    pass

class GameException(Exception):
    pass
