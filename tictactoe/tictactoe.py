"""
Tic Tac Toe Player
"""
import random
import math


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

    for row in board:
        for item in row:
            if item is X:
                x_count += 1
            elif item is O:
                o_count += 1
    if o_count < x_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    states = set()
    if terminal(board):
        return states
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                states.add((i, j))
    return states


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    turn = player(board)
   # temp = copy.deepcopy(board)
    board[action[0]][action[1]] = turn
    return board


#    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if win_check(board,X):
        return X
    elif win_check(board,O):
        return O
    else: return None


def win_check(arr, char):
    # Check all possible winning combinations
    matches = [[0, 1, 2], [3, 4, 5],
               [6, 7, 8], [0, 3, 6],
               [1, 4, 7], [2, 5, 8],
               [0, 4, 8], [2, 4, 6]]

    for i in range(8):
        first = matches[i][0]
        second = matches[i][1]
        third = matches[i][2]

        if (arr[first//3][first%3] == char and
                arr[second//3][second%3] == char and
                arr[third//3][third%3] == char):
            return True
    return False

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for rows in board:
        for item in rows:
            if item is EMPTY:
                return False

    return True

   # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is X:
        return 1
    elif winner(board) is O:
        return -1
    else:return 0
#
# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     if terminal(board):
#         return None
#
#     current_player = player(board)
#
#     opt_action = help(board, current_player)
#
#     return opt_action[1]
#
#
# def help(board, current_player):
#
#     if terminal(board):
#         return utility(board), None
#
#     else:
#
#         all_actions = actions(board)
#         val = 1.0
#         action = []
#
#         if current_player == X:
#             val = -1.0
#
#             for i in all_actions:
#                 temp = result(board, i)
#                 ans = help(temp, O)
#                 temp_val = val
#                 val = max(val, ans[0]/2)
#                 if val > temp_val:
#                     action = i
#                 board[i[0]][i[1]] = EMPTY
#                 if val == 1:
#                     break
#
#         else:
#
#             for i in all_actions:
#                 temp = result(board, i)
#                 ans = help(temp, X)
#                 temp_val = val
#                 val = min(val, ans[0]/2)
#                 if val < temp_val:
#                     action = i
#                 board[i[0]][i[1]] = EMPTY
#                 if val == -1:
#                     break
#
#         return val, action

def minimax(board):
    if terminal(board):
        return None

    possible_actions = actions(board)
    if len(possible_actions) == 9:
        return random.choice(tuple(possible_actions))
    current_player = player(board)
    if current_player is X:
        optimal = max_score(board)
        return optimal[1]
    optimal = min_score(board)
    return optimal[1]

def max_score(board):
    if terminal(board):
        return utility(board),None
    a = actions(board)
    move = []
    v = -math.inf
    for action in a:
        temp = result(board,action)
        rv = min_score(temp)
        if rv[0] > v:
            v = rv[0]
            move = action
        board[action[0]][action[1]] = EMPTY
        if v == 1:
            break
    return v,move

def min_score(board):
    if terminal(board):
        return utility(board),None
    a = actions(board)
    move = []
    v = math.inf
    for action in a:
        temp = result(board,action)
        rv = max_score(temp)
        if rv[0] < v:
            v = rv[0]
            move = action
        board[action[0]][action[1]] = EMPTY
        if v == -1:
            break
    return v,move