"""
Tic Tac Toe Player
"""

import math
import copy

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
    c=0
    for i in board:
        for j in i:
            if j!=EMPTY:
                c=c+1
    if (c%2)==0:
        return X;
    else:
        return O;

 #   raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    d=set()

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                d.add((i,j))
    return d

   # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
        """
    if terminal(board) or board[action[0]][action[1]]!= EMPTY:
        return board

    bboard=copy.deepcopy(board)
    p = player(bboard)
    if p==O:
        bboard[action[0]][action[1]]=O
    else:
        bboard[action[0]][action[1]]=X

    return bboard

  #  raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(0 ,3):
        if board[i][0]==O and board[i][1]==O and board[i][2]==O:
            return O;

    for j in range(0 ,3):
        if board[0][j]==O and board[1][j]==O and board[2][j]==O:
            return O;

    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O;

    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O;


    for i in range(0, 3):
        if board[i][0] == X and board[i][1] == X and board[i][2] == X:
            return X;

    for j in range(0, 3):
        if board[0][j] == X and board[1][j] == X and board[2][j] == X:
            return X;

    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X;

    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X;


    return None

   # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner==X or winner ==O:
        return True

    x=False
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j]==EMPTY:
                x=True
    if x is True:
        return False
    else:
        return True

    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) ==X:
        return 1
    elif winner(board)==O:
        return -1
    else:
        return 0
    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board)==X:
        return optx(board)
    else:
        return opto(board)

   # raise NotImplementedError


def optx(board):
    if terminal(board):
        return None

    s=actions(board)
    d=[]
    for i in s:
        newboard=result(board,i)
        if utility(newboard)==1:
            return i
        else:
            d.append((utility(result(newboard,minimax(newboard))),i))

    d.sort()
    d.reverse()
    return d[0][1]

def opto(board):
    if terminal(board):
        return None

    s = actions(board)
    d = []
    for i in s:
        newboard = result(board, i)
        if utility(newboard) == -1:
            return i
        else:
            d.append((utility(result(newboard, minimax(newboard))), i))

    d.sort()
    return d[0][1]