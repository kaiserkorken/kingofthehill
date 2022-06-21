from bitboard import *
import copy
import time

from movegen import *

bibsbbl=["la","lb","lc","ld","le","lf","lg","lh"]
bibsbbr=["1","2","3","4","5","6","7","8"]
bibp=["k","q","n","r","b","p"]


### ZUGGENERATOR ###

### https://www.chessprogramming.org/Pieces_versus_Directions


    

def generate_moves(b, player):

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

    return moves

def generate_move(b, player):
    pass


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
    player = Player()
    
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


