from lib2to3.pgen2.token import ISTERMINAL
import numpy as np
# requires: pip install anytree
from anytree import Node, RenderTree
import random
from bitboard import *
from tree import *
from movegen import *
import logging
import threading
import time
import concurrent.futures


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
        elif color_code=="win":
            print("Du hast gewonnen!")
        else:
            print("Du hast verloren!")
            #TODO remis implement

    def __get__(self):
        # extrahiert aktuellen Spieler als String
        if self.current == 1:
            return 'W'
        elif self.current == -1:
            return 'B'
        else:
            return 'error'
    def utility(self,b):
        return spielBewertung(b,self.current)

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
        children = np.asarray(tree.root.children,Node)
        #print(children)
        if len(children)>0: # falls Züge vorhanden
            values=[]
            for x in children:
                values.append(x.value)
            #values = [value for index,parent,b,value,h in children]
            #print(tree)
            #print(children)

            #return best node of nodes of tree height 1 
            best_nodes = []
            #print(children)
            while len(children)>0:
                possible_best_node = children[np.argmax(values)]
                children = np.delete(children,np.argmax(values))#bzw. values.remove(node.index)
                #print(children)
                for x in children:
                    values.append(x.value)  
                
                if best_nodes: # falls Liste schon Element enthält
                    if possible_best_node.value == best_nodes.value: # falls ein weiterer gleichwertiger Zug existiert
                        best_nodes.append(possible_best_node)
                    else: # falls nächstbester Zug schlechter
                        break # alle besten Züge gefunden
                else: # falls Liste noch leer
                    if checkmate(possible_best_node.b,(-1)**possible_best_node.h) == False: # erster Zug muss auf jeden Fall legal sein
                        best_nodes.append(possible_best_node)#  ,player)=(-1)^höhe
            # best_nodes sollte nun mindestens einen Zug enthalten. Dieser ist immer legal
            if len(best_nodes) == 1: # falls nur ein Zug vorhanden
                print("best0:",best_nodes[0])
                return best_nodes[0] # gib Zug zurück
            elif len(best_nodes)>1:
                while len(best_nodes)>0: # entferne Züge von Liste bis zufälliger legaler Zug gefunden
                    best_node = random.choice(best_nodes) # wähle zufällig besten Zug
                    if checkmate(best_node,(-1)**best_node.h) == False: # falls Zug legal
                        print("best:",best_node)
                        return best_node # gib Zug zurück
                    else:
                        best_nodes.remove(best_node) 
            print('kein guter Zug vorhanden!')
            children = np.asarray(tree.root.children,Node)
            print("doof: ",children[0])
            return children[0]
             
        else:
            print('kein Zug vorhanden!')
            print("else: ",children[0])
            return children[0]

        

    def generate_moves(self,b):
        return generate_moves(b,self)

    def make_move(self,b_old,bb_from, bb_to):
        return make_move(b_old,bb_from,bb_to)

    def set_movetree(self,tree,tmove, h=0,index=0,step=0):#added züge an node(index)
    #while (time-(tmax/2)>0):
    
        node=tree.find_node(index)
        #print("node:")
        #print(node)
        #while node.h==h:
        moves=self.generate_moves(node.b)#liste aller moves von bb
        #moves=[["a1a2",move(b)],["a2a4",b],...]
        #print("moves")
        for b in moves:
        #for b in range (len(moves)):
            if b:
            #if b[0] and b[1]:
                #name=b[0]
                #bb=b[1]
                #print("b:")
                #print(b)
                #tree.insert_node(node,[bb,self.utility(b),h,name])
                tree.insert_node(node,[b,self.utility(b),h])  #in Node mit bitboard und wertung einsetzen
                #TODO auch in insert node auskommentieren! (tree.py)
                # print("u:")
                # print(self.utility(b))
                #print(self.utility(b))
                #tree.print_tree()
            else:
                moves.remove(b)
        index +=1
        node=tree.find_node(index)
        
        step+=index
        
        #print("h:",h,"moves:",len(moves))
        h+=1
        
        return [tmove, len(moves),h]

    def tree_height(self,player,tree,tmove,index=0,altaltstep=0,altstep=1,h=0):
        #tmove=arr[4]
        #arr=[tree,h,index,step,tmove]
        #logging.info("Thread1    : started")
        #print(arr)
        # if h==0:
        #     arr=player.set_movetree(tree,tmove,h,index)#ein ausgerechneter zug alle züge ausrechnen
        #     print(arr)
        arr=[tmove,altstep]
        neustep=altstep
        altstep+=altaltstep
        for z in range(index, altstep):#eine weitere ebene durchgehen
            #print(arr[0])
            #logging.info("Main    : creating height "+str(h))
            arr=(self.set_movetree(tree,arr[0],h,z))
            neustep+=arr[1]
            #print("Tree "+str(z)+":")
            #tre.print_tree()
            arr[0]-=0.1
            if arr[0]<=0:
                return arr
        #print(arr[0])
        if arr[0]>=0:
            arr[0]-=0.5
            altstep-=altaltstep#-=alt
            return self.tree_height(player,tree,arr[0],index+altstep,altstep,neustep-altstep,h+1)
        return arr

    def turn(self, FEN,time=2):#ein kompletter zug der ki

        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                                        datefmt="%H:%M:%S")
        logging.info("Main    : start turn "+str(time))

        tmove=time/2
        tsearch=time/2
        bb=FENtoBit(FEN)
        #bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#testFEN
        tree=Tree(bb)#leerer baum mit b als root
        tmove=time/2
        if not checkmate(bb,self):#Spielende überprüfen
            #tre.print_tree()
            #arr=p.set_movetree(tre,tmove)
            #save=arr[0]
            save=tree
            #tree.print_tree()
            logging.info("Main    : building movetree "+str(time))
            arr=self.tree_height(self,tree,tmove)#time bzw. depth
            if arr:
                time-=(tmove-arr[0])
                save=arr
            logging.info("Main    : movetree finished with height:"+str(arr[2])+" "+str(time))
            
            
            #tree.print_tree()
            #print(tree)  
            #utility auf root?
            depth=1
            logging.info("Main    : doing minimax "+str(time))
            savetree=tree
            while(tsearch>=0 and depth<=arr[2]):#noch zeit und noch nicht so tief wie baumhöhe
                tree=savetree
                tiefe=self.alphabetasearch(tree.root,depth)#indizes aktualisieren#wertung des bestmöglichen zuges ausgeben
                children = np.asarray(tree.root.children,Node)
                print("search:",depth,children[0])
                depth+=1
                tsearch-=0.1
                time-=0.1
            logging.info("Main    : minimax finished with depth:"+str(depth-1)+" "+str(time))
            logging.info("Main    : choosing good move "+str(time))

            node=self.best_node(tree)#besten zug auswaehlen
            #move=tree.find_node(node.index)
            logging.info("Main    : finished turn "+str(time))
            FEN=BittoFEN(node.b,self.current)
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
    else:
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
        


"""
class ThreadWithReturnValue(threading):#https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None
    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
    def join(self):
        threading.join(self)
        return self._return
"""


### DEMO ###




#Test tree.py
"""
time=10
tmove=time/2
p=Player()    
bb=init_game(p)
bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#TODO fix fen->bit
tre=Tree(bb)
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
#tre.print_tree()
#arr=p.set_movetree(tre,tmove)
#save=arr[0]
save=tre
tre.print_tree()
arr=tree_height(p,tre,tmove)
if arr:
    save=arr
tre.print_tree()
print(tre)  
"""  
# while(arr[4]>=0):#solange zeit ist
#     print(arr[4])
#     arr=tree_height(arr)
#     # logging.info("Main    : before creating thread")
#     # e= concurrent.futures.ThreadPoolExecutor()
#     # logging.info("Main    : thread created")
#     # future = e.submit(tree_height, arr)
#     # return_value = future.result()
#     # save=return_value
#     # logging.info("Main    : waiting for thread")
#     # save=concurrent.futures.wait(e)
#     # logging.info("Main    : thread finished")
#     # logging.info("Main    : wait for the thread to finish")

#     logging.info("Main    : before creating thread")
#     x = threading.Thread(target=tree_height, args=arr)
#     logging.info("Main    : thread created")

#     logging.info("Main    : before running thread")
#     x.start()
#     logging.info("Main    : wait for the thread to finish")
#     x.join()
    
# logging.info("Main    : all done")
#return save

#return tre


#if __name__ == "__main__":


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
## DEMO ##
#kompletten zug ausführen
p=Player()
FEN=p.turn("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w",10)
print(FEN)
print_board(FENtoBit(FEN))