from kingofthehill import *
"""
class game(object):
    def __init__(self,fen):
        self.fen=fen
"""
    #FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    #1. rows 1-8
    #2. w/b
    #3. castling
    #4. en passent (position)
    #5. turns w/out capture/pawn advance
    #6. overall moves

    
    
    #FEN:
def BittoFEN(type, board):#turns bitboard into FEN Strings
    for x in board:
        if board[x]:
            self.FEN(type, x)
    return board

def FEN(x, y):
    #inserts value x at position y
    pass

def FENtoBit(fen):
    info = fen.split(" ")
    board = info[0].split("/")
    b = giveBitboards()
    for y in range(len(board)):  # a row
        for x in range(len(y)):  # a field in a row
            if not int(board[y][x]):  # field is a character
                if board[y][x].islower():
                    b["B"][x, y] = True
                else:
                    b["W"][x, y] = True
                b[board[y][x]][x, y] = True#adding specific character
    # TODO
    # using the other values in FEN string
    #bitboard: 
    #bit[0]== bottom left
    #bit[7] == bottom right
    #bit[63]== upper right
    return b

#try
x=FENtoBit("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#print(x)#bzw. printBitboard(x)