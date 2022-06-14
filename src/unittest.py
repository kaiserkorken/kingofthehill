import numpy as np
from player import *

from movegen_test import unit_test

    
 
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
    verbose = False
    
    print('Unit Test 1:')
    print('Moves to find: ' + str(len(possible_moves_1)) + ' move(s) possible')
    print(possible_moves_1)
    passed = unit_test(FEN_1, possible_moves_1, verbose)
    print('Unit test passed?: ' + str(passed))
    
    print('------------------')
    print('------------------')
    print('------------------')
    
    print('Unit Test 2:')
    print('Moves to find: ' + str(len(possible_moves_2)) + ' move(s) possible')
    print(possible_moves_2)
    passed = unit_test(FEN_2, possible_moves_2, verbose)
    print('Unit test passed?: ' + str(passed))
    