from player import *
player = Player()  
def newGame():#unsere KI gegen sich selbst
    time=10
    player=[]
    player[0]=Player()
    player[1]=Player()
    FEN=BittoFEN(init_game())
    x=0
    while (not checkmate(FENtoBit(FEN),player[x])):
        FEN=player[x].turn(FEN,time)#TODO hier zeitbeschränkung z.B. per threads einbauen
        x=(x+1)%2#wechsel zwischen 0 und 1
        #print_bitboard(FEN)
    print("Spieler"+x+"hat verloren!")

### DEMO ###
#TODO Demo kompatibel mit neuen klassen
    

if __name__ == "__main__":
    pass