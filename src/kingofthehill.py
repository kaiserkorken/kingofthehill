import numpy as np
# requires: pip install anytree
from anytree import Node, RenderTree

def bitboard():
    # defines basic bitboards of type boolean
    return np.zeros((8,8), dtype=bool)

def giveBitboards():
    # creates bitboards
    b = {
        
        # lines
        "la" : bitboard(),
        "lb" : bitboard(),
        "lc" : bitboard(),
        "ld" : bitboard(),
        "le" : bitboard(),
        "lf" : bitboard(),
        "lg" : bitboard(),
        "lh" : bitboard(),
        # rows
        "1" : bitboard(),
        "2" : bitboard(),
        "3" : bitboard(),
        "4" : bitboard(),
        "5" : bitboard(),
        "6" : bitboard(),
        "7" : bitboard(),
        "8" : bitboard(),#erst ab hier?
        # piece colors
        "W" : bitboard(),#reihen und spalten ergeben sich doch aus index?!
        "B" : bitboard(),
        # pieces
        "k" : bitboard(),
        "q" : bitboard(),
        "n" : bitboard(),
        "r" : bitboard(),
        "b" : bitboard(),
        "p" : bitboard(),
        
    }
    return b

def initGame(b):
    # initializes board with pieces
    
    # colored pieces for black/white player
    b['W'][0:2,:] = True
    b['B'][-2:,:] = True
    
    # adds kings('k'), queens, knights, rooks, bishops and pawns to the board on respecting fields
    b['k'][[0,-1],[4,4]] = True
    b['q'][[0,-1],[3,3]] = True
    b['n'][[0,0,-1,-1],[1,-2,1,-2]] = True
    b['r'][[0,0,-1,-1],[0,-1,0,-1]] = True
    b['b'][[0,0,-1,-1],[2,-3,2,-3]] = True
    b['p'][[1,-2],:] = True
    
    return b


def printBoard(b, flip=False):
    # pretty prints board
    # flip: white at bottom
    board = np.empty((8,8), dtype=str)
    board[:] = '_'
    
    # black player: lower case, white player: UPPER CASE
    board[b['B'] & b['k']] = 'k'
    board[b['B'] & b['q']] = 'q'
    board[b['B'] & b['n']] = 'n'
    board[b['B'] & b['r']] = 'r'
    board[b['B'] & b['b']] = 'b'
    board[b['B'] & b['p']] = 'p'
    
    board[b['W'] & b['k']] = 'K'
    board[b['W'] & b['q']] = 'Q'
    board[b['W'] & b['n']] = 'N'
    board[b['W'] & b['r']] = 'R'
    board[b['W'] & b['b']] = 'B'
    board[b['W'] & b['p']] = 'P'

    cols = np.reshape([['a','b','c','d','e','f','g','h'],['-','-','-','-','-','-','-','-']],(2,8))
    rows = np.reshape([['/','-','1','2','3','4','5','6','7','8'],['|','+','|','|','|','|','|','|','|','|']],(2,10))
    
    board = np.concatenate((cols, board), axis=0)
    board = np.concatenate((rows.T, board), axis=1)
    
    if flip == True:
        board = np.flip(board, axis=0)
    return board

def generateMoves(b, player):
    # generate a searchtree and search for possible pseudolegal moves
    moves = Node('root')
    # add possible striking moves
    
    # add plain movement moves
    
    return moves

def movesPawnsW(b):
    # shows possible normal moves of Black pawns
    return np.roll((b['W'] & b['p']), 8) & ~(b['W'] | b['B'])

def movesPawnsB(b):
    # shows possible normal moves of Black pawns
    
    #((B & SCH) >> 8) & ~(WEI | SCH)
    return np.roll((b['B'] & b['p']), -8) & ~(b['W'] | b['B'])

def movablePawnsW(b):
    # returns all White pawns that can move one ahead
    return (b['W'] & b['p']) & ~np.roll((b['W'] | b['B']),-8)

def movablePawnsB(b):
    # returns all Black pawns that can move one ahead
    
    #((B & SCH) >> 8) & ~(WEI | SCH)
    return (b['B'] & b['p']) & ~np.roll((b['W'] | b['B']),8)

# b = initGame(giveBitboards())
# print(printBoard(b))
# movablePawnsW(b)
# movablePawnsB(b)

# [['/' '|' 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h']
#  ['-' '+' '-' '-' '-' '-' '-' '-' '-' '-']
#  ['1' '|' 'R' 'N' 'B' 'Q' 'K' 'B' 'N' 'R']
#  ['2' '|' 'P' 'P' 'P' 'P' 'P' 'P' 'P' 'P']
#  ['3' '|' '_' '_' '_' '_' '_' '_' '_' '_']
#  ['4' '|' '_' '_' '_' '_' '_' '_' '_' '_']
#  ['5' '|' '_' '_' '_' '_' '_' '_' '_' '_']
#  ['6' '|' '_' '_' '_' '_' '_' '_' '_' '_']
#  ['7' '|' 'p' 'p' 'p' 'p' 'p' 'p' 'p' 'p']
#  ['8' '|' 'r' 'n' 'b' 'q' 'k' 'b' 'n' 'r']]
# array([[False, False, False, False, False, False, False, False],
#        [False, False, False, False, False, False, False, False],
#        [False, False, False, False, False, False, False, False],
#        [False, False, False, False, False, False, False, False],
#        [False, False, False, False, False, False, False, False],
#        [False, False, False, False, False, False, False, False],
#        [ True,  True,  True,  True,  True,  True,  True,  True],
#        [False, False, False, False, False, False, False, False]])
# Node('/root')
#player = 1
#generateMoves(b,player)