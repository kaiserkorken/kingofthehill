import numpy as np

from bitboard import *
import copy
import time

from movegen import *

bibsbbl=["la","lb","lc","ld","le","lf","lg","lh"]
bibsbbr=["1","2","3","4","5","6","7","8"]
bibp=["k","q","n","r","b","p"]


### ZUGGENERATOR ###

### https://www.chessprogramming.org/Pieces_versus_Directions

def make_move_id(b_old, bb_from, bb_to):
    pass

# erstellt lesbaren String in Quasi-Schachnotation
def make_move_name(b_old, bb_from, bb_to, short = False):
    #print(print_board(b_old))
    #print(bb_from)
    #print(bb_to)
    #print(bb_from & b_old['W'])
    #print(np.any(bb_from & b_old['W']))
    
    # Farbe
    if np.any(bb_from & b_old['W']):
        color = 'W'
        color_opponent = 'B'
    else:
        color = 'B'
        color_opponent = 'W'
        
    # Schlag oder Still
    if np.any(bb_to & b_old[color_opponent]):
        strike_or_quiet = 'x' # Schlag
    else:
        strike_or_quiet = '-' # Still
        
    # Figur
    piece="null"
    for p in bibp:
        
        if np.any(bb_from & b_old[p]):
            piece = p
    """        
    if piece == 'p': # Bauern werden nicht spezifiziert
        piece = ''#brauchen aber 
    """   
    if color == 'W': # Weiße Figuren werden groß geschrieben
        piece = piece.upper()
        
    # Felder
    line_from ,row_from ,line_to ,row_to="0","0","0","0"#TODO wieso kommt da nichts raus?
    for l in bibsbbl: # Linie
        if np.any(bb_from & sbb[l]):
            line_from = l[1]
        if np.any(bb_to & sbb[l]):
            line_to = l[1]
    for r in bibsbbr: # Reihe
        if np.any(bb_from & sbb[r]):
            row_from = r
        if np.any(bb_to & sbb[r]):
            row_to = r
        
            
    # Zusammensetzen
    
    
    if short:
        move = line_from + row_from + line_to + row_to
    else:
        move = piece + line_from + row_from + strike_or_quiet + line_to + row_to
    return move
            
    


def generate_moves_verbose(b, player):

    # king moves
    # queen moves
    # knight moves
    # rook moves
    # bishop moves
    # pawn moves
    
    t_start = time.time()
    ### erstelle Liste aller möglichen Züge durch Simulation ###

    # pawn to queen
#    print('pawn to queen')
    move_list_capture_pawn_to_queen, move_list_quiet_pawn_to_queen, name_list_capture_pawn_to_queen, name_list_quiet_pawn_to_queen = gen_moves_pawn_to_queen(b, player) 
    move_list_capture_king, move_list_quiet_king, name_list_capture_king, name_list_quiet_king = gen_moves_king(b, player)
    move_list_capture_queen, move_list_quiet_queen, name_list_capture_queen, name_list_quiet_queen = gen_moves_queen(b, player)
    move_list_capture_knight, move_list_quiet_knight, name_list_capture_knight, name_list_quiet_knight = gen_moves_knight(b, player) 
    move_list_capture_rook, move_list_quiet_rook, name_list_capture_rook, name_list_quiet_rook = gen_moves_rook(b, player) 
    move_list_capture_bishop, move_list_quiet_bishop, name_list_capture_bishop, name_list_quiet_bishop = gen_moves_bishop(b, player) 
    move_list_capture_pawn, move_list_quiet_pawn, name_list_capture_pawn, name_list_quiet_pawn = gen_moves_pawn(b, player) 
    
    #t_piece = time.time() - t_start
    #print("t_piece: " + str(t_piece))
#    """    
    move_list_capture = np.concatenate((move_list_capture_pawn_to_queen, 
                                        move_list_capture_king,
                                        move_list_capture_queen,
                                        move_list_capture_knight,
                                        move_list_capture_rook,
                                        move_list_capture_bishop,
                                        move_list_capture_pawn,
                                        ))
                                       
    # add quiet moves
    move_list_quiet = np.concatenate((move_list_quiet_pawn_to_queen, 
                                      move_list_quiet_king,
                                      move_list_quiet_queen,
                                      move_list_quiet_knight,
                                      move_list_quiet_rook,
                                      move_list_quiet_bishop,
                                      move_list_quiet_pawn,
                                      ))
      
    # corresponding move names
    name_list_capture = np.concatenate((name_list_capture_pawn_to_queen, 
                                        name_list_capture_king,
                                        name_list_capture_queen,
                                        name_list_capture_knight,
                                        name_list_capture_rook,
                                        name_list_capture_bishop,
                                        name_list_capture_pawn,
                                        ))
    
    name_list_quiet = np.concatenate((name_list_quiet_pawn_to_queen, 
                                      name_list_quiet_king,
                                      name_list_quiet_queen,
                                      name_list_quiet_knight,
                                      name_list_quiet_rook,
                                      name_list_quiet_bishop,
                                      name_list_quiet_pawn,
                                      ))
    
    move_list = np.concatenate((move_list_capture, move_list_quiet))
    name_list = np.concatenate((name_list_capture, name_list_quiet))
    
    #t_cat = time.time() - t_start - t_piece
    #print("t_cat: " + str(t_cat))
    """
    
     # list of list: liste mit elementen: liste mit allen zügen für jeden Figurentyp
    # add possible capture moves
    move_list_capture = []
    # add quiet moves
    move_list_quiet = []
    
    # corresponding move names
    name_list_capture = []
    name_list_quiet = []
    
    if move_list_capture_pawn_to_queen:
        move_list_capture.append(move_list_capture_pawn_to_queen)
        name_list_capture.append(name_list_capture_pawn_to_queen)
    if move_list_quiet_pawn_to_queen:
        move_list_quiet.append(move_list_quiet_pawn_to_queen)
        name_list_quiet.append(name_list_capture_pawn_to_queen)
    
    # king
#    print('king')
    if move_list_capture_king:
        move_list_capture.append(move_list_capture_king)
        name_list_capture.append(name_list_capture_king)
    if move_list_quiet_king:
        move_list_quiet.append(move_list_quiet_king)
        name_list_quiet.append(name_list_quiet_king)

    # queen
#    print('queen')
    if move_list_capture_queen:
        move_list_capture.append(move_list_capture_queen)
        name_list_capture.append(name_list_capture_queen)
    if move_list_quiet_queen:
        move_list_quiet.append(move_list_quiet_queen)
        name_list_quiet.append(name_list_quiet_queen)
    
    # knight
#    print('knight')
    if move_list_capture_knight:
        move_list_capture.append(move_list_capture_knight)
        name_list_capture.append(name_list_capture_knight)
    if move_list_quiet_knight:
        move_list_quiet.append(move_list_quiet_knight)
        name_list_quiet.append(name_list_quiet_knight)

    # rook
#    print('rook')
    if move_list_capture_rook:
        move_list_capture.append(move_list_capture_rook)
        name_list_capture.append(name_list_capture_rook)
    if move_list_quiet_rook:
        move_list_quiet.append(move_list_quiet_rook)
        name_list_quiet.append(name_list_quiet_rook)

        
    # bishop
#    print('bishop')
    if move_list_capture_bishop:
        move_list_capture.append(move_list_capture_bishop)
        name_list_capture.append(name_list_capture_bishop)
    if move_list_quiet_bishop:
        move_list_quiet.append(move_list_quiet_bishop)
        name_list_quiet.append(name_list_quiet_bishop)

    # pawn
#    print('pawn')
    if move_list_capture_pawn:
        move_list_capture.append(move_list_capture_pawn)
        name_list_capture.append(name_list_capture_pawn)
    if move_list_quiet_pawn:
        move_list_quiet.append(move_list_quiet_pawn)
        name_list_quiet.append(name_list_quiet_pawn)
        

    # flacht list of list zu liste ab [[a,b],[c,d]] -> [a,b,c,d] (zugehörigkeit für figuren geht flöten)
    move_list_capture_flat = flatten_list_of_list(move_list_capture)
    move_list_quiet_flat = flatten_list_of_list(move_list_quiet)
    
    name_list_capture_flat = flatten_list_of_list(name_list_capture)
    name_list_quiet_flat = flatten_list_of_list(name_list_quiet)
    '''
    print('TEST 3')
    print(str(len(move_list_capture_flat)) + " " + str(len(move_list_quiet_flat)))
    print(str(len(name_list_capture_flat)) + " " + str(len(name_list_quiet_flat)))
    '''
    
    move_list = np.concatenate((move_list_capture_flat, move_list_quiet_flat))
    name_list = np.concatenate((name_list_capture_flat, name_list_quiet_flat))
    
    """
   
#    print(move_list)
#    print(name_list)
    
    return move_list , name_list

# Hilfsfunktion für figurenspezifische Zuggeneratoren
def gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player, pawn_to_queen=False):
    # erstellt Listen mit Folgezuständen aus Liste in der Paare aus bb_from und bb_all_moves stehen
    # bb_from: einzelne 1 für bewegte Figur
    # bb_all_moves: 1en auf alle Felder die sich die Figur auf bb_from bewegen kann
    move_list_capture = []
    move_list_quiet = []
    
    name_list_capture = []
    name_list_quiet = []
    
    t_start = time.time()
    t = t_start
    
    for bb_from, bb_all_moves in bb_from_and_all_moves_list:
        #####
        #t_start = time.time()
        #t = t_start
        
        # teilt Züge in capture und quiet Züge auf.
        bb_capture, bb_quiet = split_capture_quiet(b, bb_all_moves, player)
        # erstellt für jeweils alle Züge Liste mit einzelnen Zügen
        bb_capture_list = serialize_bb(bb_capture)
        bb_quiet_list = serialize_bb(bb_quiet)
        
        #print('split: ')
        #print(time.time() - t)
        #t = time.time()
                
        if pawn_to_queen: # spezieller Zugsimulator für Damenumwandlung
            capture_list = [make_move_pawn_to_queen(b, bb_from, bb_to) for bb_to in bb_capture_list]
            quiet_list = [make_move_pawn_to_queen(b, bb_from, bb_to) for bb_to in bb_quiet_list]
            
        else:      
            # simuliert Züge -> Elemente sind Dictionaries mit Folgezuständen
            capture_list = [make_move(b, bb_from, bb_to) for bb_to in bb_capture_list]
            quiet_list = [make_move(b, bb_from, bb_to) for bb_to in bb_quiet_list]
            
        #print('make move: ')
        #print(time.time() - t)
        #t = time.time()
        
        # erstelle entsprechende Zugnotation
        capture_names = [make_move_name(b, bb_from, bb_to) for bb_to in bb_capture_list]
        quiet_names = [make_move_name(b, bb_from, bb_to) for bb_to in bb_quiet_list]
    
        #print('TEST')
        #print(str(len(capture_list)) + " " + str(len(quiet_list)))
        #print(str(len(capture_names)) + " " + str(len(quiet_names)))
        
        # füge keine leeren elemente ein
        if capture_list:
            move_list_capture.append(capture_list)
            name_list_capture.append(capture_names)
        if quiet_list:
            move_list_quiet.append(quiet_list)
            name_list_quiet.append(quiet_names)
        
        #print('make move names: ')
        #print(time.time() - t)
        #t = time.time()
        
    #print('moves: ')
    #print(time.time() - t)
    #t = time.time()
        
    # flacht list of list zu liste ab
    # zugehörigkeit für figuren eines Typs geht verloren
    move_list_capture_flat = flatten_list_of_list(move_list_capture)
    move_list_quiet_flat = flatten_list_of_list(move_list_quiet)
     
    name_list_capture_flat = flatten_list_of_list(name_list_capture)
    name_list_quiet_flat = flatten_list_of_list(name_list_quiet)
    
    #print('flatten: ')
    #print(time.time() - t)
    #t = time.time()
    '''
    print('TEST 2')
    print(str(len(move_list_capture_flat)) + " " + str(len(move_list_quiet_flat)))
    print(str(len(name_list_capture_flat)) + " " + str(len(name_list_quiet_flat)))
    '''
    return move_list_capture_flat, move_list_quiet_flat, name_list_capture_flat, name_list_quiet_flat




# Hilfsfunktion für figurenspezifische Zuggeneratoren
def gen_capture_quiet_lists_from_all_moves_bak(b, bb_from_and_all_moves_list, player, pawn_to_queen=False):
    # erstellt Listen mit Folgezuständen aus Liste in der Paare aus bb_from und bb_all_moves stehen
    # bb_from: einzelne 1 für bewegte Figur
    # bb_all_moves: 1en auf alle Felder die sich die Figur auf bb_from bewegen kann
    move_list_capture = []
    move_list_quiet = []
    
    name_list_capture = []
    name_list_quiet = []
    for bb_from, bb_all_moves in bb_from_and_all_moves_list:
        # teilt Züge in capture und quiet Züge auf.
        bb_capture, bb_quiet = split_capture_quiet(b, bb_all_moves, player)
        # erstellt für jeweils alle Züge Liste mit einzelnen Zügen
        bb_capture_list = serialize_bb(bb_capture)
        bb_quiet_list = serialize_bb(bb_quiet)
        
                
        if pawn_to_queen: # spezieller Zugsimulator für Damenumwandlung
            capture_list = [make_move_pawn_to_queen(b, bb_from, bb_to) for bb_to in bb_capture_list]
            quiet_list = [make_move_pawn_to_queen(b, bb_from, bb_to) for bb_to in bb_quiet_list]
            
        else:      
            # simuliert Züge -> Elemente sind Dictionaries mit Folgezuständen
            capture_list = [make_move(b, bb_from, bb_to) for bb_to in bb_capture_list]
            quiet_list = [make_move(b, bb_from, bb_to) for bb_to in bb_quiet_list]
            
        # erstelle entsprechende Zugnotation
        capture_names = [make_move_name(b, bb_from, bb_to) for bb_to in bb_capture_list]
        quiet_names = [make_move_name(b, bb_from, bb_to) for bb_to in bb_quiet_list]
    
        #print('TEST')
        #print(str(len(capture_list)) + " " + str(len(quiet_list)))
        #print(str(len(capture_names)) + " " + str(len(quiet_names)))
        
        # füge keine leeren elemente ein
        if capture_list:
            move_list_capture.append(capture_list)
            name_list_capture.append(capture_names)
        if quiet_list:
            move_list_quiet.append(quiet_list)
            name_list_quiet.append(quiet_names)
        
    # flacht list of list zu liste ab
    # zugehörigkeit für figuren eines Typs geht verloren
    move_list_capture_flat = flatten_list_of_list(move_list_capture)
    move_list_quiet_flat = flatten_list_of_list(move_list_quiet)
     
    name_list_capture_flat = flatten_list_of_list(name_list_capture)
    name_list_quiet_flat = flatten_list_of_list(name_list_quiet)
    '''
    print('TEST 2')
    print(str(len(move_list_capture_flat)) + " " + str(len(move_list_quiet_flat)))
    print(str(len(name_list_capture_flat)) + " " + str(len(name_list_quiet_flat)))
    '''
    return move_list_capture_flat, move_list_quiet_flat, name_list_capture_flat, name_list_quiet_flat



# Figurenspezifische Generatoren für capture und quiet Listen


def gen_moves_pawn_to_queen(b, player):
    # generates bb_lists with caputure and quiet moves
    if player == 1:
        bb_pawns = b['p'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_pawn_to_queen_W(b, bb_from)] for bb_from in serialize_bb(bb_pawns)] # iteriere über alle Türme
    else:
        bb_pawns = b['p'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_pawn_to_queen_B(b, bb_from)] for bb_from in serialize_bb(bb_pawns)] # iteriere über alle Türme
    
    # zu jeder Figur capture- und quiet-listen erstellen
    return gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player, pawn_to_queen=True)

def gen_moves_king(b, player):
    # generates bb_lists with caputure and quiet moves
    if player== 1:
        bb_from = b['k'] & b['W']
        bb_all_moves = moves_king_W(b)
    else:
        bb_from = b['k'] & b['B']
        bb_all_moves = moves_king_B(b)
    return gen_capture_quiet_lists_from_all_moves(b, [[bb_from, bb_all_moves]], player)

def gen_moves_queen(b, player):
    # generates bb_lists with caputure and quiet moves
    if player == 1:
        bb_from = b['q'] & b['W']
        bb_all_moves = moves_queen_W(b, bb_from)
    else:
        bb_from = b['q'] & b['B']
        bb_all_moves = moves_queen_B(b, bb_from)
        
    return gen_capture_quiet_lists_from_all_moves(b, [[bb_from, bb_all_moves]], player)

def gen_moves_knight(b, player):
    if player == 1:
        bb_knights = b['n'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_knight_W(b, bb_from)] for bb_from in serialize_bb(bb_knights)] # iteriere über alle Springer
    else:
        bb_knights = b['n'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_knight_B(b, bb_from)] for bb_from in serialize_bb(bb_knights)] # iteriere über alle Springer
    
    # zu jeder Figur capture- und quiet-listen erstellen
    return gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player)
    
    
def gen_moves_rook(b, player):
    # generates bb_lists with caputure and quiet moves
    if player == 1:
        bb_rooks = b['r'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_rook_W(b, bb_from)] for bb_from in serialize_bb(bb_rooks)] # iteriere über alle Türme
    else:
        bb_rooks = b['r'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_rook_B(b, bb_from)] for bb_from in serialize_bb(bb_rooks)] # iteriere über alle Türme
    
    # zu jeder Figur capture- und quiet-listen erstellen
    return gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player)
    
    
    
def gen_moves_bishop(b, player):
    # generates bb_lists with caputure and quiet moves
    if player == 1:
        bb_bishops = b['b'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_bishop_W(b, bb_from)] for bb_from in serialize_bb(bb_bishops)] # iteriere über alle Türme
    else:
        bb_bishops = b['b'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_bishop_B(b, bb_from)] for bb_from in serialize_bb(bb_bishops)] # iteriere über alle Türme
    
    # zu jeder Figur capture- und quiet-listen erstellen
    return gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player)

def gen_moves_pawn(b, player):
    # generates bb_lists with caputure and quiet moves
    if player == 1:
        bb_pawns = b['p'] & b['W']
        bb_from_and_all_moves_list = [[bb_from, moves_pawn_W(b, bb_from)] for bb_from in serialize_bb(bb_pawns)] # iteriere über alle Türme
    else:
        bb_pawns = b['p'] & b['B']
        bb_from_and_all_moves_list = [[bb_from, moves_pawn_B(b, bb_from)] for bb_from in serialize_bb(bb_pawns)] # iteriere über alle Türme
    
    # zu jeder Figur capture- und quiet-listen erstellen
    return gen_capture_quiet_lists_from_all_moves(b, bb_from_and_all_moves_list, player)


from player import *
def bench_movegen(FEN, iterations=100, verbose=True):
    print('1')
    player = Player()
    print('2')
    
    b, pl = FENtoBit(FEN, True)
    player.current = pl
    
    t_start = time.time()
    if verbose:
        for i in range(iterations):
            moves, names = generate_moves_verbose(b, player) # generiere alle Züge aus Position b
    else:
        for i in range(iterations):
            moves = generate_moves(b, player) # generiere alle Züge aus Position b
    t_end = time.time()
    return t_end-t_start

    
    
    

# Stellung 1: 
FEN_1 = 'rnbqkbnr/p4ppp/1p1pp3/2p5/3P4/NQP1PNPB/PP3P1P/R1B1K2R b'
possible_moves_1 = ['ke8-e7', 'qd8-h4', 'qd8-g5', 'qd8-f6', 'qd8-c7', 'qd8-d7', 'qd8-e7', 'nb8-d1',
 'nb8-a6', 'nb8-c6', 'nb8-d7', 'ng8xe1', 'ng8-f6', 'ng8-h6', 'ng8-e7', 'bc8-a6',
 'bc8-b7', 'bc8-d7', 'bf8-e7', 'c5-c4', 'c5xd4', 'b6-b5', 'd6-d5', 'e6-e5',
 'a7-a5', 'a7-a6', 'f7-f5', 'f7-f6', 'g7-g5', 'g7-g6', 'h7-h5', 'h7-h6']
# Stellung 2: 
FEN_2 = 'r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w'
possible_moves_2 = ['Bc1xg5', 'h4xg5', 'Ke1-d1', 'Ke1-f1', 'Ke1-e2', 'Ng1-e2', 'Ng1-f3', 'Ng1-h3',
 'Nb7-a5', 'Nb7-c5', 'Nb7-d6', 'Ra1-b1', 'Rh1-h2', 'Rh1-h3', 'Bc1-d2', 'Bc1-e3',
 'Bc1-f4', 'a2-a3', 'a2-a4', 'b2-b3', 'b2-b4', 'f2-f3', 'f2-f4', 'g2-g3', 'g2-g4',
 'c3-c4', 'd4-d5', 'c6-c7']


if __name__ == "__main__":
    verbose = True
    iterations = 1
    print('Benchmark: Movegen (verbose)')
    print('iterations: ' + str(iterations))
    time_stopped = bench_movegen(FEN_1, iterations, verbose)
    print("avg. time per ieration: " + str(time_stopped/iterations))

   
    verbose = False
    print('Benchmark: Movegen')
    print('iterations: ' + str(iterations))
    time_stopped = bench_movegen(FEN_1, iterations, verbose)
    print("avg. time per ieration: " + str(time_stopped/iterations)) 


