from bitboard import *



def utility(b, player, simple=True):
#    print('new')
#    print(simple_utility(b,player))
#    print(spielBewertung(b,player))
    if simple:
        return simple_utility(b,player)
    else:
        return spielBewertung(b,player)

def simple_utility(b,player):
    piece_values = {'k':100, 'q':9, 'r':5, 'b':3, 'n':3, 'p':1}

       
    values_W = np.sum([np.sum(b[key] & b['W'])*piece_values[key] for key in piece_values])
    values_B = np.sum([np.sum(b[key] & b['B'])*piece_values[key] for key in piece_values])
    return player*(values_W - values_B)
    

# erstellt ein array mit String values der position der Weißen oder Schwarzen Figuren
def playerWert(bitbrd, player):
    if player == 1:
        farbe = 'W'
    else:
        farbe = 'B'
    somelist = []
    for num, x in enumerate(bitbrd[farbe], start=0):
        for sec, y in enumerate(bitbrd[farbe][num], start=0):
            if bitbrd[farbe][num][sec] == True:
                somelist.append(str(num) + ";" + str(sec))
    return somelist


# nimmt den array von playerWert und iterirt durch die verschiedenen Bitboard um nachzuprüfen um welche Figur es sich handelt
# Wert für Q = 9 R = 5 N = 3 B = 3 P = 1 K = 1
# Falls ein P ein ende erreicht nimmt er den Wert von 9 an
# Falls ein K die mittelpunkte erreicht kriegt er 1000 punkte erteilt weil er schon gewonnen hat


def calculateValue(bitbrd, listeS, player):
    wert = 0

    for x in listeS:
        if bitbrd['q'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
            wert = wert + 9

    for x in listeS:
        if bitbrd['r'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
            wert = wert + 5

    for x in listeS:
        if bitbrd['n'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
            wert = wert + 3

    for x in listeS:
        if bitbrd['b'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
            wert = wert + 3

    for x in listeS:
        if bitbrd['p'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
            if int(x.split(";")[0]) == 7 and player == 1:
                wert = wert + 9
            elif int(x.split(";")[0]) == 0 and player == -1:
                wert = wert + 9
            elif int(x.split(";")[0]) != 0:
                wert = wert + 1

    for x in listeS:
        if bitbrd['k'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
            wert = wert + 1
            if int(x.split(";")[0]) == 3 and int(x.split(";")[1]) == 3:
                wert = 100
            if int(x.split(";")[0]) == 3 and int(x.split(";")[1]) == 4:
                wert = 100
            if int(x.split(";")[0]) == 4 and int(x.split(";")[1]) == 3:
                wert = 100
            if int(x.split(";")[0]) == 4 and int(x.split(";")[1]) == 4:
                wert = 100

    return wert


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


testBoard = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["--", "bp", "--", "--", "bp", "bp", "bp", "bp"],
    ["--", "bp", "--", "--", "bp", "--", "bp", "--"],
    ["--", "bp", "--", "--", "--", "--", "--", "--"],
    ["--", "wp", "--", "--", "--", "--", "wp", "--"],
    ["--", "--", "--", "bp", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "--", "--", "--"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

# print(doubledPawns(testBoard,"b"))

testBoardB = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["bp", "bp", "--", "--", "bp", "--", "bp", "--"],
    ["--", "bp", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "wp", "--", "--", "--", "--"],
    ["--", "--", "--", "wp", "--", "--", "bN", "--"],
    ["wp", "wp", "--", "wp", "--", "wp", "wp", "wp"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


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


testBoardC = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["--", "--", "--", "--", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["bp", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "bp", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


# print(isolatedPawns(testBoardC,'b'))

def pawnP(board, player):
    if player == -1:
        return (doubledPawns(board, 'w') + blockedPawns(board, 'w') + isolatedPawns(board, 'w')) - \
               (doubledPawns(board, 'b') + blockedPawns(board, 'b') + isolatedPawns(board, 'b'))

    elif player == 1:
        return (doubledPawns(board, 'b') + blockedPawns(board, 'b') + isolatedPawns(board, 'b')) - \
               (doubledPawns(board, 'w') + blockedPawns(board, 'w') + isolatedPawns(board, 'w'))


# print(doubledPawns(testBoard,'w'))
# print(blockedPawns(testBoard,'w'))
# print(isolatedPawns(testBoard,'w'))
# print(doubledPawns(testBoard,'b'))
# print(blockedPawns(testBoard,'b'))
# print(isolatedPawns(testBoard,'b'))


# Bewertungsfunktion nimmt ein Bitboard und den Player 1 wenn Weiß und -1 wenn Schwarz
def spielBewertung(bitbrd, player):
    wertW = calculateValue(bitbrd, playerWert(bitbrd, 1), 1)
    wertB = calculateValue(bitbrd, playerWert(bitbrd, -1), -1)
    pracTable = pawnP(FENtoBoard(BittoFEN(bitbrd, player)), player)
    #print(pracTable)
    if wertW==None or wertB==None or pracTable==None:
        print(wertW, wertB ,pracTable)
    if player == 1:
        return wertW - wertB + pracTable
    elif player == -1:
        return wertB - wertW + pracTable