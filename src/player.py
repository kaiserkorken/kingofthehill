from bitboard import FENtoBit,BittoFEN,BoardtoFEN#TODO letzteres bitte nicht mehr benutzen!!
from tree import Tree
import logging
import time
from treebuild import build_tree
from tree_search import search, best_node


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
    
    def turn(self, FEN, t=10):  # ein kompletter zug der ki
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
        if self.current == play and FENtoBit(FEN,True) != False:  # spieler am zug und fen bekommen

            # bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#testFEN
            tree = Tree(bb)  # ,self.tt.starthash)#leerer baum mit b als root
            if not checkmate(bb, self.current):  # Spielende überprüfen
                # tre.print_tree()
                # arr=p.set_movetree(tre,tmove)
                # tree.print_tree()
                logging.info("Main    : building movetree " + str(time.time() - start))
                height = build_tree(tree,self.current,tmove=(start + tmove - time.time()))  # time bzw. depth
                # arr[1]=tree.h
                self.current = play
                tleft = time.time() - start
                logging.info("Main    : movetree finished with height: " + str(height) + " " + str(tleft))
                logging.info("Main    : tree build finished in:" + str(time.time() - start) + "s")

                # tree.print_tree()
                # print(tree)  
                # utility auf root?
                depth = 1
                logging.info("Main    : doing minimax " + str(tleft))
                tree.sort_nodes() #FEhler bei invertet=True
                sstart = time.time()
                depth = search(tree.root, self.current, height, tsearch)
                # tree.print_node(tree.nodes[2])#teste tree nach search
                tleft = time.time() - start
                logging.info("Main    : minimax finished with depth: " + str(depth) + " in " + str(
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
    
    
    def test_turn(self, FEN, t=None, utilities=True,tt=True):  # ein kompletter zug der ki
        # print(FEN)
        
        start = time.time()
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.info("Main    : start turn " + str(start - start))
        if t:
            tmove = (t / 10) * 9  # seconds
            tsearch = t / 10
        else:
            tmove=None
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
                if t:
                    tmove=(start + tmove - time.time())
                height = build_tree(tree,self.current,tmove=tmove,utilities=utilities,tt=tt)  # time bzw. depth
                # arr[1]=tree.h
                self.current = play
                tleft = time.time() - start
                logging.info("Main    : movetree finished with height: " + str(height) + " " + str(tleft))
                logging.info("Main    : tree build finished in:" + str(time.time() - start) + "s")

                # tree.print_tree()
                # print(tree)  
                # utility auf root?
                depth = 1
                logging.info("Main    : doing minimax " + str(tleft))
                tree.sort_nodes() #FEhler bei invertet=True
                sstart = time.time()
                if t==None:
                    tsearch=1000
                depth = search(tree.root, self.current, height, tsearch)
                # tree.print_node(tree.nodes[2])#teste tree nach search
                tleft = time.time() - start
                logging.info("Main    : minimax finished with depth: " + str(depth) + " in " + str(
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


