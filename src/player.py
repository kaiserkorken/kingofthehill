import numpy as np
# requires: pip install anytree
import random

#from movegen import *
from movegen_verbose import generate_moves_verbose
from bitboard import *
from tree import *

import logging
import time
from tt import ttable
from tree_search import *


def timer(function):
    start_time = time.time()
    function()
    elapsed = time.time() - start_time
    print("--- %s seconds ---" % (elapsed))
    return elapsed


# Player-Klasse. Macht eigentlich noch nix außer klartextübersetzung 1->W, -1->B, kann auch ersetzt werden.
class Player():
    def __init__(self):
        # weiß beginnt
        self.current = 1

        #### das auskommentieren kostet 8 GB Speicherplatz!!! ####
        # self.tt=ttable("testtable.mymemmap",32)

    def __switch__(self):
        # wechselt die Spieler ab
        self.current *= -1

    def __set__(self, color_code):
        # setzt aktuellen Spieler -> vielleicht für funktion a la: bit, player = FENtoBit(FEN)
        if color_code == 'W' or color_code == 1:
            self.current = 1
        elif color_code == 'B' or color_code == -1:
            self.current = -1
        elif color_code == "win":
            print("Du hast gewonnen!")
        else:
            print("Du hast verloren!")
            # TODO remis implement

    def __get__(self):
        # extrahiert aktuellen Spieler als String
        if self.current == 1:
            return 'W'
        elif self.current == -1:
            return 'B'
        else:
            return 'error'

    def utility(self, b):
        return spielBewertung(b, self.current)

    def alphabetasearch(self, node, depth=0, ismax=True):
        if depth == 0 or node.children == None:
            return node.value
        if ismax:
            v = 1000000
            for x in node.children:
                v = max(v, self.alphabetasearch(x, depth - 1, False))
                node.value = v
            return v
        else:
            v = -1000000
            for x in node.children:
                v = min(v, self.alphabetasearch(x, depth - 1, True))
                node.value = v
            return v

        # alphabetasearch
        # Node = findNode(ergebnis)
        # return tree with updated values

    # TODO insert functions in class



    def generate_moves(self, b):
        return generate_moves(b, self)

    def make_move(self, b_old, bb_from, bb_to):
        return make_move(b_old, bb_from, bb_to)

    def set_movetree(self, tree, h=0, index=0, step=0):  # added züge an node(index)
        # while (time-(tmax/2)>0):

        node = tree.find_node(index)
        # print("node:")
        # print(node)
        # while node.h==h:
        # moves=self.generate_moves(node.b)#liste aller moves von bb
        moves, names = generate_moves_verbose(node.b, self)  # generiere alle Züge aus Position b
        # moves=[["a1a2",move(b)],["a2a4",b],...]
        # print("moves")
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for b in range(len(moves)):
            # for b in range (len(moves)):
            if moves[b]:
                # if b[0] and b[1]:
                ### Test der names aus movegen verbose ###
                x = -1
                for z in range(len(alphabet)):
                    if alphabet[z] == names[b][4].lower():
                        x = z
                        break
                if x == -1:
                    print(names[b], "has wrong syntax")
                    print(names[b][4], "is not an column index")
                    break
                ### Test ende ###

                # name=b[0]
                # bb=b[1]
                # print("b:")
                # print(b)
                # tree.insert_node(node,[bb,self.utility(b),h,name])
                tree.insert_node(node, moves[b], self.utility(moves[b]), h,
                                 names[b])  # in Node mit bitboard und wertung einsetzen

                # auch in insert node auskommentieren! (tree.py)
                # print("u:")
                # print(self.utility(b))
                # print(self.utility(b))
                # tree.print_tree()
            else:
                print("leerer move")
                moves.remove(moves[b])
        # index +=1
        # node=tree.find_node(index)

        # step+=index
        # h+=1
        # print("h:",h,"moves:",len(moves))

        return [len(moves), h]

    def set_tt_movetree(self, tree, h=0, index=0, step=0):  # added züge an node(index)
        # while (time-(tmax/2)>0):

        node = tree.find_node(index)  # parent
        # print("node:")
        # print(node)
        # while node.h==h:
        moves, names = generate_moves_verbose(node.b, self)  # generiere alle Züge aus Position b
        # moves=self.generate_moves(node.b)#liste aller moves von bb
        # moves=[["a1a2",move(b)],["a2a4",b],...]
        # print("moves")
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for b in range(len(moves)):
            # for b in range (len(moves)):
            if moves[b]:
                # if b[0] and b[1]:
                x = -1
                for z in range(len(alphabet)):
                    if alphabet[z] == names[b][4].lower():
                        x = z
                        break
                if x == -1:
                    pass
                    # print(names[b], "has wrong syntax")
                    # print(names[b][4],"is not an column index")
                else:
                    # name=b[0]
                    # bb=b[1]
                    # print("b:")
                    # print(b)
                    # tree.insert_node(node,[bb,self.utility(b),h,name])
                    y = int(names[b][5]) - 1
                    # x=np.where(alphabet==names[b][4])#a->1
                    token = names[b][0]
                    hash = self.tt.hash_value(node.hash, x, y, token)
                    util = self.tt.in_table(hash, h + 1)
                    if len(util) != 2:
                        # print(hash)
                        util = self.utility(moves[b])
                        self.tt.to_table(hash, util, h + 1)
                        tree.insert_node(node, moves[b], util, h + 1, names[b], hash)
                    else:
                        tree.insert_node(node, moves[b], util[0], h + 1, names[b],
                                         hash)  # in Node mit bitboard und wertung einsetzen

                    # TODO auch in insert node auskommentieren! (tree.py)
                    # print("u:")
                    # print(self.utility(b))
                    # print(self.utility(b))
                    # tree.print_tree()
            else:
                print("leerer move")
                moves.remove(moves[b])
        # index +=1
        # node=tree.find_node(index)

        # step+=index
        # h+=1
        # print("h:",h,"moves:",len(moves))

        return [len(moves), h]

    def set_test_movetree(self, tree, h=0, index=0, step=0):  # added züge an node(index) mit nodes.value=None
        # while (time-(tmax/2)>0):

        node = tree.find_node(index)
        # print("node:")
        # print(node)
        # while node.h==h:
        moves = self.generate_moves(node.b)  # liste aller moves von bb
        # moves=[["a1a2",move(b)],["a2a4",b],...]
        # print("moves")
        for b in moves:
            # for b in range (len(moves)):
            if b:
                # if b[0] and b[1]:
                # name=b[0]
                # bb=b[1]
                # print("b:")
                # print(b)
                # tree.insert_node(node,[bb,self.utility(b),h,name])
                tree.insert_node(node, [b, None, h + 1])
                # TODO auch in insert node auskommentieren! (tree.py)
                # print("u:")
                # print(self.utility(b))
                # print(self.utility(b))
                # tree.print_tree()
            else:
                moves.remove(b)
        index += 1
        node = tree.find_node(index)

        step += index
        h += 1
        # print("h:",h,"moves:",len(moves))

        return [len(moves), h]  # h nötig?

    def tree_tt_height(self, tree, tmove, index=0, altstep=1, h=0):  # tree ebenen erstellen bis tiefe d
        # tmove=arr[4]
        # arr=[tree,h,index,step,tmove]
        # logging.info("Thread1    : started")
        # print(arr)
        # if h==0:
        #     arr=player.set_movetree(tree,tmove,h,index)#ein ausgerechneter zug alle züge ausrechnen
        #     print(arr)
        start = time.time()
        arr = [tmove, altstep]
        altstep = len(tree.nodes)
        for z in range(index, altstep):  # eine weitere ebene durchgehen
            # print(arr[0])
            # logging.info("Main    : creating height "+str(h))
            arr = (self.set_tt_movetree(tree, h + 1, z))
            # neustep+=arr[0]
            # print("Tree "+str(z)+":")
            # tre.print_tree()
            if start + tmove <= time.time():  # zeitlimit überschritten
                print("finished till ebene: " + str((h + 1)))
                arr[1] -= 1  # letzte ebene nicht fertig geworden
                return arr
        # print(arr[0])
        if tmove >= time.time() - start:
            index = altstep
            self.__switch__()  # neue ebene für gegner
            return self.tree_tt_height(tree, tmove, index, altstep, h + 1)
        print("finish")
        return arr

    def d_tree_height(self, tree, depth, value=False, index=0, altstep=1, h=0):  # tree ebenen erstellen bis tiefe d
        # tmove=arr[4]
        # arr=[tree,h,index,step,tmove]
        # logging.info("Thread1    : started")
        # print(arr)
        # if h==0:
        #     arr=player.set_movetree(tree,tmove,h,index)#ein ausgerechneter zug alle züge ausrechnen
        #     print(arr)
        arr = [altstep, depth]  # auskommentieren?
        altstep = len(tree.nodes)
        for z in range(index, altstep):  # eine weitere ebene durchgehen
            # print(arr[0])
            # logging.info("Main    : creating height "+str(h))
            if value:
                arr = (self.set_movetree(tree, h + 1, z))
            else:
                arr = (self.set_test_movetree(tree, h + 1, z))
            # neustep+=arr[0]
            # print("Tree "+str(z)+":")
            # tre.print_tree()
            # print(arr[0])
        depth -= 1
        if depth > 0:
            index = altstep
            # altstep-=altaltstep#-=alt
            self.__switch__()  # neue ebene für gegner
            return self.d_tree_height(tree, depth, value, index, altstep, h + 1)
        return arr

    def tree_height(self, tree, tmove, index=0, altstep=1, h=0):  # tree ebenen erstellen bis time t=0
        # tmove=arr[4]
        # arr=[tree,h,index,step,tmove]
        # logging.info("Thread1    : started")
        # print(arr)
        # if h==0:
        #     arr=player.set_movetree(tree,tmove,h,index)#ein ausgerechneter zug alle züge ausrechnen
        #     print(arr)
        start = time.time()
        arr = [tmove, altstep]
        altstep = len(tree.nodes)
        for z in range(index, altstep):  # eine weitere ebene durchgehen
            # print(arr[0])
            # logging.info("Main    : creating height "+str(h))
            arr = (self.set_movetree(tree, h + 1, z))
            # neustep+=arr[0]
            # print("Tree "+str(z)+":")
            # tre.print_tree()
            if start + tmove <= time.time():  # zeitlimit überschritten
                print("finished till ebene: " + str((h + 1)))
                arr[1] -= 1  # letzte ebene nicht fertig geworden
                return arr
        # print(arr[0])
        if tmove >= time.time() - start:
            index = altstep
            self.__switch__()  # neue ebene für gegner
            return self.tree_height(tree, tmove, index, altstep, h + 1)
        print("finish")
        return arr
    
    def turn(self, FEN, t=20):  # ein kompletter zug der ki
        # print(FEN)
        start = time.time()
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.info("Main    : start turn " + str(start - start))
        tmove = (t / 10) * 9  # seconds
        tsearch = t / 10
        [bb, play] = FENtoBit(FEN, True)
        # tt=ttable("testtable.mymemmap",32)#erstellen falls noetig, sonst in build tree
        if self.current == play and FENtoBit(FEN,True) != False:  # spieler am zug

            # bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#testFEN
            tree = Tree(bb)  # ,self.tt.starthash)#leerer baum mit b als root
            if not checkmate(bb, self):  # Spielende überprüfen
                # tre.print_tree()
                # arr=p.set_movetree(tre,tmove)
                # tree.print_tree()
                logging.info("Main    : building movetree " + str(time.time() - start))
                arr = self.tree_height(tree, (start + tmove - time.time()))  # time bzw. depth
                # arr[1]=tree.h
                self.current = play
                tleft = time.time() - start
                logging.info("Main    : movetree finished with height: " + str(arr[1]) + " " + str(tleft))
                logging.info("Main    : tree build finished in:" + str(time.time() - start) + "s")

                # tree.print_tree()
                # print(tree)  
                # utility auf root?
                depth = 1
                logging.info("Main    : doing minimax " + str(tleft))
                savetree = tree
                #savetree.sort_nodes() FEhler bei invertet=True
                sstart = time.time()
                best_val = search(tree.root, self.current, arr[1], tsearch)
                # tree.print_node(tree.nodes[2])#teste tree nach search
                tleft = time.time() - start
                logging.info("Main    : minimax finished with depth: " + str(depth - 1) + " in " + str(
                    time.time() - sstart) + "s")
                logging.info("Main    : choosing good move " + str(tleft))
                node = best_node(tree)  # besten zug auswaehlen
                # move=tree.find_node(node.index)
                # logging.info("Main    : finished turn "+str(start+t))
                finish = time.time()
                self.__switch__()
                FEN = BittoFEN(node.b, self.current)
                self.__switch__()
                logging.info("Main    : finished turn in " + str(finish - start) + "s")
                logging.info("Main    : time remaining: " + str(start + t - time.time()))
        else:  # Spieler nicht dran
            FEN = False
        # self.__switch__()#Spieler wechseln (egal ob zug gemacht odeer nicht
        return FEN

    def turn_bak(self, FEN, t=20):  # ein kompletter zug der ki
        # print(FEN)
        start = time.time()
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.info("Main    : start turn " + str(start - start))
        tmove = (t / 10) * 9  # seconds
        tsearch = t / 10
        [bb, play] = FENtoBit(FEN, True)
        # tt=ttable("testtable.mymemmap",32)#erstellen falls noetig, sonst in build tree
        if self.current == play and FENtoBit(FEN,True) != False:  # spieler am zug

            # bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#testFEN
            tree = Tree(bb)  # ,self.tt.starthash)#leerer baum mit b als root
            if not checkmate(bb, self):  # Spielende überprüfen
                # tre.print_tree()
                # arr=p.set_movetree(tre,tmove)
                # tree.print_tree()
                logging.info("Main    : building movetree " + str(time.time() - start))
                arr = self.tree_height(tree, (start + tmove - time.time()))  # time bzw. depth
                # arr[1]=tree.h
                self.current = play
                tleft = time.time() - start
                logging.info("Main    : movetree finished with height: " + str(arr[1]) + " " + str(tleft))
                logging.info("Main    : tree build finished in:" + str(time.time() - start) + "s")

                # tree.print_tree()
                # print(tree)  
                # utility auf root?
                depth = 1
                logging.info("Main    : doing minimax " + str(tleft))
                savetree = tree
                #savetree.sort_nodes() FEhler bei invertet=True
                sstart = time.time()
                while (time.time() - start + tsearch >= 0 and depth <= arr[1]):  # noch zeit und noch nicht so tief wie baumhöhe
                    tree = savetree
                    tiefe = self.alphabetasearch(tree.root,
                                                 depth)  # indizes aktualisieren#wertung des bestmöglichen zuges ausgeben
                    # children = np.asarray(tree.root.children,Node)
                    # print("search:",depth,children[0])
                    depth += 1
                # tree.print_node(tree.nodes[2])#teste tree nach search
                tleft = time.time() - start
                logging.info("Main    : minimax finished with depth: " + str(depth - 1) + " in " + str(
                    time.time() - sstart) + "s")
                logging.info("Main    : choosing good move " + str(tleft))
                node = best_node(tree)  # besten zug auswaehlen
                # move=tree.find_node(node.index)
                # logging.info("Main    : finished turn "+str(start+t))
                finish = time.time()
                self.__switch__()
                FEN = BittoFEN(node.b, self.current)
                self.__switch__()
                logging.info("Main    : finished turn in " + str(finish - start) + "s")
                logging.info("Main    : time remaining: " + str(start + t - time.time()))
        else:  # Spieler nicht dran
            FEN = False
        # self.__switch__()#Spieler wechseln (egal ob zug gemacht odeer nicht
        return FEN

    def teste(self, FEN, value=0, search=False, zug=False, utility=False, tree=False, tiefe=False, turn=False,
              baum=False, tt=False):
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

        if search:  # alphabetasearch zeit messen für tiefe
            turn = False
        elif zug:  # zuggenerator only
            zeit = time.time()
            for i in range(value):
                moves = self.generate_moves(FENtoBit(FEN))
            zeit = (time.time() - zeit) / value

            # print(moves)
            return zeit
        elif utility and not tree:  # utility only
            tree = Tree(FENtoBit(FEN))
            arr = self.d_tree_height(tree, 3)
            dep = len(tree.nodes)
            print("baum fertig")
            zeit = time.time()
            for i in tree.nodes:
                i.value = self.utility(i.b)
            zeit = (time.time() - zeit)
            print(dep)
            print(zeit / dep)
            # print(wert)
            return zeit

        elif tree:  # baumseichern
            bb = FENtoBit(FEN)
            t = Tree(bb)
            if tiefe:  # baumspeicher bis tiefe mit/ohne utility
                depth = value
                zeit = time.time()
                arr = self.d_tree_height(t, depth, utility)  # timer einbauen
                # t.print_tree()
                return time.time() - zeit
            else:  # baumspeichern bis time mit utility (Standard)
                zeit = value
                self.tree_height(t, zeit)
                t.print_node(t.nodes[len(t.nodes) - 1])
                print(len(t.nodes))
                return t.nodes[len(t.nodes) - 1].h
        if search:  # alphabetasearch zeit messen für tiefe
            # if value>=0:
            zeit = time.time()
            tree = Tree(FENtoBit(FEN))
            arr = self.d_tree_height(tree, 2)
            dep = len(tree.nodes)
            zeit = time.time() - zeit
            print("baum fertig" + str(zeit))
            zeit = time.time()
            for i in tree.nodes:
                i.value = self.utility(i.b)
            zeit = time.time() - zeit
            print("utility fertig" + str(zeit))
            searchtime = time.time()
            tiefe = value
            # while(depth<=arr[1] and tiefe>=depth):#noch zeit und noch nicht so tief wie baumhöhe
            self.alphabetasearch(tree.root, tiefe)  # indizes aktualisieren#wertung des bestmöglichen zuges ausgeben
            # children = list(tree.root.children)
            # print("search:",depth,children[0].value)
            return time.time() - searchtime
        elif turn:  # normaler zug #und alphabetasearch bis zeit um
            FEN = self.turn(FEN, value)
            print(FEN)
            return (FEN)
            # print_board(FENtoBit(FEN))
        elif baum:  # baum ergebnis printen # teste tree.py
            bb = FENtoBit(FEN)
            if tt:
                self.tt = ttable("testtable", dict=True)
                tre = Tree(bb, self.tt.starthash)
            else:
                tre = Tree(bb)
            zeit = value  # eher durchgänge
            tmove = zeit  # /2 
            # bb=init_game()
            # bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#TODO fix fen->bit

            # format = "%(asctime)s: %(message)s"
            # logging.basicConfig(format=format, level=logging.INFO,
            #                             datefmt="%H:%M:%S")
            # tre.print_tree()
            # arr=p.set_movetree(tre,tmove)
            # save=arr[0]
            tre.print_tree()
            if tt:
                arr = self.tree_tt_height(tre, tmove)
            else:
                arr = self.tree_height(tre, tmove)
                # tre.print_tree()
                tre.print_node(tre.nodes[len(tre.nodes) - 1])
            print(len(tre.nodes))
            # print(tre)
            # for x in tre.nodes:
            #     if x.h==4:
            #         tre.print_node(x)  
            #         break
            # Ke3-e4 -24 4
            # ├── kf4-d3 24 5
            # ├── kf4-e3 24 5
            # ├── kf4-f3 24 5
            # ├── kf4-d4 24 5
            # ├── kf4-d5 0 5
            # ├── kf4-e5 0 5
            # └── kf4-f5 24 5


def checkmate(bitboard,player):
    counter = 0
    sss = FENtoBit(BoardtoFEN(bitboard))
    mitte = False
    for countA, value in enumerate(sss['k']):
        for countB, info in enumerate(value):
            if info == True:
                counter = counter+1
                if countA==3 and countB ==3 or countA==3 and countB ==4 or countA==4 and countB ==3 or countA==4 and countB ==4:
                    mitte = True
            else:
                pass
    if counter < 2 or mitte == True:
        return True
    else:
        return mitte


# erstellt ein array mit String values der position der Weißen oder Schwarzen Figuren
def playerWert(bitbrd, player):
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
                wert = wert + 9
            elif int(x.split(";")[0]) == 0 and player == -1:
                wert = wert + 9
            elif int(x.split(";")[0]) != 0:
                wert = wert + 1

    for x in listeS:
        if bitbrd['k'][int(x.split(";")[0])][int(x.split(";")[1])] == True:
            wert = wert + 1
            if int(x.split(";")[0]) == 3 and int(x.split(";")[1]) == 3:
                wert = 100
            if int(x.split(";")[0]) == 3 and int(x.split(";")[1]) == 4:
                wert = 100
            if int(x.split(";")[0]) == 4 and int(x.split(";")[1]) == 3:
                wert = 100
            if int(x.split(";")[0]) == 4 and int(x.split(";")[1]) == 4:
                wert = 100

    return wert


def doubledPawns(board, color):
    color = color[0]
    # Get indices of pawns:
    listofpawns = lookfor(board, color + 'p')
    # Count the number of doubled pawns by counting occurences of
    # repeats in their x-coordinates:
    repeats = 0
    temp = []
    for pawnpos in listofpawns:
        if pawnpos[0] in temp:
            repeats = repeats + 1
        else:
            temp.append(pawnpos[0])
    return repeats


def lookfor(board, piece):
    listofLocations = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == piece:
                x = col
                y = row
                listofLocations.append((x, y))
    return listofLocations


testBoard = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["--", "bp", "--", "--", "bp", "bp", "bp", "bp"],
    ["--", "bp", "--", "--", "bp", "--", "bp", "--"],
    ["--", "bp", "--", "--", "--", "--", "--", "--"],
    ["--", "wp", "--", "--", "--", "--", "wp", "--"],
    ["--", "--", "--", "bp", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "--", "--", "--"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

# print(doubledPawns(testBoard,"b"))

testBoardB = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["bp", "bp", "--", "--", "bp", "--", "bp", "--"],
    ["--", "bp", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "wp", "--", "--", "--", "--"],
    ["--", "--", "--", "wp", "--", "--", "bN", "--"],
    ["wp", "wp", "--", "wp", "--", "wp", "wp", "wp"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


def blockedPawns(board, color):
    color = color[0]
    listofpawns = lookfor(board, color + 'p')
    blocked = 0
    # Self explanatory:
    for pawnpos in listofpawns:
        if ((color == 'w' and isOccupiedby(board, pawnpos[0], pawnpos[1] - 1,
                                           'black'))
                or (color == 'b' and isOccupiedby(board, pawnpos[0], pawnpos[1] + 1,
                                                  'white'))):
            blocked = blocked + 1
    return blocked


def isOccupiedby(board, x, y, color):
    if board[int(y)][int(x)] == '--':
        # the square has nothing on it.
        return False
    if board[int(y)][int(x)][0] == color[0]:
        # The square has a piece of the color inputted.
        return True
    # The square has a piece of the opposite color.
    return False


# print(blockedPawns(testBoardB,'b'))

def isolatedPawns(board, color):
    color = color[0]
    listofpawns = lookfor(board, color + 'p')
    # Get x coordinates of all the pawns:
    xlist = [x for (x, y) in listofpawns]
    isolated = 0
    for x in xlist:
        if x != 0 and x != 7:
            # For non-edge cases:
            if x - 1 not in xlist and x + 1 not in xlist:
                isolated += 1
        elif x == 0 and 1 not in xlist:
            # Left edge:
            isolated += 1
        elif x == 7 and 6 not in xlist:
            # Right edge:
            isolated += 1
    return isolated


testBoardC = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["--", "--", "--", "--", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["bp", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "bp", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


# print(isolatedPawns(testBoardC,'b'))

def pawnP(board, player):
    if player == -1:
        return (doubledPawns(board, 'w') + blockedPawns(board, 'w') + isolatedPawns(board, 'w')) - \
               (doubledPawns(board, 'b') + blockedPawns(board, 'b') + isolatedPawns(board, 'b'))

    elif player == 1:
        return (doubledPawns(board, 'b') + blockedPawns(board, 'b') + isolatedPawns(board, 'b')) - \
               (doubledPawns(board, 'w') + blockedPawns(board, 'w') + isolatedPawns(board, 'w'))


# print(doubledPawns(testBoard,'w'))
# print(blockedPawns(testBoard,'w'))
# print(isolatedPawns(testBoard,'w'))
# print(doubledPawns(testBoard,'b'))
# print(blockedPawns(testBoard,'b'))
# print(isolatedPawns(testBoard,'b'))


# Bewertungsfunktion nimmt ein Bitboard und den Player 1 wenn Weiß und -1 wenn Schwarz
def spielBewertung(bitbrd, player):
    wertW = calculateValue(bitbrd, playerWert(bitbrd, 1), 1)
    wertB = calculateValue(bitbrd, playerWert(bitbrd, -1), -1)
    pracTable = pawnP(FENtoBoard(BittoFEN(bitbrd, player)), player)
    #print(pracTable)
    if wertW==None or wertB==None or pracTable==None:
        print(wertW, wertB ,pracTable)
    if player == 1:
        return wertW - wertB + pracTable
    elif player == -1:
        return wertB - wertW + pracTable
#Testen der Bewertungsfunktion
"""def testen(fenss):
    print(spielBewertung(FENtoBit(fenss),-1))

testen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
testen("5r2/6k1/p2p3p/P1pP4/2P1p3/7P/5PK1/R7 b - -  30;")
testen("8/6pp/ppnk1p2/2p5/P3K3/2P5/1P4PP/4N3 b - -  36")
testen("8/7p/1p1n1p2/p2k2p1/P5P1/2P1K2P/2N5/8 w - -  44")
testen("rnbqk2r/pp2bppp/3p1n2/2pP4/4PB2/2N5/PPP3PP/R2QKBNR w KQkq -  7")
testen("2kr4/1p2K1R1/p2P4/P1P5/8/8/8/8 b - -  62")
testen("4r3/1p4k1/p7/P2PN1r1/5p1R/6P1/2P1R2p/4K3 w - -  36")
testen("1rb5/1p3pk1/p4np1/P2Pp1r1/R1N1P3/3B2Pp/2P2R1P/2q1QK2 b - -  27")
"""
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
# potenziell für baum erstellen auf 4 prozessoren kerne aufteilen


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
# return save

# return tre


# if __name__ == "__main__":


"""    

if __name__ == "__main__":
    player = Player()

    b = init_game()
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

    # inputs:#

    p = Player()
    # FEN="r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR W"
    # FEN="rnb1kbnr/p4ppp/1p1pp3/2p3q1/3P4/NQP1PNPB/PP3P1P/R1B1K2R w"
    # FEN="3q3r/1pp2pb1/3pkn2/1B6/3P4/4PN1P/5K1P/7R b"
    # FEN="rnbqkbnr/pp1p1ppp/4p3/1Pp5/8/2N5/P1PPPPPP/R1BQKBNR w"
    # FEN="8/4k3/8/8/8/8/3K4/8"
    FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"

    zeit = 10
    depth = 4
    wdh = 1000

    ### Unit/Benchmark Tests ###

    p.teste(FEN,zeit,turn=True)#turn ausführen
    # searchtime=p.teste(FEN,depth,search=True)#alphabetasearch zeit messen für tiefe
    # t=p.teste(FEN,wdh,zug=True)#zuggenerator only 1000 mal durchschnitt
    # t=p.teste(FEN,wdh,utility=True)#utility only
    # t=p.teste(FEN,depth,tree=True,tiefe=True)#baumspeicher bis tiefe ohne utility
    # t=p.teste(FEN,depth,tree=True,tiefe=True,utility=True)#baumspeicher bis tiefe mit utility
    # tiefe = p.teste(FEN, zeit, tree=True)  # baumspeichern bis time mit utility (Standard)
    # p.teste(FEN,zeit,baum=True)#baum ergebnis printen

    # print(searchtime)

    # transposition tables test: 8 GB Speicherplatz benoetigt!!!!!

    # p.teste(FEN,zeit,baum=True,tt=True)#baum ergebnis printen
    # print(len(p.tt.table))
    # p.tt.save_table()
    # print(len(p.tt.table))
    # del p.tt.table$

    # time=60 -> 30 sek
    # einmal
#     19467
# 12098
# 12098

# nochmal
# 22625
# 14945
# 14945

# ohne movenames missprint
# 29002
# 18749
# 18749

# ohne hash print
# 37205
# 23525
# 23525

# mit letzter spalte
# 34444
# 30164
# 30164

# vergleich 30 sek. tree mit utility:
# node 32407 :
# ph7-h6   9 4
# 32408

# vergeich mit tt
# 46119
# 32078
# 32078
