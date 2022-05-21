import numpy as np
from player import *
from movegen_test import unit_test


# Stellung 1: 
FEN_1 = 'rnb1kbnr/p4ppp/1p1pp3/2p3q1/3P4/NQP1PNPB/PP3P1P/R1B1K2R b'
possible_moves_1 = 'a7a6, b8a6, b8c6, b8d7, c8b7, c8d7, e8d8, e8d7, e8e7, f8e7, g8e7, g8f6, g8h6, a7a5, b6b5, c5c4, c5d4, d6d5, e6e5, f7f6, f7f5, g7g6, h7h6, h7h5, g5f6, g5e7, g5d8, g5h6, g5f4, g5h4, g5e3'

# Stellung 2: 
FEN_2 = 'r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w'
possible_moves_2 = 'A1b1, c1d2, c1e3, c1f4, c1g5, e1d1, e1e1, e1d2, e1f1, g1e2, g1f3, g1h3, h1h2, h1h3, a2a3, a2a4, b2b3, b2b4, d4d5, f2f3, f2f4, g2g3, g2g4, h4g5, c6c7, b7d8, b7d6, b7c5, b7a5'


if __name__ == "__main__":
    
    print('Unit Test 1:')
    print('Moves to find:')
    print(possible_moves_1)
    unit_test(FEN_1)
    
    
    print('Unit Test 2:')
    print('Moves to find:')
    print(possible_moves_2)
    unit_test(FEN_2)