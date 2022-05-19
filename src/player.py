from lib2to3.pgen2.token import ISTERMINAL
import numpy as np
# requires: pip install anytree
from anytree import Node, RenderTree
import random

from bitboard import *
from tree import *
from movegen import *


# Player-Klasse. Macht eigentlich noch nix außer klartextübersetzung 1->W, -1->B, kann auch ersetzt werden.
class Player():
    def __init__(self):
        # weiß beginnt
        self.current = 1
    def __switch__(self):
        # wechselt die Spieler ab
        self.current *= -1
    def __set__(self, color_code):
        # setzt aktuellen Spieler -> vielleicht für funktion a la: bit, player = FENtoBit(FEN)
        if color_code == 'W':
            self.current = 1
        elif color_code == 'B':
            self.current = -1
        else:
            pass

    def __get__(self):
        # extrahiert aktuellen Spieler als String
        if self.current == 1:
            return 'W'
        elif self.current == -1:
            return 'B'
        else:
            return 'error'
    def utility(self,node):
        return spielBewertung(node,self.current)

    def alphabetasearch(self,node,depth=0,ismax=True):
        if depth==0 or node.children==None:
            return node.value
        if ismax:
            v=1000000
            for x in node.children:
                v=max(v,self.alphabetasearch(x,depth-1,False))
                node.value=v
            return v
        else:
            v=-1000000
            for x in node.children:
                v=min(v,self.alphabetasearch(x,depth-1,True))
                node.value=v
            return v

        #alphabetasearch
        #Node = findNode(ergebnis)
        #return tree with updated values
    #TODO insert functions in class
    
    
    
    
    
    def best_node(self,tree):
        #nodes height 1 sammeln
        children = tree.root.children
        if children: # falls Züge vorhanden
            values = [value for index,parent,b,value,h in children]
            #print(tree)
            #print(children)

            #return best node of nodes of tree height 1 
            best_nodes = []
            while True:
                possible_best_node = children[np.argmax(values)]
                children = children.remove(possible_best_node)
                values = [value for index,parent,b,value,h in children] 
                
                if best_nodes: # falls Liste schon Element enthält
                    if possible_best_node[3] == best_nodes[0][3]: # falls ein weiterer gleichwertiger Zug existiert
                        best_nodes.append(possible_best_node)
                    else: # falls nächstbester Zug schlechter
                        break # alle besten Züge gefunden
                else: # falls Liste noch leer
                    if checkmate(possible_best_node[2]) == False: # erster Zug muss auf jeden Fall legal sein
                        best_nodes.append(possible_best_node)
            # best_nodes sollte nun mindestens einen Zug enthalten. Dieser ist immer legal
            if len(best_nodes) == 1: # falls nur ein Zug vorhanden
                return best_nodes[0] # gib Zug zurück
            else:
                while True: # entferne Züge von Liste bis zufälliger legaler Zug gefunden
                    best_node = random.choice(best_nodes) # wähle zufällig besten Zug
                    if checkmate(best_node) == False: # falls Zug legal
                        return best_node # gib Zug zurück
                    else:
                        best_nodes.remove(best_node) 
             
        else:
            print('kein Zug vorhanden!')
            pass # kein Zug vorhanden

        

    def generate_moves(self,b):
        return generate_moves(b,self)

    def make_move(self,b_old,bb_from, bb_to):
        return make_move(b_old,bb_from,bb_to)

    def set_movetree(self,tree,h=0,index=0,step=0):#added züge zum baum, solange time = True
    #while (time-(tmax/2)>0):
    
        node=tree.find_node(index)
        print("node:")
        print(node)
        while node.h==h:
            moves=self.generate_moves(node.b)#liste aller moves von bb
            for b in moves:
                print("b:")
                print(b)
                tree.insert_node(node,[index,b,self.utility(b),h])  #in Node mit bitboard und wertung einsetzen
            index +=1
            node=tree.find_node(index)
        step+=index
        h+=1

        
        return tree,h,index, step

    def turn(self, FEN):#ein kompletter zug der ki
        time=2
        tmove=time/2
        tsearch=time/2
        bb=FENtoBit(FEN)
        tree=tree(bb)#leerer baum mit b als root
        if not checkmate(FEN,self):#Spielende überprüfen
            arr=self.set_movetree(tree,0,0,0)#arr=[tree,h,index,step]
            while(tmove>=0):#solange zeit ist
                for z in range(arr[3], arr[2]):#eine weitere ebene durchgehen
                    arr=self.set_movetree(tree,arr[1],z)#ein ausgerechneter zug alle züge ausrechnen
                tmove-=0.1
                time-=0.1
        
            #utility auf root?
            depth=1
            while(tsearch>=0):
                tiefe=self.alphabetasearch(tree.root,depth)#indizes aktualisieren#wertung des bestmöglichen zuges ausgeben
                depth+=1
                tsearch-=0.1
                time-=0.1

            index=self.best_node(tree)#besten zug auswaehlen
            move=tree.findNode(index)
            bb=self.make_move(move)
            FEN=BittoFEN(bb)
            return FEN



def checkmate(bitbrd,player):#Spiel nächsten Zug beendet -> True
       listeS = playerWert(bitbrd,player)
       schach = True
       for x in listeS:
              if bitbrd['k'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
                     schach = False
       if schach == True:
              return True
        
        



# erstellt ein array mit String values der position der Weißen oder Schwarzen Figuren
def playerWert(bitbrd,player):

    if player == 1:
          farbe = 'W'
    elif player == -1:
          farbe = 'B'
    somelist = []
    for num, x in enumerate(bitbrd[farbe], start=0):
          for sec, y in enumerate(bitbrd[farbe][num], start=0):
                 if bitbrd[farbe][num][sec] == True:
                        somelist.append(str(num) + ";" + str(sec))
    return somelist

# nimmt den array von playerWert und iterirt durch die verschiedenen Bitboard um nachzuprüfen um welche Figur es sich handelt
# Wert für Q = 9 R = 5 N = 3 B = 3 P = 1 K = 1
# Falls ein P ein ende erreicht nimmt er den Wert von 9 an
# Falls ein K die mittelpunkte erreicht kriegt er 1000 punkte erteilt weil er schon gewonnen hat


def calculateValue(bitbrd, listeS, player):
    wert = 0

    for x in listeS:
          if bitbrd['q'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
                 wert = wert + 9

    for x in listeS:
          if bitbrd['r'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
                 wert = wert + 5

    for x in listeS:
          if bitbrd['n'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
                 wert = wert + 3

    for x in listeS:
          if bitbrd['b'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
                 wert = wert + 3

    for x in listeS:
          if bitbrd['p'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
                if int(x.split(";")[0]) == 7 and player == 1:
                        wert = wert +9
                elif int(x.split(";")[0]) == 0 and player == -1:
                        wert = wert +9
                elif int(x.split(";")[0]) != 0:
                        wert = wert + 1

    for x in listeS:
          if bitbrd['k'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
                wert = wert + 1
                if int(x.split(";")[0]) == 3 and int(x.split(";")[1]) == 3:
                    wert = wert +1000
                if int(x.split(";")[0]) == 3 and int(x.split(";")[1]) == 4:
                    wert = wert +1000
                if int(x.split(";")[0]) == 4 and int(x.split(";")[1]) == 3:
                    wert = wert + 1000
                if int(x.split(";")[0]) == 4 and int(x.split(";")[1]) == 4:
                    wert = wert + 1000


    return wert

# Bewertungsfunktion nimmt ein Bitboard und den Player 1 wenn Weiß und -1 wenn Schwarz
def spielBewertung(bitbrd,player):
    wertW = calculateValue(bitbrd, playerWert(bitbrd, 1),1)
    wertB = calculateValue(bitbrd, playerWert(bitbrd, -1),-1)
    if player == 1:
        return wertW-wertB
    elif player == -1:
        return wertB-wertW
        





 
### DEMO ###
        

#Test tree.py
time=2
tmove=time/2
p=Player()    
bb=init_game(p)
tre=tree(bb)
tre.print_tree()
arr=p.set_movetree(tre)
while(tmove):#solange zeit ist
    for z in range(arr[3], arr[2]):#eine weitere ebene durchgehen
        arr=p.set_movetree(tre,arr[1],z)#ein ausgerechneter zug alle züge ausrechnen
        print("Tree"+z+":")
        tre.print_tree()
    tmove-=0.1



"""    
    
if __name__ == "__main__":
    player = Player()
    
    b = init_game(give_bitboards(), player)
    sbb = give_static_bitboards()
    print(print_board(b))

    print(player.__get__())
    
    b_test = player.make_move(b, bitboard(), bitboard())
    #b_test = make_move(b_test, bitboard(4), bitboard(43)) # Teststellung mit König auf d6 per illegalem zug
    #b_test = make_move(b_test, bitboard(1), bitboard(33)) # Teststellung mit Springer auf xy per illegalem zug
    #b_test = make_move(b_test, bitboard(6), bitboard(37)) # Teststellung mit Springer auf xy per illegalem zug
    #b_test = make_move(b_test, sbb['ld']&sbb['1'], sbb['lc']&sbb['5']) # Dame
    #b_test = make_move(b_test, sbb['lc']&sbb['1'], sbb['lf']&sbb['5']) # bishop
    b_test = player.make_move(b_test, sbb['la']&sbb['1'], sbb['lf']&sbb['5']) # rook
    #b_test = make_move(b_test, sbb['lc']&sbb['2'], sbb['lc']&sbb['4']) # pawns
    #b_test = make_move(b_test, sbb['ld']&sbb['7'], sbb['ld']&sbb['5']) # pawns

    print(print_board(b_test))
    print(player.__get__())

    cap, qui = generate_moves(b_test, player) # generiere alle Züge aus Position b
    print('capture:')
    #print(cap)
    print_board_list(cap)
    print('quiet:')
    #print(qui)
    print_board_list(qui)
"""