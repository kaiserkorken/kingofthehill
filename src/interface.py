from distutils.log import error
import string

from traitlets import Dict
from kingofthehill import *
"""
class game(object):
    def __init__(self,fen):§
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
def BittoFEN(b):#turns bitboard into FEN Strings
    if type(b)!=dict:
        error("BittoFEN only takes one argument of type dict and not" +str(type(b)))
    # FENboard=np.zeros((8,8))
    # check=["k","q","n","r","b","p"]
    # for z in check:
    #     for x in range(7):#maybe replace with b[z] and (b["W"] or b["B"])
    #         for y in range(7):
    #             if b[z][x,y]==1 and b["W"][x,y]==1:
    #                 FENboard[x+y]=z.upper()
    #             elif b[z][x,y] and b["B"][x,y]:
    #                 FENboard[x+y]=z
    #build string
    board = np.empty((8,8), dtype=str)
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
    #print(board)
    remember=0
    nothing=False
    FEN=""
    for x in range(8):
        nothing=False
        for y in range(8):
            t=board[x,y]
            if t!="":#Spielfigur auf dem Feld
                if nothing:#wenn vorheriges Feld frei war
                    FEN+=str(remember)
                    remember=0#reset nothing streak
                    nothing=False
                FEN+=str(t)
            else:#freies feld
                remember+=1#ein weiteres Feld isz frei
                nothing=True
            #add missing arguments to FEN
        if remember==8:#ganze reihe leer
            FEN+=str(8)
            remember=0
        if x!=7:
            FEN+="/"
    #print(FEN)
    return FEN


def FENtoBit(fen):
    if type(fen)!=str:
        error("FENtoBit only takes one argument of type str and not" +str(type(fen)))
    info = fen.split(" ")
    board = info[0].split("/")
    #print(board)
    b = giveBitboards()
    ver=0
    for y in range(8):  # a row
        ver=0#versatz, falls int index verschiebt
        for x in range(8):  # a field in a row
            #"".lower()
            #print(board[y][x])
            try:#int
                ver+=int(board[y][x])# field is a character
                if ver+x>=8:#zeike fertig
                    break
            except:#string
                if (board[y][x]).islower():
                    b["B"][y,x+ver] = True
                else:
                    b["W"][y,x+ver] = True
                b[board[y][x].lower()][y,x+ver] = True#adding specific character
                
    # TODO
    # using the other values in FEN string
    #bitboard: 
    #bit[0]== bottom left
    #bit[7] == bottom right
    #bit[63]== upper right
    #player=info[1]
    return b#,player
#test str:
#bench
# rnbq1bnr/pppQkpp1/3p3p/8/3p4/2P5/PP2PPPP/RNB1KBNR
# a/b search: r2qkb1r/ppp2pp1/2np1n1p/1N6/3p4/2P1B2b/PP2PPPP/R3KBNR
# zugg: 3q3r/1pp1kpb1/3p1n2/1B6/3P4/4PN1P/5K1P/7R #0schlagende#
# zugg: rnb1kbnr/p4ppp/1p1pp3/2p3q1/3P4/NQP1PNPB/PP3P1P/R1B1K2R #
#try
# print("FEN in Bitboard:\n")
# x=FENtoBit("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
# print(printBoard(x))
# y=BittoFEN(x)
# print("Bitboard in FEN\n"+y)
# #print(printBoard(FENtoBit(y)))