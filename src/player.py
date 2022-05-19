import numpy as np
# requires: pip install anytree
from anytree import Node, RenderTree
import random
import copy
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
        spielBewertung(node,self.current)

    def alphabetasearch(self,tree):
        #alphabetasearch
        #Node = findNode(ergebnis)
       
        pass #return tree with updated values
    #TODO insert functions in class
    
    def best_node(self,tree):
        #nodes height 1 sammeln
        children = tree.root.children
        if children # falls Züge vorhanden
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
                        if possible_best_node[3] == best_nodes[0][3] # falls ein weiterer gleichwertiger Zug existiert
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
        generate_moves(b,self)

    def make_move(self,b_old,bb_from, bb_to):
        make_move(b_old,bb_from,bb_to)

player = Player()  




'''

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
        
'''
 
### DEMO ###

        
if __name__ == "__main__":
    
    b = init_game(give_bitboards(), player)
    
    tree = tree(BittoFEN(b))
    
    player.best_node(tree)