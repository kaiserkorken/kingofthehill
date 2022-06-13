from ctypes import util
from bitboard import FENtoBit,BittoFEN
from tree import Tree
import logging
import time
from treebuild import build_tree
from tree_search import search, best_node
from checkmate import checkmate
from utility import utility
from tt import ttable


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
    
        # alphabetasearch
        # Node = findNode(ergebnis)
        # return tree with updated values

    # TODO insert functions in class
    
    def turn(self, FEN, t=10,tt=False):  # ein kompletter zug der ki
        # print(FEN)
        start = time.time()
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.info("Main    : start turn " + str(start - start))
        tmove = (t / 10) * 9  # seconds
        tsearch = t / 10
        if tt!=False:
            tt=ttable("hashtable")
        [bb, play] = FENtoBit(FEN, True)
        # tt=ttable("testtable.mymemmap",32)#erstellen falls noetig, sonst in build tree
        if self.current == play and FENtoBit(FEN,True) != False:  # spieler am zug und fen bekommen

            # bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#testFEN
            tree = Tree(bb)  # ,self.tt.starthash)#leerer baum mit b als root
            if not checkmate(bb, self.current):  # Spielende überprüfen
                # tre.print_tree()
                # arr=p.set_movetree(tre,tmove)
                # tree.print_tree()
                logging.info("Main    : building movetree " + str(time.time() - start))
                height = build_tree(tree,self.current,tmove=(start + tmove - time.time()),tt=tt)  # time bzw. depth
                # arr[1]=tree.h
                self.current = play
                tleft = time.time() - start
                logging.info("Main    : movetree finished with height: " + str(height) + " " + str(tleft))
                logging.info("Main    : tree build finished in:" + str(time.time() - start) + "s")

                # tree.print_tree()
                # print(tree)  
                # utility auf root?
                depth = 1
                logging.info("Main    : doing tree search " + str(tleft))
                tree.sort_nodes() #FEhler bei invertet=True
                sstart = time.time()
                depth = search(tree.root, self.current, height, tsearch)
                # tree.print_node(tree.nodes[2])#teste tree nach search
                tleft = time.time() - start
                logging.info("Main    : tree search finished with depth: " + str(depth) + " in " + str(
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
    
    
    def test_turn(self, FEN, t=None, depth=None,utilities=True,tt=False,sort=False,windows=False):  # ein kompletter zug der ki
        # print(FEN)
        
        start = time.time()
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.info("Main    : start turn " + str(start - start))
        if t==None:
            tmove=None
            tsearch=1000
        else:
            tmove = (t / 10) * 9  # seconds
            tsearch = t / 10
        [bb, play] = FENtoBit(FEN, True)
        # tt=ttable("testtable.mymemmap",32)#erstellen falls noetig, sonst in build tree
        if self.current == play and FENtoBit(FEN,True) != False:  # spieler am zug und fen bekommen

            # bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#testFEN
            if tt!=False:
                
                tree = Tree(bb,tt.starthash)  # ,self.tt.starthash)#leerer baum mit b als root
            else:
                tree=Tree(bb)
            if not checkmate(bb, self.current):  # Spielende überprüfen
                # tre.print_tree()
                # arr=p.set_movetree(tre,tmove)
                # tree.print_tree()
                logging.info("Main    : building movetree " + str(time.time() - start))
                if t:
                    tmove=(start + tmove - time.time())
                height = build_tree(tree,self.current,tmove=tmove,depth=depth,utilities=True,tt=tt)  # time bzw. depth
                # arr[1]=tree.h
                
                    
                self.current = play
                tleft = time.time() - start
                logging.info("Main    : movetree finished with height: " + str(height) + " " + str(tleft))
                logging.info("Main    : tree build finished in: " + str(time.time() - start) + "s")
                if utilities==False:
                    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
                    logging.info("Main    : start utility "+str(tleft))
                    sstart=time.time()
                    if tt!=False:
                        tree.nodes[0].hash=tt.starthash
                    for x in tree.nodes[1:]:
                        if tt!=False:
                            k = -1
                            for z in range(len(alphabet)):
                                if alphabet[z] == x.name[4].lower():
                                    k = z
                                    break
                            if k == -1:
                                print(x.name, "has wrong syntax")
                                print(x.name[4], "is not an column index")
                                break
                            else:
                                y = int(x.name[5]) - 1
                                # x=np.where(alphabet==names[b][4])#a->1
                                token = x.name[0]
                                hash = tt.hash_value(x.parent.hash, k, y, token)
                                util = tt.in_table(hash, x.h + 1)
                                if len(util) != 2:
                                    # print(hash)
                                    
                                    util = utility(x.b,self.current)
                                    tt.to_table(hash, util, x.h)
                                x.value=util    
                                x.hash=hash
                        else:
                            x.value=utility(x.b,self.current)
                    tt=False
                    fin=time.time()-sstart
                    logging.info("Main    : utility finished in: " +str(fin) + "s")
                # tree.print_tree()
                # print(tree)  
                # utility auf root?
                depth = 1
                if sort:
                    logging.info("Main    : sorting nodes " + str(tleft))
                    sstart=time.time()
                    tree.sort_nodes() 
                    logging.info("Main    : finished sorting in: " + str(time.time() - sstart) + "s")
                logging.info("Main    : doing tree search " + str(tleft))
                sstart = time.time()
                # if t==None:
                #     tsearch=1000
                depth = search(tree.root, self.current, height, tsearch,old=windows)
                # tree.print_node(tree.nodes[2])#teste tree nach search
                logging.info("Main    : tree search finished with depth: " + str(depth) + " in " + str(
                    time.time() - sstart) + "s")
                tleft = time.time() - start
                logging.info("Main    : choosing good move " + str(tleft))
                node = best_node(tree)  # besten zug auswaehlen
                # move=tree.find_node(node.index)
                # logging.info("Main    : finished turn "+str(start+t))
                finish = time.time()
                self.__switch__()
                FEN = BittoFEN(node.b, self.current)
                self.__switch__()
                logging.info("Main    : finished turn in " + str(finish - start) + "s")
                if t==None:
                    t=0
                logging.info("Main    : time remaining: " + str(start + t - time.time()))
                print("lenge: ",len(tree.nodes))
        else:  # Spieler nicht dran
            FEN = False
        # self.__switch__()#Spieler wechseln (egal ob zug gemacht odeer nicht
        return FEN
