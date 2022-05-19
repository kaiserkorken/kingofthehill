from player import *
#player = Player()  

def newGame():#unsere KI gegen sich selbst
    player=[]
    player[0]=Player()
    player[1]=Player()
    FEN=BittoFEN(init_game())
    x=0
    while (not checkmate(FEN,player[x])):
        FEN=player[x].turn(FEN)#TODO hier zeitbeschränkung z.B. per threads einbauen
        x=(x+1)%2#wechsel zwischen 0 und 1
        #print_bitboard(FEN)
    print("Spieler"+x+"hat verloren!")

### DEMO ###
#TODO Demo kompatibel mit neuen klassen
    
        

    
b = init_game(player)
sbb = give_static_bitboards()
print(print_board(b))

print(player.__get__())

print(print_board(b))
#b1 = make_move(b, bitboard(4), bitboard(43)) # Teststellung mit König auf d6 per illegalem zug
b1 = make_move(b, bitboard(1), bitboard(33)) # Teststellung mit Springer auf xy per illegalem zug
b2 = make_move(b1, bitboard(6), bitboard(37)) # Teststellung mit Springer auf xy per illegalem zug



print(print_board(b2))
print(player.__get__())

cap, qui = generate_moves(b2, player) # generiere alle Züge aus Position b
print('capture:')
print(cap)
#print_board_list(cap)
print('quiet:')
print(qui)
#print_board_list(qui)