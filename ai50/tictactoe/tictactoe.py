"""
Tic Tac Toe Player
"""

from copy import deepcopy
import random

# See https://docs.python.org/3/tutorial/errors.html#raising-exceptions
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidActionError(Error):
    """Exception raised for errors in the input.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, action, board, message):
        print('InvalidActionError: ', message, 'Action: ', action, 'on board: ', board)

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    EMPTY_count = 0

    for row in board:
      x_count += row.count(X)
      o_count += row.count(O)
      EMPTY_count += row.count(EMPTY)

    # If X has more squares than O, its O's turn:
    if x_count > o_count:
      return O

    # Otherwise it is X's turn:
    else:
      return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """ 
    moves = set()

    for i in range(3):
      for j in range(3):
        if board[i][j] == EMPTY:
          moves.add((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    # Check move is valid:
    if i not in [0, 1, 2] or j not in [0, 1, 2]:
      raise InvalidActionError(action, board, 'Result function given an invalid board position for action: ')
    elif board[i][j] != EMPTY:
      raise InvalidActionError(action, board, 'Result function tried to perform invalid action on occupaied tile: ')

    # Make a deep copy of the board and update with the current player's move:
    board_copy = deepcopy(board)
    board_copy[i][j] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
        # Check rows:
    for row in board:
      if row.count(X) == 3:
        return X
      if row.count(O) == 3:
        return O

    # Check columns:
    for j in range(3):
      column = ''
      for i in range(3):
        column += str(board[i][j])

      if column == 'XXX':
        return X
      if column == 'OOO':
        return O

    # Check Diagonals:
    diag1 = ''
    diag2 = ''
    j = 2

    for i in range(3):
      diag1 += str(board[i][i])
      diag2 += str(board[i][j])
      j -= 1

    if diag1 == 'XXX' or diag2 == 'XXX':
      return X
    elif diag1 == 'OOO' or diag2 == 'OOO':
      return O

    # No current winner, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or not actions(board):
      return True
    else:
      return False
        

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0

def minimax(board):
    """
    Returns optimal action for the current player on the board.
    """
    global actions_explored
    actions_explored = 0

    def max_player(board, ideal_min = 10):
        """ 
        determine maximum score for 'X' player.
        ideal_min is the ideal result
        """

        global actions_explored

        # If the game is over, return board value
        if terminal(board):
            return (utility(board), None)

        # max value when min_player plays optimally
        value = -10
        ideal_action = None

        # Get set of actions and then select a random one until list is empty:
        action_set = actions(board)

        while len(action_set) > 0:
            action = random.choice(tuple(action_set))
            action_set.remove(action)

            # breaks calls to min_player if lowest result identified
            if ideal_min <= value:
                break

        actions_explored += 1
        min_player_result = min_player(result(board, action), value)
        if min_player_result[0] > value:
            ideal_action = action
            value = min_player_result[0]

        return (value, ideal_action)


    def min_player(board, ideal_max = -10):
      """ 
      determine minimal score for 'O' player 
      """

      global actions_explored

      # If the game is over, return board value
      if terminal(board):
        return (utility(board), None)

      # Else pick the action giving the min value when max_player plays optimally
      value = 10
      ideal_action = None

      # Get set of actions and then select a random one until list is empty:
      action_set = actions(board)

      while len(action_set) > 0:
        action = random.choice(tuple(action_set))
        action_set.remove(action)

        # A-B Pruning skips calls to max_player if higher result already found:
        if ideal_max >= value:
          break

        actions_explored += 1
        max_result = max_player(result(board, action), value)
        if max_result[0] < value:
          ideal_action = action
          value = max_result[0]

      return (value, ideal_action)


    # If the board is terminal, return None:
    if terminal(board):
      return None

    if player(board) == 'X':
      print('Exploring optimal action...')
      ideal_move = max_player(board)[1]
      print('Actions explored by AI: ', actions_explored)
      return ideal_move
    else:
      print('Exploring optimal action...')
      ideal_move = min_player(board)[1]
      print('Total actions explored: ', actions_explored)
      return ideal_move
