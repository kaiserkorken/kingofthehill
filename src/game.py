from player import *
player = Player()  
def turn(self, FEN):#ein kompletter zug der ki
    bb=FENtoBit(FEN)
    tree=tree(bb)#leerer baum mit b als root
    if not checkmate(FEN,player):#Spielende überprüfen
        arr=set_movetree(tree,0,0,0)#arr=[tree,h,index,step]
        while(time):#solange zeit ist
            for z in range(arr[3], arr[2]):#eine weitere ebene durchgehen
                arr=set_movetree(self,tree,arr[1],z)#ein ausgerechneter zug alle züge ausrechnen
    
        #utility auf root?
        tree=player.alphabetasearch(tree)#indizes aktualisieren
        index=player.best_node(tree)#besten zug auswaehlen
        move=tree.findNode(index)
        bb=player.make_move(move)
        FEN=BittoFEN(bb)
        return FEN


def set_movetree(self,tree,h=0,index=0,step=0):#added züge zum baum, solange time = True
    #while (time-(tmax/2)>0):
    
    b=tree.find_node(index)
    while b.h==h:
        moves=player.generatemoves(b.value)#liste aller moves von bb
        for x in moves:
            self.insert_node(b,[x,player.utility(x),h])  #in Node mit bitboard und wertung einsetzen
        index +=1
        b=tree.find_node(index)
    step+=index
    h+=1

    
    return tree,h,index, step

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
    

if __name__ == "__main__":

    b = init_game(give_bitboards(), player)

    print(print_board(b))

    print(player.__get__())

    print(print_board(b))

