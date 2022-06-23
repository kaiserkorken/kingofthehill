from bitboard import *
from tt import ttable
import time


def utility(b,player,h,simple=True):
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
    
    
    return util
        
           


def simple_utility(b,player_code):
    piece_values = {'k':100, 'q':9, 'r':5, 'b':3, 'n':3, 'p':1}

       
    values_W = np.sum([np.sum(b[key] & b['W'])*piece_values[key] for key in piece_values])
    values_B = np.sum([np.sum(b[key] & b['B'])*piece_values[key] for key in piece_values])
    return player_code*(values_W - values_B)
    

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

def spielBewertung(BitBoard,Player):
    nesBoard = FENtoBoard(BittoFEN(BitBoard))
    valuesW = seitenWert(nesBoard,1)
    valuesB = seitenWert(nesBoard,-1)
    valuesP = pawnP(nesBoard,Player)

    if Player ==1:
        return valuesW-valuesB+valuesP
    elif Player ==-1:
        return valuesB-valuesW+valuesP
