import numpy as np
# requires: pip install anytree
from anytree import Node, RenderTree
import copy
from interface import *


# Player-Klasse. Macht eigentlich noch nix außer klartextübersetzung 1->W, -1->B, kann auch ersetzt werden.
class Player():
    def __init__(self):
        # weiß beginnt
        self.current = 1
    def __switch__(self):
        # wechselt die Spieler ab
        self.current *= -1
    def __set__(self, color_code):
        # setzt aktuellen Spieler -> vielleicht für funktion a la: bit, player = FENtoBit(FEN)
        if color_code == 'W':
            self.current = 1
        elif color_code == 'B':
            self.current = -1
        else:
            pass

    def __get__(self):
        # extrahiert aktuellen Spieler als String
        if self.current == 1:
            return 'W'
        elif self.current == -1:
            return 'B'
        else:
            return 'error'
        
        
player = Player()  

def turn(self, FEN):#ein kompletter zug der ki
    bb=FENtoBit(FEN)
    checkmate(FEN,player)
    moves=player.generatemoves(bb)#liste aller moves
    for x in moves:#outsourcen
        tree.insertnode(x)#eine Node in Baum hinzufügen
    tree=player.utility(tree)#bewertungsfunktion ändert knoten des baums
    move=player.alphabetasearch(tree)
    bb=player.make_move(move)
    FEN=BittoFEN(bb)
    return FEN
def checkmate(FEN,player):
    b=BittoFEN(FEN)
    #TODO b-> Spiel beendet?
    #spiel gewonnen
    #player.win=True
    #return True

    #else:
    return False
def newGame():#unsere KI gegen sich selbst
    player=[]
    player[0]=Player()
    player[1]=Player()
    FEN=BittoFEN(init_game())
    #t=init_tree(FEN)#leerer baum mit FEN als root
    x=0
    while (not checkmate(FEN,player[x])):
        FEN=player[x].turn(FEN)#TODO hier zeitbeschränkung z.B. per threads einbauen
        x=(x+1)%2#wechsel zwischen 0 und 1
        #print_bitboard(FEN)
    print("Spieler"+x+"hat verloren!")


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
bibsbbl=["la","lb","lc","ld","le","lf","lg","lh"]
bibssbr=["1","2","3","4","5","6","7","8"]
        


def init_game(b, player):
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

    #print(b)
    
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
    if b_list:
        for b in b_list:
            if b:
                print(print_board(b, flip))
            else:
                print('empty board')
    else:
        print('empty b_list')
            
            

### PURE QUIET MOVES ###

def moves_quiet_pawns_W(b):
    # shows possible normal moves of Black pawns
    return np.roll((b['W'] & b['p']), 8) & ~(b['W'] | b['B'])

def moves_quiet_pawns_B(b):
    # shows possible normal moves of Black pawns
    
    #((B & SCH) >> 8) & ~(WEI | SCH)
    return np.roll((b['B'] & b['p']), -8) & ~(b['W'] | b['B'])

### PURE ATTACK MOVES ###

def moves_attack_pawns_W(b):
    pass

### AMBIGUOS MOVES ###

# king
def kcolor(color):
    if color=="W":
        return "b"
    else:
        return "W"

def moves_rook(b,color):#-> bitboard aller mögl züge des Turms
    enemy=kcolor(color)
    #TODO implement Pseudocode
    #Turm Reihe und Spalte zuweisen
    #z.B. mit position mit zeilen und spalten bitboard verunden
    #-> Kreuz oder pos -> kreuz mit zügen
    #cut(Kreuz,color)
    # -> Kreuz geht nur bis dahin wo ein eigner spieler steht (<) oder ein gegnerischer spieler (<=) 
    pos=np.where(b["r"]==1 & b[str(color)] ==1 )#position des turms ermitteln
    #print(pos)#[x,y]
    #kreuz=np.roll(sbb[bibsbbl[0]] & sbb[bibssbr[1]])#kreuz je nach position ausgeben
    #iterative variante:
    plays=bitboard()
    upbool=True
    rbool=True
    lbool=True
    dobool=True
    y=pos[1]
    x=pos[0]
    for z in range(7):
        if rbool and x+z<=7:#indices inbound
            s=b[enemy][x+z,y]
            if (b[color][x+z,y]|s):#Feld besetzt
                rbool=False
                if (s):#feld mit gegner besetzt ->schlagen
                    plays[x+z,y]=1
            else:#feld frei
                plays[x+z,y]=1#mögl Zug
        if upbool and y+z<=7:
            s=b[enemy][x,y+z]
            if (b[color][x,y+z]|s):#
                upbool=False
                if (s):
                    plays[x,y+z]=1
            else:
                plays[x,y+z]=1
        if lbool and x-z>=0:
            s=b[enemy][x-z,y]
            if (b[color][x-z,y]|s):#
                lbool=False
                if (s):
                    plays[x-z,y]=1
            else:
                plays[x-1,y]=1
        if dobool and y-z>=0:
            s=b[enemy][x,y-z]
            if (b[color][x,y-z]|s):#
                dobool=False
                if (s):
                    plays[x,y-z]=1
            else:
                plays[x,y-z]=1
    return plays

def moves_bishop(b, color):
    #Läufer Position mit Kreuz bitboards verunden (-> entsprechendes Kreuz auswählen)
    #idee kreuz bitboards: kreuz in der mitte implementieren und damm immer um pos(bishop) verschieben
    #-> Kreuz oder pos -> kreuz mit zügen
    #cut(Kreuz, color)
    #-> Kreuz geht nur bis dahin wo ein eigner spieler steht (<) oder ein gegnerischer spieler (<=) 
    pos=np.where(b["b"]==1 & b[str(color)] ==1 )#position des läufers ermitteln
    #print(pos)#[x,y]
    enemy=kcolor(color)

    #iterative variante:
    plays=bitboard()
    upbool=True#obenlinks
    rbool=True#obenrechts
    lbool=True#untenlinks
    dobool=True#untenrechts
    y=pos[1]
    x=pos[0]
    for z in range(7):
        if rbool and x+z<=7 and y+z<=7:#indices inbound
            s=b[enemy][x+z,y+z]
            if (b[color][x+z,y+z]|s):#Feld besetzt
                rbool=False
                if (s):#feld mit gegner besetzt ->schlagen
                    plays[x+z,y+z]=1
            else:#feld frei
                plays[x+z,y]=1#mögl Zug
        if upbool and x-z>=0 and y+z<=7:
            s=b[enemy][x-z,y+z]
            if (b[color][x-z,y+z]|s):#
                upbool=False
                if (s):
                    plays[x-z,y+z]=1
            else:
                plays[x-z,y+z]=1
        if lbool and x-z>=0 and y-z>=0:
            s=b[enemy][x-z,y-z]
            if (b[color][x-z,y-z]|s):#
                lbool=False
                if (s):
                    plays[x-z,y-z]=1
            else:
                plays[x-1,y-z]=1
        if dobool and x+z<=7 and y-z>=0:
            s=b[enemy][x+z,y-z]
            if (b[color][x+z,y-z]|s):#
                dobool=False
                if (s):
                    plays[x+z,y-z]=1
            else:
                plays[x+z,y-z]=1
    return plays

def cut(b, color):#bitboard -> gekürztes bitboard je nachdem, wo andere spielfiguren stehen
    # von pos immer dem kreuz entlang bis: (x)
    # x und color -> 0
    # x und !color -> 1 
    # danach stopp
    # rest bleibt
    #return kreuz
    pass

def moves_king_W(b):
    # king can only move up if it is not in the upper row, etc. 
    up    = np.roll((b['W'] & b['k'] & ~sbb['8']),   8) & ~(b['W'] )
    down  = np.roll((b['W'] & b['k'] & ~sbb['1']),  -8) & ~(b['W'] )
    left  = np.roll((b['W'] & b['k'] & ~sbb['la']), -1) & ~(b['W'] )
    right = np.roll((b['W'] & b['k'] & ~sbb['lh']),  1) & ~(b['W'] )
    return (up|down|left|right)


def moves_king_B(b):
    # bb_from nicht nötig, da Position durch Schnittmenge mit Farbe und König eindeutig bestimmt
    # king can only move up if it is not in the upper row, etc. 
    up    = np.roll((b['B'] & b['k'] & ~sbb['8']),   8) & ~( b['B'])
    down  = np.roll((b['B'] & b['k'] & ~sbb['1']),  -8) & ~( b['B'])
    left  = np.roll((b['B'] & b['k'] & ~sbb['la']), -1) & ~( b['B'])
    right = np.roll((b['B'] & b['k'] & ~sbb['lh']),  1) & ~( b['B'])
    return (up|down|left|right)
    


# queen moves
def moves_queen(b):#returns bitboard of all possible plays
    return (moves_bishop(b)|moves_rook(b))

def moves_queen_W(b, bb_from):
    return moves_queen(b, bb_from) & ~( b['W']) # Zielfelder der gegnerischen Figur sind erlaubt (Schlagen)
eigene Figuren sind Blockaden

def moves_queen_B(b, bb_from):
    return moves_queen(b, bb_from) & ~( b['B'])

# bishop moves
def moves_bishop_W(b, bb_from):
    return moves_bishop(b, bb_from) & ~( b['W'])

def moves_bishop_B(b, bb_from):
    return moves_bishop(b, bb_from) & ~( b['B'])

# rook moves
def moves_rook_W(bb_from):
    return moves_rook(b, bb_from) & ~( b['W'])

def moves_rook_B(bb_from):
    return moves_rook(b, bb_from) & ~( b['B'])

# knight moves
def moves_knight_W(b, bb_from): 
    return moves_knight(b, bb_from) & ~( b['W'])
    
def moves_knight_B(b, bb_from):
    return moves_knight(b, bb_from) & ~( b['B'])

def moves_knight(b, bb_from):
    # erzeugt bb mit allen zügen von bb_from aus
    # bb_from: True an Koordinate an der Springer steht
    # first_second -> 2 in first dir, 1 in second dir
    # up
    up_left    = np.roll((bb_from & ~sbb['6'] & ~sbb['la']),  16-1)
    up_right   = np.roll((bb_from & ~sbb['6'] & ~sbb['lh']),  16+1)
    # down
    down_left  = np.roll((bb_from & ~sbb['2'] & ~sbb['la']), -16-1)
    down_right = np.roll((bb_from & ~sbb['2'] & ~sbb['lh']), -16+1)
    # left
    left_up    = np.roll((bb_from & ~sbb['7'] & ~sbb['lb']),  -2+8)
    left_down  = np.roll((bb_from & ~sbb['1'] & ~sbb['lb']),  -2-8)
    # down
    right_up   = np.roll((bb_from & ~sbb['7'] & ~sbb['lg']),   2+8)
    right_down = np.roll((bb_from & ~sbb['1'] & ~sbb['lg']),   2-8)
    
    up = up_left|up_right
    down = down_left|down_right
    left = left_up|left_down
    right = right_up|right_down
    
    return up|down|left|right

### 


### ZUG-SIMULATOR ###



#ziehende Figur: BB(From) OR BB(To) XOR BB(gezogene Figur)
#geschlagene Figur: bb(geschlagene Figur) XOR BB(To) -> (Figur)
'''
def make_move_quiet(b, bb_from, bb_to, bb_piece):
    for bb in b:
        b[bb] = (bb_from | bb_to) ^ bb_piece
    return b

def make_move_attack(b, bb_from, bb_to, bb_piece, bb_enemy_piece):
    for bb in b:
        b[bb] = (bb_from | bb_to) ^ bb_piece
        b[bb] = (bb_enemy_piece ^ bb_to) ^ bb_piece
    return b
'''


def make_move(b_old, bb_from, bb_to):
    # Zuggenerator funktioniert!
    b_new = copy.deepcopy(b_old) # Tiefkopie wegen call-by-reference
    
    for bb_key, bb in b_old.items():
        #print(bb_key)
        #print("FROM")
        #print(b_new[bb_key])
        if (bb & bb_to).any() : # falls gegnerische figur auf ziel auf bitboard verhanden
            b_new[bb_key] = bb  ^ bb_to # update bitboard: Schlag: Feld auf bb_to verschwindet
            
        if (bb & bb_from).any() : # falls eigene figur auf bitboard verhanden
            b_new[bb_key] = (bb | bb_to) ^ bb_from # update bitboard : Feld auf bb_to entsteht, Feld auf bb_from verschwindet
        #print("TO")
        #print(b_new[bb_key])  
    #print(print_board(b_new))
    return b_new



def serialize_bb(bb):
    # gibt einzelne bitboards für jedes True an entsprechender Stelle zurück
    return [bitboard(index) for index in np.flatnonzero(bb)]

def split_capture_quiet(b, bb_to, player):
    if player.current:
        bb_opponent = b['B']
    else:
        bb_opponent = b['W']
    bb_capture = bb_to & bb_opponent # felder auf denen Gegner stehen: Capture
    bb_quiet = bb_to & ~bb_opponent # felder auf denen Gegner stehen: Quiet
    
    return bb_capture, bb_quiet

def flatten_list_of_list(list_of_list):
    # flacht list of list zu liste ab [[a,b],[c,d]] -> [a,b,c,d] (zb: zugehörigkeit für figuren geht flöten)
    #[item for sublist in t for item in sublist]
    return [item for sublist in list_of_list for item in sublist]
    

### ZUGGENERATOR ###

### https://www.chessprogramming.org/Pieces_versus_Directions



def generate_moves(b, player):

    # king moves
    # queen moves
    # knight moves
    # rook moves
    # bishop moves
    # pawn moves
    
    
    ### erstelle Liste aller möglichen Züge durch Simulation ###
    
    # list of list: liste mit elementen: liste mit allen zügen für jeden Figurentyp
    # add possible capture moves
    move_list_capture = []
    # add quiet moves
    move_list_quiet = []
    
    # king
#    print('king')
    move_list_capture_king, move_list_quiet_king = gen_moves_king(b, player)
    if move_list_capture_king:
        move_list_capture.append(move_list_capture_king)
    if move_list_quiet_king:
        move_list_quiet.append(move_list_quiet_king)
        
    # queen
#    print('queen')
    move_list_capture_queen, move_list_quiet_queen = gen_moves_queen(b, player)
    if move_list_capture_queen:
        move_list_capture.append(move_list_capture_queen)
    if move_list_quiet_queen:
        move_list_quiet.append(move_list_quiet_queen)
    
    # knight
#    print('knight')
    move_list_capture_knight, move_list_quiet_knight = gen_moves_knight(b, player) 
    if move_list_capture_knight:
        move_list_capture.append(move_list_capture_knight)
    if move_list_quiet_knight:
        move_list_quiet.append(move_list_quiet_knight)
    
    # flacht list of list zu liste ab [[a,b],[c,d]] -> [a,b,c,d] (zugehörigkeit für figuren geht flöten)
    move_list_capture_flat = flatten_list_of_list(move_list_capture)
    move_list_quiet_flat = flatten_list_of_list(move_list_quiet)
    
    return move_list_capture_flat, move_list_quiet_flat


# Hilfsfunktion für figurenspezifische Zuggeneratoren
def gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list):
    # erstellt Listen mit Folgezuständen aus Liste in der Paare aus bb_from und bb_all_moves stehen
    # bb_from: einzelne 1 für bewegte Figur
    # bb_all_moves: 1en auf alle Felder die sich die Figur auf bb_from bewegen kann
    move_list_capture = []
    move_list_quiet = []
    for bb_from, bb_all_moves in bb_from_and_all_moves_list:
        # teilt Züge in capture und quiet Züge auf.
        bb_capture, bb_quiet = split_capture_quiet(b, bb_all_moves, player)
        # erstellt für jeweils alle Züge Liste mit einzelnen Zügen
        bb_capture_list = serialize_bb(bb_capture)
        bb_quiet_list = serialize_bb(bb_quiet)
        
        # simuliert Züge -> Elemente sind Dictionaries mit Folgezuständen
        capture_list = [make_move(b, bb_from, bb_to) for bb_to in bb_capture_list]
        quiet_list = [make_move(b, bb_from, bb_to) for bb_to in bb_quiet_list]
        
        # füge keine leeren elemente ein
        if capture_list:
            move_list_capture.append(capture_list)
        if quiet_list:
            move_list_quiet.append(quiet_list)
        
    # flacht list of list zu liste ab
    # zugehörigkeit für figuren eines Typs geht verloren
    move_list_capture_flat = flatten_list_of_list(move_list_capture)
    move_list_quiet_flat = faltten_list_of_list(move_list_quiet)
    
    return move_list_capture_flat, move_list_quiet_flat



# Figurenspezifische Generatoren für capture und quiet Listen

def gen_moves_pawn(b, player):
    pass

def gen_moves_king(b, player):
    # generates bb_lists with caputure and quiet moves
    if player.current == 1:
        bb_from = b['k'] & b['W']
        bb_all_moves = moves_king_W(b)
    else:
        bb_from = b['k'] & b['B']
        bb_all_moves = moves_king_B(b)
        
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, [[bb_from, bb_all_moves]])
    return move_list_capture, move_list_quiet

def gen_moves_queen(b, player):
    # generates bb_lists with caputure and quiet moves
    if player.current == 1:
        bb_from = b['q'] & b['W']
        bb_all_moves = moves_queen_W(b)
    else:
        bb_from = b['q'] & b['B']
        bb_all_moves = moves_queen_B(b)
        
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, [[bb_from, bb_all_moves]])
    return move_list_capture, move_list_quiet
    
def gen_moves_knight(b, player):
    if player.current == 1:
        bb_knights = b['n'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_knight_W(b, bb_from)] for bb_from in serialize_bb(bb_knights)] # iteriere über alle Springer
    else:
        bb_knights = b['n'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_knight_B(b, bb_from)] for bb_from in serialize_bb(bb_knights)] # iteriere über alle Springer
    
    # zu jeder Figur capture- und quiet-listen erstellen
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list)
    return move_list_capture, move_list_quiet
    
    
    
### DEMO ###
    
    
    
b = init_game(give_bitboards(), player)
sbb = give_static_bitboards()
print(print_board(b))

print(player.__get__())

#b1 = make_move(b, bitboard(4), bitboard(43)) # Teststellung mit König auf d6 per illegalem zug
b1 = make_move(b, bitboard(1), bitboard(33)) # Teststellung mit Springer auf xy per illegalem zug
b2 = make_move(b1, bitboard(6), bitboard(37)) # Teststellung mit Springer auf xy per illegalem zug



print(print_board(b2))
print(player.__get__())

cap, qui = generate_moves(b2, player) # generiere alle Züge aus Position b
print('capture:')
#print(cap)
print_board_list(cap)
print('quiet:')
#print(qui)
print_board_list(qui)
