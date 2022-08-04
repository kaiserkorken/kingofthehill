from bitboard import *
from tt import ttable
import time


def utility(b,player,h,simple=False):
    util=0
    if player.tt!= None:
        hash = player.tt.hash_value(b,player.current)
        util = player.tt.in_table(hash, h)
        if len(util) != 2:
            # print(hash)
            if simple:
                util=simple_utility(b,player.current)
            else:
                util= spielBewertung(b,player.current)
            player.tt.to_table(hash, util, h)
        else:
            util=util[0]
    else:
        if simple:
                util=simple_utility(b,player.current)
        else:
                util= spielBewertung(b,player.current)         
    
    
    return util, hash
        
           


def simple_utility(b,player_code):
    piece_values = {'k':100, 'q':9, 'r':5, 'b':3, 'n':3, 'p':1}

       
    values_W = np.sum([np.sum(b[key] & b['W'])*piece_values[key] for key in piece_values])
    values_B = np.sum([np.sum(b[key] & b['B'])*piece_values[key] for key in piece_values])
    return player_code*(values_W - values_B)
gamma=0.2    
pawn_table = [[0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
     [5,  5, 10, 25, 25, 10,  5,  5],
     [0,  0,  0, 20, 20,  0,  0,  0],
     [5, -5,-10,  0,  0,-10, -5,  5],
     [5, 10, 10,-20,-20, 10, 10,  5],
     [0,  0,  0,  0,  0,  0,  0,  0]]
knight_table = [[-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-90,-30,-30,-30,-30,-90,-50]]
bishop_table = [[-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-90,-10,-10,-90,-10,-20]]
rook_table = [[0,  0,  0,  0,  0,  0,  0,  0],
      [5, 10, 10, 10, 10, 10, 10,  5],
     [-5,  0,  0,  0,  0,  0,  0, -5],
     [-5,  0,  0,  0,  0,  0,  0, -5],
     [-5,  0,  0,  0,  0,  0,  0, -5],
     [-5,  0,  0,  0,  0,  0,  0, -5],
     [-5,  0,  0,  0,  0,  0,  0, -5],
     [0,  0,  0,  5,  5,  0,  0,  0]]
queen_table = [[-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
     [-5,  0,  5,  5,  5,  5,  0, -5],
      [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, 70, -5,-10,-10,-20]]
queen_table_reverse = [[-20, -10, -10, 70, -5, -10, -10, -20],
                       [-10, 0, 5, 0, 0, 0, 0, -10],
                       [-10, 5, 5, 5, 5, 5, 0, -10],
                       [0, 0, 5, 5, 5, 5, 0, -5],
                       [-5, 0, 5, 5, 5, 5, 0, -5],
                       [-10, 0, 5, 5, 5, 5, 0, -10],
                       [-10, 0, 0, 0, 0, 0, 0, -10],
                       [-20, -10, -10, -5, -5, -10, -10, -20]]

king_table = [[-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,60,60,-30,-30,-20],
    [-10,-20,-20,80,80,-20,-20,-10],
     [-50,-30,-10,20,20,10,-30, 50],
     [20, 30, 10, 0, 0, 10, 30, 20]]

def chessPositionValue(x,y,piece,color):


    if color =="b" and piece!="Queen":
        x = 7-x
        y = 7-y


    if piece == "Rook":
        return rook_table[x][y]
    elif piece == "Pawn":
        return pawn_table[x][y]
    elif piece == "Knight":
        return knight_table[x][y]
    elif piece == "Bishop":
        return bishop_table[x][y]
    elif piece == "Queen":
        if color == "w":
            return queen_table[x][y]
        else:
            return queen_table_reverse[x][y]
    elif piece == "King":
        return king_table[x][y]
    
    
    
# erstellt ein array mit String values der position der Weißen oder Schwarzen Figuren

#neue Bewertungsfunktion
def doubledPawns(board, color):
    color = color[0]
    # Get indices of pawns:
    listofpawns = lookfor(board, color + 'p')
    # Count the number of doubled pawns by counting occurences of
    # repeats in their x-coordinates:
    repeats = 0
    temp = []
    for pawnpos in listofpawns:
        if pawnpos[0] in temp:
            repeats = repeats + 1
        else:
            temp.append(pawnpos[0])
    return repeats


def lookfor(board, piece):
    listofLocations = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == piece:
                x = col
                y = row
                listofLocations.append((x, y))
    return listofLocations

def blockedPawns(board, color):
    color = color[0]
    listofpawns = lookfor(board, color + 'p')
    blocked = 0
    # Self explanatory:
    for pawnpos in listofpawns:
        if ((color == 'w' and isOccupiedby(board, pawnpos[0], pawnpos[1] - 1,
                                           'black'))
                or (color == 'b' and isOccupiedby(board, pawnpos[0], pawnpos[1] + 1,
                                                  'white'))):
            blocked = blocked + 1
    return blocked


def isOccupiedby(board, x, y, color):
    if board[int(y)][int(x)] == '--':
        # the square has nothing on it.
        return False
    if board[int(y)][int(x)][0] == color[0]:
        # The square has a piece of the color inputted.
        return True
    # The square has a piece of the opposite color.
    return False


# print(blockedPawns(testBoardB,'b'))

def isolatedPawns(board, color):
    color = color[0]
    listofpawns = lookfor(board, color + 'p')
    # Get x coordinates of all the pawns:
    xlist = [x for (x, y) in listofpawns]
    isolated = 0
    for x in xlist:
        if x != 0 and x != 7:
            # For non-edge cases:
            if x - 1 not in xlist and x + 1 not in xlist:
                isolated += 1
        elif x == 0 and 1 not in xlist:
            # Left edge:
            isolated += 1
        elif x == 7 and 6 not in xlist:
            # Right edge:
            isolated += 1
    return isolated

def pawnP(board, player):
    if player == -1:
        return (doubledPawns(board, 'w') + blockedPawns(board, 'w') + isolatedPawns(board, 'w')) - \
               (doubledPawns(board, 'b') + blockedPawns(board, 'b') + isolatedPawns(board, 'b'))

    elif player == 1:
        return (doubledPawns(board, 'b') + blockedPawns(board, 'b') + isolatedPawns(board, 'b')) - \
               (doubledPawns(board, 'w') + blockedPawns(board, 'w') + isolatedPawns(board, 'w'))

def seitenWert(board,player):
    summe = 0
    color =""
    if player == 1:
        color = "w"
    elif player ==-1:
        color = "b"

    for x in board:
        for y in x:
                if y == color+'R':
                    summe+=5
                elif y ==color+'N':
                    summe+=3
                elif y ==color+'B':
                    summe+=3
                elif y ==color+'Q':
                    summe+=9
                elif y ==color+'K':
                    summe+=100
                elif y ==color+'p':
                    summe+=1

    if board[3][3]==color+'K' or board[3][4]==color+'K' or board[4][3]==color+'K' or board[4][4]==color+'K':
        return 1000

    else:
        return summe
    
def seitenWert2(board,player):
    summe = 0
    color =""
    if player == 1:
        color = "w"
    elif player ==-1:
        color = "b"


    for x, value in enumerate(board):
        for y, info in enumerate(value):
                if info == color+'R':
                    zwisch = chessPositionValue(x,y,"Rook",color)
                  #  print("Player:"+color+" Rook Value Position: x:"+str(x)+" y:"+str(y)+" Value:"+str(zwisch))
                    summe+=50+zwisch*gamma
                    zwisch = 0
                elif info ==color+'N':
                    zwisch = chessPositionValue(x, y, "Knight", color)
                  #  print("Player:" + color + " Knight Value Position: x:" + str(x) + " y:" + str(y) + " Value:" + str(
                   #     zwisch))
                    summe+=30+zwisch*gamma
                    zwisch = 0
                elif info ==color+'B':
                    zwisch = chessPositionValue(x, y, "Bishop", color)
                  #  print("Player:" + color + " Bishop Value Position: x:" + str(x) + " y:" + str(y) + " Value:" + str(
                  #      zwisch))
                    summe+=30+zwisch*gamma
                    zwisch = 0
                elif info ==color+'Q':
                    zwisch = chessPositionValue(x, y, "Queen", color)
                  #  print("Player:" + color + " Queen Value Position: x:" + str(x) + " y:" + str(y) + " Value:" + str(
                  #      zwisch))
                    summe+=90+zwisch*gamma
                    zwisch = 0
                elif info ==color+'K':
                    zwisch = chessPositionValue(x, y, "King", color)
                 #   print("Player:" + color + " King Value Position: x:" + str(x) + " y:" + str(y) + " Value:" + str(
                  #      zwisch))
                    #values_W = np.sum([np.sum(b[key] & b['W'])*piece_values[key] for key in piece_values])
                    summe+=1000+zwisch
                    zwisch = 0
                elif info ==color+'p':
                    zwisch = chessPositionValue(x, y, "Pawn", color)
                 #   print("Player:" + color + " Pawn Value Position: x:" + str(x) + " y:" + str(y) + " Value:" + str(
                  #      zwisch))
                    summe+=10+zwisch
                    zwisch = 0

    if board[3][3]==color+'K' or board[3][4]==color+'K' or board[4][3]==color+'K' or board[4][4]==color+'K':
        summe+=1000

    
    return summe

def spielBewertung(BitBoard,Player):
    nesBoard = FENtoBoard(BittoFEN(BitBoard))
    valuesW = seitenWert2(nesBoard,1)
    valuesB = seitenWert2(nesBoard,-1)
    valuesP = pawnP(nesBoard,Player)

    if Player ==1:
        return valuesW-valuesB+valuesP
    elif Player ==-1:
        return valuesB-valuesW+valuesP
    
#print(spielBewertung(FENtoBit("rnbqkbnr/ppp1pppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),1))
if __name__ == "__main__":
    guh ,player= FENtoBit("rnbqkbnr/ppp1pppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",True)
    guh,player= FENtoBit("rnbq2nr/ppp2ppp/8/1BbkP3/8/2P1P3/PP3PPP/RNB1K1NR w",True)
    #def testZeit():
    start_time = time.time()
    for x in range(10):
        spielBewertung(guh,player)
        print("time elapsed: {:.8f}s".format(time.time() - start_time))

    #testZeit()
