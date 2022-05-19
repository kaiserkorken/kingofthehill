from player import *
player = Player()  
def newGame():#unsere KI gegen sich selbst
    player=[]
    player[0]=Player()
    player[1]=Player()
    FEN=BittoFEN(init_game(player[0]))
    x=0
    while (not checkmate(FEN,player[x])):
        FEN=player[x].turn(FEN)#TODO hier zeitbeschränkung z.B. per threads einbauen
        x=(x+1)%2#wechsel zwischen 0 und 1
        #print_bitboard(FEN)
    print("Spieler"+x+"hat verloren!")

### DEMO ###
#TODO Demo kompatibel mit neuen klassen
    

if __name__ == "__main__":

    b = init_game(give_bitboards(), player)

    print(print_board(b))

    print(player.__get__())

    cap, qui = generate_moves(b, player) # generiere alle Züge aus Position b
    print('capture:')
    print(cap)
    #print_board_list(cap)
    print('quiet:')
    print(qui)
    #print_board_list(qui)