import numpy as np
from distutils.log import error
from traitlets import Dict#maybe overkill

def bitboard(indices=[]):
    # defines basic bitboard of type int8/boolean
    # gibt bitboard mit 1en für jeden index in indices und ansonsten 0en aus
    bb = np.zeros((8,8), dtype=bool)
    bb.flat[indices] = True
    return bb


def give_bitboards():
    # creates bitboards as dictionary
    # ein gesamter Spielzustand als Spielbrett wird durch bb definiert
    bb = {
        # piece colors
        "W" : bitboard(),
        "B" : bitboard(),
        # pieces
        "k" : bitboard(),
        "q" : bitboard(),
        "n" : bitboard(),
        "r" : bitboard(),
        "b" : bitboard(),
        "p" : bitboard(),
    }
    return bb


def give_static_bitboards():
    # creates static bitboards
    # bitboards für Reihen von 1en für jeweilige Reihe/Spalte
    # Beispiel: bitboard mit 1 bei b3: b = sbb['lb'] & sbb['3']
    sbb = {
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
        "8" : bitboard(),
    }
    
    # lines
    sbb['la'][:,0] = True
    sbb['lb'][:,1] = True
    sbb['lc'][:,2] = True
    sbb['ld'][:,3] = True
    sbb['le'][:,4] = True
    sbb['lf'][:,5] = True
    sbb['lg'][:,6] = True
    sbb['lh'][:,7] = True
    
    # rows
    sbb['1'][0,:] = True
    sbb['2'][1,:] = True
    sbb['3'][2,:] = True
    sbb['4'][3,:] = True
    sbb['5'][4,:] = True
    sbb['6'][5,:] = True
    sbb['7'][6,:] = True
    sbb['8'][7,:] = True
    
    return sbb


sbb = give_static_bitboards()


def init_game(player):#kein b als input(wozu?)
    # initializes board with pieces
    # stellt Spielfiguren auf die jeweiligen Felder auf Spielfeld
    # -> könnte auch mit static bitboards initialisiert werden
    
    # weiß beginnt
    player = player.__set__('W')
    b = give_bitboards()
    
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


def print_board(b, flip=False):
    # pretty prints board
    # flip: white at bottom (typical orientation of board, but reverse order of array when printing (up <> down)
    
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

def print_board_list(b_list, flip=False):
    # prints a whole list of bitboard_dicts
    if len(b_list) > 0:
        for b in b_list:
            if len(b) > 0:
                #print('print:')
                print(print_board(b, flip))
            else:
                print('empty board')
    else:
        print('empty b_list')

def BittoFEN(b,player=False):#turns bitboard into FEN Strings
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
    if player==-1:
        player="W"
    elif player==1:
        player="B"
        FEN+=" "+str(player) 
    return FEN

def serialize_bb(bb):
    # gibt einzelne bitboards für jedes True an entsprechender Stelle zurück
    return [bitboard(index) for index in np.flatnonzero(bb)]

def flatten_list_of_list(list_of_list):
    # flacht list of list zu liste ab [[a,b],[c,d]] -> [a,b,c,d] (zb: zugehörigkeit für figuren geht flöten)
    #[item for sublist in t for item in sublist]
    return [item for sublist in list_of_list for item in sublist]
    


def FENtoBit(fen,player=False):
    if type(fen)!=str:
        error("FENtoBit only takes one argument of type str and not" +str(type(fen)))
    info = fen.split(" ")
    board = info[0].split("/")
    #print(board)
    b = give_bitboards()
    ver=0
    for y in range(8):  # a row
        #print(y)
        #y = 7-y
        #print(y)
        ver=0#versatz, falls int index verschiebt
        for x in range(8):  # a field in a row
            #"".lower()
            #print(board[y][x])
            if ver+x>=8:#zeile fertig
                     break
            try:#int ->skip
                z=int(board[y][x])
                # ver+=int(board[y][x])# field is a character
                if z>=0:
                    ver+=z-1
                
                
            except:#string
                if (board[y][x]).islower():
                    b["B"][7-y,x+ver] = True
                else:
                    b["W"][7-y,x+ver] = True
                b[board[y][x].lower()][7-y,x+ver] = True#adding specific character
            #print(x,y,": ",board[y][x])
            #print(ver)
    # TODO
    # using the other values in FEN string
    #bitboard: 
    #bit[0]== bottom left
    #bit[7] == bottom right
    #bit[63]== upper right
    #player=info[1]
    if player:
        if (info[1]=="W" or info[1]=="w"):
            player=1
        else:
            player=-1
        return [b,player]#gib player mit aus
    else:
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

 