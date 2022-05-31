from lib2to3.pgen2.token import ISTERMINAL
from tkinter.font import families
import numpy as np
# requires: pip install anytree
from anytree import Node, RenderTree
import random

from sqlalchemy import values
from bitboard import *
from tree import *
from movegen import *
import logging
import threading
import time
import concurrent.futures

def timer(function):
    start_time = time.time()
    function()
    elapsed=time.time() - start_time
    print("--- %s seconds ---" % (elapsed))
    return elapsed

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
        if color_code == 'W' or color_code==1:
            self.current = 1
        elif color_code == 'B'or color_code==-1:
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
        #print(tree.root.children)
        children = list(tree.root.children)
        #print(children)
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
                children.pop(np.argmax(values))#bzw. values.remove(node.index)
                #print(children)
                values=[]
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
            children = list(tree.root.children)
            #print("doof: ",children[0])
            node=random.choice(children)
            return node
             
        else:
            print('kein Zug vorhanden!')
            print("else: ",children[0])
            return children[0]

        

    def generate_moves(self,b):
        return generate_moves(b,self)

    def make_move(self,b_old,bb_from, bb_to):
        return make_move(b_old,bb_from,bb_to)

    def set_movetree(self,tree,h=0,index=0,step=0):#added züge an node(index)
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
                print("leerer move")
                moves.remove(b)
        #index +=1
        #node=tree.find_node(index)
        
        #step+=index
        #h+=1
        #print("h:",h,"moves:",len(moves))
        
        
        return [len(moves),h]
    def set_test_movetree(self,tree,h=0,index=0,step=0):#added züge an node(index) mit nodes.value=None
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
                tree.insert_node(node,[b,None,h+1])
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
        h+=1
        #print("h:",h,"moves:",len(moves))
        
        
        return [len(moves),h]#h nötig?

    def c_tree_height(self,tree,depth,value=False,index=0,altaltstep=0,altstep=1,h=1):#tree ebenen erstellen bis tiefe d
            #tmove=arr[4]
            #arr=[tree,h,index,step,tmove]
            #logging.info("Thread1    : started")
            #print(arr)
            # if h==0:
            #     arr=player.set_movetree(tree,tmove,h,index)#ein ausgerechneter zug alle züge ausrechnen
            #     print(arr)
            arr=[altstep,depth]#auskommentieren?
            neustep=altstep
            altstep+=altaltstep
            for z in range(index, altstep):#eine weitere ebene durchgehen
                #print(arr[0])
                #logging.info("Main    : creating height "+str(h))
                if value:
                    arr=(self.set_movetree(tree,h,z))#setze alle moves unter parent index=z
                else:
                    arr=(self.set_test_movetree(tree,h,z))
                neustep+=arr[0]
                #print("Tree "+str(z)+":")
                #tre.print_tree()
            #print(arr[0])
            if arr[1]<=depth:
                altstep-=altaltstep#-=alt
                return self.d_tree_height(tree,depth,value,index+altstep,altstep,neustep-altstep,h+1)
            return arr
    def d_tree_height(self,tree,depth,value=False,index=0,altstep=1,h=0):#tree ebenen erstellen bis tiefe d
                #tmove=arr[4]
            #arr=[tree,h,index,step,tmove]
            #logging.info("Thread1    : started")
            #print(arr)
            # if h==0:
            #     arr=player.set_movetree(tree,tmove,h,index)#ein ausgerechneter zug alle züge ausrechnen
            #     print(arr)
            arr=[altstep,depth]#auskommentieren?
            altstep=len(tree.nodes)
            for z in range(index, altstep):#eine weitere ebene durchgehen
                #print(arr[0])
                #logging.info("Main    : creating height "+str(h))
                if value:
                    arr=(self.set_movetree(tree,h+1,z))
                else:
                    arr=(self.set_test_movetree(tree,h+1,z))
                #neustep+=arr[0]
                #print("Tree "+str(z)+":")
                #tre.print_tree()
                #print(arr[0])
            depth-=1
            if depth>0:
                index =altstep
                #altstep-=altaltstep#-=alt
                self.__switch__()#neue ebene für gegner
                return self.d_tree_height(tree,depth,value,index,altstep,h+1)
            return arr


    def tree_height(self,tree,tmove,index=0,altstep=1,h=0):#tree ebenen erstellen bis time t=0
        #tmove=arr[4]
        #arr=[tree,h,index,step,tmove]
        #logging.info("Thread1    : started")
        #print(arr)
        # if h==0:
        #     arr=player.set_movetree(tree,tmove,h,index)#ein ausgerechneter zug alle züge ausrechnen
        #     print(arr)
        start=time.time()
        arr=[tmove,altstep]
        altstep=len(tree.nodes)
        for z in range(index, altstep):#eine weitere ebene durchgehen
            #print(arr[0])
            #logging.info("Main    : creating height "+str(h))
            arr=(self.set_movetree(tree,h+1,z))
            #neustep+=arr[0]
            #print("Tree "+str(z)+":")
            #tre.print_tree()
            if start+tmove<=time.time():#zeitlimit überschritten
                print("ebene" +(h+1)+" not finished")
                arr[1]-=1#letzte ebene nicht fertig geworden
                return arr
        #print(arr[0])
        if tmove>=time.time()-start:
            index=altstep
            self.__switch__()#neue ebene für gegner
            return self.tree_height(tree,tmove,index,altstep,h+1)
        print("finish")
        return arr

    def turn(self, FEN,t=20):#ein kompletter zug der ki
        #print(FEN)
        start=time.time()
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                                        datefmt="%H:%M:%S")
        logging.info("Main    : start turn "+str(start-start))
        tmove=(t/10)*9#seconds
        tsearch=t/10
        [bb,play]=FENtoBit(FEN,True)
        if self.current==play:#spieler am zug

            #bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#testFEN
            tree=Tree(bb)#leerer baum mit b als root
            if not checkmate(bb,self):#Spielende überprüfen
                #tre.print_tree()
                #arr=p.set_movetree(tre,tmove)
                #tree.print_tree()
                logging.info("Main    : building movetree "+str(time.time()-start))
                arr=self.tree_height(tree,(start+tmove-time.time()))#time bzw. depth
                #arr[1]=tree.h
                self.current=play
                tleft=time.time()-start
                logging.info("Main    : movetree finished with height: "+str(arr[1])+" "+str(tleft))
                logging.info("Main    : tree build finished in:"+str(time.time()-start)+"s")
                
                
                #tree.print_tree()
                #print(tree)  
                #utility auf root?
                depth=1
                logging.info("Main    : doing minimax "+str(tleft))
                savetree=tree
                sstart=time.time()
                while(time.time()-start+tsearch>=0 and depth<=arr[1]):#noch zeit und noch nicht so tief wie baumhöhe
                    tree=savetree
                    tiefe=self.alphabetasearch(tree.root,depth)#indizes aktualisieren#wertung des bestmöglichen zuges ausgeben
                    #children = np.asarray(tree.root.children,Node)
                    #print("search:",depth,children[0])
                    depth+=1
                #tree.print_node(tree.nodes[2])#teste tree nach search
                tleft=time.time()-start
                logging.info("Main    : minimax finished with depth: "+str(depth-1)+" in "+str(time.time()-sstart)+"s")
                logging.info("Main    : choosing good move "+str(tleft))
                node=self.best_node(tree)#besten zug auswaehlen
                #move=tree.find_node(node.index)
                #logging.info("Main    : finished turn "+str(start+t))
                finish=time.time()
                self.__switch__()
                FEN=BittoFEN(node.b,self.current)
                self.__switch__()
                logging.info("Main    : finished turn in "+str(finish-start)+"s")
                logging.info("Main    : time remaining: "+str(start+t-time.time()))
        else:#Spieler nicht dran
                FEN=False
            #self.__switch__()#Spieler wechseln (egal ob zug gemacht odeer nicht
        return FEN
            
    def teste(self,FEN,value=0,search=False,zug=False,utility=False,tree=False,tiefe=False,turn=False,baum=False):
        # value depends on what you want to do:
        # eingabe -> prozess: datatype(value) -> return
        # zug-> player.turn(): int(time) -> str(FEN)
        # search -> alphabetasearch zeit messen für tiefe: int(tiefe) -> int(time)
        # zug -> zuggenerator: int(wdh.) -> int(time)
        # utility (einzeln) -> utility: int(wdh) -> int(time)
        #         sonst -> Funktion ohne utility ausführen: -
        # tree -> baumspeichern: tiefe or time
        # tiefe -> baumspeichern bis tiefe value: int(tiefe) -> int(time)
        # not tiefe -> baumspeichern bis time=0: int(time) -> int(tiefe)
        # baum -> baum printen: int(time) -> print

        if search:#alphabetasearch zeit messen für tiefe
            turn=False
        elif zug:#zuggenerator only
            zeit=time.time()
            for i in range (value):
                moves=self.generate_moves(FENtoBit(FEN))
            zeit=(time.time()-zeit)/value
            
            #print(moves)
            return zeit
        elif utility and not tree:#utility only
            tree=Tree(FENtoBit(FEN))
            arr=self.d_tree_height(tree,3)
            dep=len(tree.nodes)
            print("baum fertig")
            zeit=time.time()
            for i in tree.nodes:
                i.value=self.utility(i.b)
            zeit=(time.time()-zeit)
            print(dep)
            print(zeit/dep)
            #print(wert)
            return zeit

        elif tree:#baumseichern
            bb=FENtoBit(FEN)
            t=Tree(bb)
            if tiefe:#baumspeicher bis tiefe mit/ohne utility
                depth=value
                zeit=time.time()
                arr=self.d_tree_height(t,depth,utility)#timer einbauen
                #t.print_tree()
                return time.time()-zeit
            else:#baumspeichern bis time mit utility (Standard)
                zeit=value
                self.tree_height(t,zeit)
                return t.nodes[len(t.nodes)-1].h
        if search:#alphabetasearch zeit messen für tiefe
            #if value>=0:
            zeit=time.time()
            tree=Tree(FENtoBit(FEN))
            arr=self.d_tree_height(tree,2)
            dep=len(tree.nodes)
            zeit=time.time()-zeit
            print("baum fertig"+str(zeit))
            zeit=time.time()
            for i in tree.nodes:
                i.value=self.utility(i.b)
            zeit=time.time()-zeit
            print("utility fertig"+str(zeit))
            searchtime=time.time()
            tiefe=value
            #while(depth<=arr[1] and tiefe>=depth):#noch zeit und noch nicht so tief wie baumhöhe
            self.alphabetasearch(tree.root,tiefe)#indizes aktualisieren#wertung des bestmöglichen zuges ausgeben
            #children = list(tree.root.children)
            #print("search:",depth,children[0].value)
            return time.time()-searchtime
        elif turn:#normaler zug #und alphabetasearch bis zeit um
            FEN=self.turn(FEN,value)
            print(FEN)
            return(FEN)
            # print_board(FENtoBit(FEN))
        elif baum:#baum ergebnis printen # teste tree.py
            zeit=value#eher durchgänge
            tmove=zeit/2 
            #bb=init_game(p)
            #bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#TODO fix fen->bit
            bb=FENtoBit(FEN)
            tre=Tree(bb)
            # format = "%(asctime)s: %(message)s"
            # logging.basicConfig(format=format, level=logging.INFO,
            #                             datefmt="%H:%M:%S")
            #tre.print_tree()
            #arr=p.set_movetree(tre,tmove)
            #save=arr[0]
            tre.print_tree()
            arr=self.tree_height(tre,tmove)
            tre.print_tree()
            #print(tre)
            # for x in tre.nodes:
            #     if x.h==4:
            #         tre.print_node(x)  
            #         break



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


### Beispiele Threading (parallelisierung) ###
#potenziell für baum erstellen auf 4 prozessoren kerne aufteilen




  
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


if __name__ == "__main__":

    ## DEMO ## TODO andere Demos auf aktualität überprüfen ung ggf. removen
    #                   ich brauch davon nichts mehr

    #inputs:#

    p=Player()
    #FEN="r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR W"
    #FEN="rnb1kbnr/p4ppp/1p1pp3/2p3q1/3P4/NQP1PNPB/PP3P1P/R1B1K2R w"
    #FEN="3q3r/1pp2pb1/3pkn2/1B6/3P4/4PN1P/5K1P/7R b"
    #FEN="rnbqkbnr/pp1p1ppp/4p3/1Pp5/8/2N5/P1PPPPPP/R1BQKBNR w"
    FEN="8/4k3/8/8/8/8/3K4/8"

    zeit=10
    depth=4
    wdh=1000

    ### Unit/Benchmark Tests ###


    #p.teste(FEN,zeit,turn=True)#turn ausführen
    #searchtime=p.teste(FEN,depth,search=True)#alphabetasearch zeit messen für tiefe
    #t=p.teste(FEN,wdh,zug=True)#zuggenerator only 1000 mal durchschnitt
    #t=p.teste(FEN,wdh,utility=True)#utility only
    #t=p.teste(FEN,depth,tree=True,tiefe=True)#baumspeicher bis tiefe ohne utility
    t=p.teste(FEN,depth,tree=True,tiefe=True,utility=True)#baumspeicher bis tiefe mit utility
    #tiefe=p.teste(FEN,zeit,tree=True)#baumspeichern bis time mit utility (Standard)
    #p.teste(FEN,zeit,baum=True)#baum ergebnis printen

    #print(searchtime)