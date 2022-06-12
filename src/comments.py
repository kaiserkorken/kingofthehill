

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