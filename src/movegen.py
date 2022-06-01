from bitboard import *
import copy


bibsbbl=["la","lb","lc","ld","le","lf","lg","lh"]
bibssbr=["1","2","3","4","5","6","7","8"]

### ZUG-SIMULATOR ###



def make_move(b_old, bb_from, bb_to):
    # Zuggenerator funktioniert!
    b_new = copy.deepcopy(b_old) # Tiefkopie wegen call-by-reference
    #if (bb_from | bb_to).any():
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


def make_move_pawn_to_queen(b_old, bb_from, bb_to):
    # Zuggenerator funktioniert!
    b_new = copy.deepcopy(b_old) # Tiefkopie wegen call-by-reference
    #if (bb_from | bb_to).any():
    for bb_key, bb in b_old.items():
        #print(bb_key)
        #print("FROM")
        #print(b_new[bb_key])
        if (bb & bb_to).any() : # falls gegnerische figur auf ziel auf bitboard verhanden
            b_new[bb_key] = bb  ^ bb_to # update bitboard: Schlag: Feld auf bb_to verschwindet


    b_new['p'] = b_new['p'] ^ bb_to # entferne Bauern nachträglich wieder
    b_new['q'] = b_new['q'] ^ bb_to # setze Dame
    #print("TO")
    #print(b_new[bb_key])  
    #print(print_board(b_new))
    return b_new





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
    
    # pawn to queen
#    print('pawn to queen')
    move_list_capture_pawn_to_queen, move_list_quiet_pawn_to_queen = gen_moves_pawn_to_queen(b, player) 
    if move_list_capture_pawn_to_queen:
        move_list_capture.append(move_list_capture_pawn_to_queen)
    if move_list_quiet_pawn_to_queen:
        move_list_quiet.append(move_list_quiet_pawn_to_queen)
    
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
        
    # rook
#    print('rook')
    move_list_capture_rook, move_list_quiet_rook = gen_moves_rook(b, player) 
    if move_list_capture_rook:
        move_list_capture.append(move_list_capture_rook)
    if move_list_quiet_rook:
        move_list_quiet.append(move_list_quiet_rook)

    # bishop
#    print('bishop')
    move_list_capture_bishop, move_list_quiet_bishop = gen_moves_bishop(b, player) 
    if move_list_capture_bishop:
        move_list_capture.append(move_list_capture_bishop)
    if move_list_quiet_bishop:
        move_list_quiet.append(move_list_quiet_bishop)
        
    # pawn
#    print('pawn')
    move_list_capture_pawn, move_list_quiet_pawn = gen_moves_pawn(b, player) 
    if move_list_capture_pawn:
        move_list_capture.append(move_list_capture_pawn)
    if move_list_quiet_pawn:
        move_list_quiet.append(move_list_quiet_pawn)

        
    # flacht list of list zu liste ab [[a,b],[c,d]] -> [a,b,c,d] (zugehörigkeit für figuren geht flöten)
    move_list_capture_flat = flatten_list_of_list(move_list_capture)
    move_list_quiet_flat = flatten_list_of_list(move_list_quiet)
    
    return np.concatenate((move_list_capture_flat, move_list_quiet_flat))



    
def split_capture_quiet(b, bb_to, player):
    if player.current:
        bb_opponent = b['B']
    else:
        bb_opponent = b['W']
    bb_capture = bb_to & bb_opponent # felder auf denen Gegner stehen: Capture
    bb_quiet = bb_to & ~bb_opponent # felder auf denen Gegner stehen: Quiet
    
    return bb_capture, bb_quiet


# Hilfsfunktion für figurenspezifische Zuggeneratoren
def gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player, pawn_to_queen=False):
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
        
        if pawn_to_queen:
            capture_list = [make_move_pawn_to_queen(b, bb_from, bb_to) for bb_to in bb_capture_list]
            quiet_list = [make_move_pawn_to_queen(b, bb_from, bb_to) for bb_to in bb_quiet_list]
        else:
            # simuliert Züge -> Elemente sind Dictionaries mit Folgezuständen
            capture_list = [make_move_pawn_to_queen(b, bb_from, bb_to) for bb_to in bb_capture_list]
            quiet_list = [make_move_pawn_to_queen(b, bb_from, bb_to) for bb_to in bb_quiet_list]
        
        # füge keine leeren elemente ein
        if capture_list:
            move_list_capture.append(capture_list)
        if quiet_list:
            move_list_quiet.append(quiet_list)
        
    # flacht list of list zu liste ab
    # zugehörigkeit für figuren eines Typs geht verloren
    move_list_capture_flat = flatten_list_of_list(move_list_capture)
    move_list_quiet_flat = flatten_list_of_list(move_list_quiet)
    
    return move_list_capture_flat, move_list_quiet_flat



# Figurenspezifische Generatoren für capture und quiet Listen


def gen_moves_king(b, player):
    # generates bb_lists with caputure and quiet moves
    if player.current == 1:
        bb_from = b['k'] & b['W']
        bb_all_moves = moves_king_W(b)
    else:
        bb_from = b['k'] & b['B']
        bb_all_moves = moves_king_B(b)
        
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, [[bb_from, bb_all_moves]], player)
    return move_list_capture, move_list_quiet

def gen_moves_queen(b, player):
    # generates bb_lists with caputure and quiet moves
    if player.current == 1:
        bb_from = b['q'] & b['W']
        bb_all_moves = moves_queen_W(b, bb_from, player)
    else:
        bb_from = b['q'] & b['B']
        bb_all_moves = moves_queen_B(b, bb_from, player)
        
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, [[bb_from, bb_all_moves]], player)
    return move_list_capture, move_list_quiet
    
def gen_moves_knight(b, player):
    if player.current == 1:
        bb_knights = b['n'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_knight_W(b, bb_from)] for bb_from in serialize_bb(bb_knights)] # iteriere über alle Springer
    else:
        bb_knights = b['n'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_knight_B(b, bb_from)] for bb_from in serialize_bb(bb_knights)] # iteriere über alle Springer
    
    # zu jeder Figur capture- und quiet-listen erstellen
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player)
    return move_list_capture, move_list_quiet
    
    
def gen_moves_rook(b, player):
    # generates bb_lists with caputure and quiet moves
    if player.current == 1:
        bb_rooks = b['r'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_rook_W(b, bb_from, player)] for bb_from in serialize_bb(bb_rooks)] # iteriere über alle Türme
    else:
        bb_rooks = b['r'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_rook_B(b, bb_from, player)] for bb_from in serialize_bb(bb_rooks)] # iteriere über alle Türme
    
    # zu jeder Figur capture- und quiet-listen erstellen
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player)
    return move_list_capture, move_list_quiet
    
    
    
def gen_moves_bishop(b, player):
    # generates bb_lists with caputure and quiet moves
    if player.current == 1:
        bb_bishops = b['b'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_bishop_W(b, bb_from, player)] for bb_from in serialize_bb(bb_bishops)] # iteriere über alle Türme
    else:
        bb_bishops = b['b'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_bishop_B(b, bb_from, player)] for bb_from in serialize_bb(bb_bishops)] # iteriere über alle Türme
    
    # zu jeder Figur capture- und quiet-listen erstellen
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player)
    return move_list_capture, move_list_quiet

def gen_moves_pawn(b, player):
    # generates bb_lists with caputure and quiet moves
    if player.current == 1:
        bb_pawns = b['p'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_pawn_W(b, bb_from)] for bb_from in serialize_bb(bb_pawns)] # iteriere über alle Türme
    else:
        bb_pawns = b['p'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_pawn_B(b, bb_from)] for bb_from in serialize_bb(bb_pawns)] # iteriere über alle Türme
    
    # zu jeder Figur capture- und quiet-listen erstellen
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player)
    return move_list_capture, move_list_quiet

def gen_moves_pawn_to_queen(b, player):
    # generates bb_lists with caputure and quiet moves
    if player.current == 1:
        bb_pawns = b['p'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_pawn_to_queen_W(b, bb_from)] for bb_from in serialize_bb(bb_pawns)] # iteriere über alle Türme
    else:
        bb_pawns = b['p'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_pawn_to_queen_B(b, bb_from)] for bb_from in serialize_bb(bb_pawns)] # iteriere über alle Türme
    
    # zu jeder Figur capture- und quiet-listen erstellen
    move_list_capture, move_list_quiet = gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player, pawn_to_queen=True)
    return move_list_capture, move_list_quiet

    
### POSSIBLE MOVES LOGIC ###

def moves_pawn_to_queen_W(b, bb_from):
    quiet = moves_quiet_pawn_to_queen_W(b, bb_from)
    attack = moves_attack_pawn_to_queen_W(b, bb_from)
    return (attack | quiet)

def moves_pawn_to_queen_B(b, bb_from):
    quiet = moves_quiet_pawn_to_queen_B(b, bb_from)
    attack = moves_attack_pawn_to_queen_B(b, bb_from)
    return (attack | quiet)

def moves_quiet_pawn_to_queen_W(b, bb_from):
    # shows possible normal moves of Black pawns
    one_step = np.roll(bb_from & sbb['7'], 8) & ~(b['W'] | b['B']) # last row: queen
    return (one_step)

def moves_quiet_pawn_to_queen_B(b, bb_from):
    # shows possible normal moves of Black pawns
    one_step = np.roll(bb_from & sbb['2'], -8)  & ~(b['W'] | b['B']) # last row: queen
    return (one_step)

def moves_attack_pawn_to_queen_W(b, bb_from):
    left_attack  = np.roll(bb_from & ~sbb['la'] & sbb['7'], 7) & b['B']
    right_attack = np.roll(bb_from & ~sbb['lh'] & sbb['7'], 9) & b['B']
    return (left_attack | right_attack)

def moves_attack_paw_to_queen_B(b, bb_from):
    left_attack  = np.roll(bb_from & ~sbb['la'] & sbb['2'], -9) & b['W']
    right_attack = np.roll(bb_from & ~sbb['lh'] & sbb['2'], -7) & b['W']
    return (left_attack | right_attack)



def moves_pawn_W(b, bb_from):
    quiet = moves_quiet_pawn_W(b, bb_from)
    attack = moves_attack_pawn_W(b, bb_from)
    return (attack | quiet)

def moves_pawn_B(b, bb_from):
    quiet = moves_quiet_pawn_B(b, bb_from)
    attack = moves_attack_pawn_B(b, bb_from)
    return (attack | quiet)

def moves_quiet_pawn_W(b, bb_from):
    # shows possible normal moves of Black pawns
    one_step = np.roll(bb_from &~sbb['7'], 8) & ~(b['W'] | b['B']) # last row: queen
    two_step = np.roll(bb_from & sbb['2'], 16) & ~(b['W'] | b['B'])
    return (one_step | two_step)

def moves_quiet_pawn_B(b, bb_from):
    # shows possible normal moves of Black pawns
    one_step = np.roll(bb_from &~sbb['2'], -8)  & ~(b['W'] | b['B']) # last row: queen
    two_step = np.roll(bb_from & sbb['7'], -16) & ~(b['W'] | b['B'])
    return (one_step | two_step)

def moves_attack_pawn_W(b, bb_from):
    left_attack  = np.roll(bb_from & ~sbb['la'] &~sbb['7'], 7) & b['B']
    right_attack = np.roll(bb_from & ~sbb['lh'] &~sbb['7'], 9) & b['B']
    return (left_attack | right_attack)

def moves_attack_pawn_B(b, bb_from):
    left_attack  = np.roll(bb_from & ~sbb['la'] &~sbb['2'], -9) & b['W']
    right_attack = np.roll(bb_from & ~sbb['lh'] &~sbb['2'], -7) & b['W']
    return (left_attack | right_attack)

# king
def kcolor(color):
    if color=="W":
        return "b"
    else:
        return "W"

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


def moves_queen_W(b, bb_from, player):
    # gibt bitboard mit allen Zügen der Dame aus
    # b: Spielfeld-Dictionary, bb_from: 1 an Position der Dame
    # Zielfelder der gegnerischen Figur sind erlaubt (Schlagen)
    # eigene Figuren sind Blockaden
    return moves_queen(b, bb_from, player) & ~( b['W']) 

def moves_queen_B(b, bb_from, player):
    return moves_queen(b, bb_from, player) & ~( b['B'])

def moves_queen(b, bb_from, player):#returns bitboard of all possible plays
    return (moves_bishop(b, bb_from, player) | moves_rook(b, bb_from, player))

# bishop moves
def moves_bishop_W(b, bb_from, player):
    return moves_bishop(b, bb_from, player) & ~( b['W'])

def moves_bishop_B(b, bb_from, player):
    return moves_bishop(b, bb_from, player) & ~( b['B'])

def moves_bishop(b, bb_from , player):
    #pseudocode:
    #Läufer Position mit Kreuz bitboards verunden (-> entsprechendes Kreuz auswählen)
    #idee kreuz bitboards: kreuz in der mitte implementieren und damm immer um pos(bishop) verschieben
    #-> Kreuz oder pos -> kreuz mit zügen
    #cut(Kreuz, color)
    #-> Kreuz geht nur bis dahin wo ein eigner spieler steht (<) oder ein gegnerischer spieler (<=) 

    if player.current:
        enemy = b['B']
        bb= b["W"]
    else:
        enemy = b['W']
        bb= b["B"]
    pos=np.where(bb_from)#position des läufers ermitteln
    #print(pos)#[x,y]

    #iterative variante:
    plays=bitboard()
    upbool=True#obenlinks (leider nur oben)
    rbool=True#obenrechts
    lbool=True#untenlinks
    dobool=True#untenrechts
    y=pos[1]
    x=pos[0]
    for z in range(1,7):
        if rbool and x+z<=7 and y+z<=7:#indices inbound
            s=enemy[x+z,y+z]
            if (bb[x+z,y+z]|s):#Feld besetzt
                rbool=False
                if (s):#feld mit gegner besetzt ->schlagen
                    plays[x+z,y+z]=1
            else:#feld frei
                plays[x+z,y+z]=1#mögl Zug
        if upbool and x-z>=0 and y+z<=7:
            s=enemy[x-z,y+z]
            if (bb[x-z,y+z]|s):#
                upbool=False
                if (s):
                    plays[x-z,y+z]=1
            else:
                plays[x-z,y+z]=1
        if lbool and x-z>=0 and y-z>=0:
            s=enemy[x-z,y-z]
            if (bb[x-z,y-z]|s):#
                lbool=False
                if (s):
                    plays[x-z,y-z]=1
            else:
                plays[x-z,y-z]=1
        if dobool and x+z<=7 and y-z>=0:
            s=enemy[x+z,y-z]
            if (bb[x+z,y-z]|s):#
                dobool=False
                if (s):
                    plays[x+z,y-z]=1
            else:
                plays[x+z,y-z]=1
#    print('plays:')
#    print(plays)
    plays = plays & ~(bb_from) # keine Züge auf die vorherige Person erlaubt
#    print(plays)
#    print('stop')
    return plays

# rook moves


def moves_rook_W(b, bb_from, player):
    return moves_rook(b, bb_from, player) & ~( b['W'])

def moves_rook_B(b, bb_from, player):
    return moves_rook(b, bb_from, player) & ~( b['B'])

def moves_rook(b, bb_from, player):#-> bitboard aller mögl züge des Turms
    
    #TODO implement Pseudocode
    #Turm Reihe und Spalte zuweisen
    #z.B. mit position mit zeilen und spalten bitboard verunden
    #-> Kreuz oder pos -> kreuz mit zügen
    #cut(Kreuz,color)
    # -> Kreuz geht nur bis dahin wo ein eigner spieler steht (<) oder ein gegnerischer spieler (<=) 

    if player.current:
        enemy = b['B']
        color= b["W"]
    else:
        enemy = b['W']
        color= b["B"]
    pos=np.where(bb_from)#position des turms ermitteln
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
    for z in range(1,7):
        if rbool and x+z<=7:#indices inbound
            s=enemy[x+z,y]
            if (color[x+z,y]|s):#Feld besetzt
                rbool=False
                if (s):#feld mit gegner besetzt ->schlagen
                    plays[x+z,y]=1
            else:#feld frei
                plays[x+z,y]=1#mögl Zug
        if upbool and y+z<=7:
            s=enemy[x,y+z]
            if (color[x,y+z]|s):#
                upbool=False
                if (s):
                    plays[x,y+z]=1
            else:
                plays[x,y+z]=1
        if lbool and x-z>=0:
            s=enemy[x-z,y]
            if (color[x-z,y]|s):#
                lbool=False
                if (s):
                    plays[x-z,y]=1
            else:
                plays[x-z,y]=1
        if dobool and y-z>=0:
            s=enemy[x,y-z]
            if (color[x,y-z]|s):#
                dobool=False
                if (s):
                    plays[x,y-z]=1
            else:
                plays[x,y-z]=1
#    plays = plays & ~(bb_from)
#    print(plays)
    return plays

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
    up_left    = np.roll((bb_from & ~(sbb['7']|sbb['8']|sbb['la'])),  16-1)
    up_right   = np.roll((bb_from & ~(sbb['7']|sbb['8']|sbb['lh'])),  16+1)
    # down
    down_left  = np.roll((bb_from & ~(sbb['1']|sbb['2']|sbb['la'])), -16-1)
    down_right = np.roll((bb_from & ~(sbb['1']|sbb['2']|sbb['lh'])), -16+1)
    # left
    left_up    = np.roll((bb_from & ~(sbb['7']|sbb['la']|sbb['lb'])),  -2+8)
    left_down  = np.roll((bb_from & ~(sbb['1']|sbb['la']|sbb['lb'])),  -2-8)
    # down
    right_up   = np.roll((bb_from & ~(sbb['7']|sbb['lg']|sbb['lh'])),   2+8)
    right_down = np.roll((bb_from & ~(sbb['1']|sbb['lg']|sbb['lh'])),   2-8)
    
    up = up_left|up_right
    down = down_left|down_right
    left = left_up|left_down
    right = right_up|right_down
    
    return up|down|left|right

### 



