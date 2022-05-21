import numpy as np
from player import *
from movegen_verbose import make_move_name, generate_moves_verbose


def unit_test(FEN):
    player = Player()
    
    b, pl = FENtoBit(FEN, True)
    player.current = pl
    
    moves, names = generate_moves_verbose(b, player) # generiere alle Züge aus Position b
    
    print('FEN loaded: ' + str(FEN))
    print('Player: ' + player.__get__())
    print(print_board(b, True))
    print('Number of moves found: ' + str(len(moves)))
    print(names)
    
    for i in range(len(moves)):
        print('Move #'+str(i))
        print(names[i])
        print(print_board(moves[i], True))
    
    

if __name__ == "__main__":
    player = Player()
    
    b = init_game(player)
    sbb = give_static_bitboards()
    print(print_board(b))

    print(player.__get__())
    
    b_test = player.make_move(b, bitboard(), bitboard())
    #b_test = make_move(b_test, bitboard(4), bitboard(43)) # Teststellung mit König auf d6 per illegalem zug
    #b_test = make_move(b_test, bitboard(1), bitboard(33)) # Teststellung mit Springer auf xy per illegalem zug
    #b_test = make_move(b_test, bitboard(6), bitboard(37)) # Teststellung mit Springer auf xy per illegalem zug
    #b_test = make_move(b_test, sbb['ld']&sbb['1'], sbb['lc']&sbb['5']) # Dame
    #b_test = make_move(b_test, sbb['lc']&sbb['1'], sbb['lf']&sbb['5']) # bishop
    print(make_move_name(b_test, sbb['la']&sbb['1'], sbb['lf']&sbb['5']))
    b_test = player.make_move(b_test, sbb['la']&sbb['1'], sbb['lf']&sbb['5']) # rook
    print('second_move')
    print(make_move_name(b_test, sbb['la']&sbb['2'], sbb['la']&sbb['6']))
    b_test = player.make_move(b_test, sbb['la']&sbb['2'], sbb['la']&sbb['6']) # rook
    
    #b_test = make_move(b_test, sbb['lc']&sbb['2'], sbb['lc']&sbb['4']) # pawns
    #b_test = make_move(b_test, sbb['ld']&sbb['7'], sbb['ld']&sbb['5']) # pawns

    print(print_board(b_test))
    print(player.__get__())

    moves, names = generate_moves_verbose(b_test, player) # generiere alle Züge aus Position b
    moves = list(moves)
    names = list(names)
    
    print(type(moves))
    print(len(moves))
    print(type(names))
    print(len(names))
    '''
    print(moves)
    cap = moves[0]
    qui = moves[1]
    print('capture:')
    print(len(cap))
    print(cap)
    print_board_list(cap)
    print('quiet:')
    print(len(qui))
    print(qui)
    print_board_list(qui)
    '''
    print_board_list(moves)
    print(names)