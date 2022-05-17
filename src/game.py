from player import *
player = Player()  
def turn(self, FEN):#ein kompletter zug der ki
    bb=FENtoBit(FEN)
    tree=tree(bb)#leerer baum mit b als root
    if not checkmate(FEN,player):#Spielende überprüfen
        moves=player.generatemoves(bb)#liste aller moves
        #utility auf root?
        for x in moves:#outsourcen
            tree.insert_node([x,player.utility(x)])#in Node mit bitboard und wertung einsetzen
        tree=player.alphabetasearch(tree)#indizes aktualisieren
        index=player.best_node(tree)#besten zug auswaehlen
        move=tree.findNode(index)
        bb=player.make_move(move)
        FEN=BittoFEN(bb)
        return FEN
def checkmate(FEN,player):#Spiel nächsten Zug beendet -> True
    b=BittoFEN(FEN)
    #TODO b-> Spiel beendet?
    #spiel gewonnen
    #player.win=True
    #return True

    #else:
    return False#kein Schachmatt
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
    
        

    
b = init_game(give_bitboards(), player)
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