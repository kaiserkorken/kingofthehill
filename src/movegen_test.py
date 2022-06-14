import numpy as np
from player import *
from movegen_verbose import make_move_name, generate_moves_verbose, print_board
import time


def unit_test(FEN, all_moves, verbose=False):
    player = Player()
    
    b, pl = FENtoBit(FEN, True)
    player.current = pl
#    print(player.current)
    
    moves, names = generate_moves_verbose(b, player.current) # generiere alle Züge aus Position b
    
    print('FEN loaded: ' + str(FEN)) # zeige genutzte FEN
    print('Player: ' + player.__get__()) # Spieler am Zug
    print(print_board(b, True))
    print('Number of moves found: ' + str(len(moves)))
    print(names)
    
    if verbose:
        # veranschauliche alle Züge
        for i in range(len(moves)):
            print('Move #'+str(i))
            print(names[i])
            print(print_board(moves[i], True))
          
    # falls sortierte Zuglisten identisch -> Unit-Test bestanden
    return sorted(all_moves) == sorted(names)

    
    

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
    iterations = 100
    print('Benchmark: Movegen (verbose)')
    print('iterations: ' + str(iterations))
    time_stopped = bench_movegen(FEN_1, iterations, verbose)
    print("avg. time per ieration: " + str(time_stopped/iterations))

   
    verbose = False
    print('Benchmark: Movegen')
    print('iterations: ' + str(iterations))
    time_stopped = bench_movegen(FEN_1, iterations, verbose)
    print("avg. time per ieration: " + str(time_stopped/iterations)) 
    
    
    