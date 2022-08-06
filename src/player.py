import logging
from tree_search import *
from tt import *


def timer(function):
    start_time = time.time()
    function()
    elapsed = time.time() - start_time
    print("--- %s seconds ---" % (elapsed))
    return elapsed


# Player-Klasse. Macht eigentlich noch nix außer klartextübersetzung 1->W, -1->B, kann auch ersetzt werden.
class Player():
    def __init__(self,current=1):
        # weiß beginnt
        self.current = current
        self.tt=ttable("hashtable")
        self.opening=ttable("opening",open=True)
        self.ergebnis=[]
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
            # TODO remis implementfor local tests

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
        
    def close(self):
        self.tt.save_table()
        self.opening.save_table()
    
    def reset(self):
        self.ergebnis=[]
        
    def do_move(self, FEN, t=10,tt=True,name=False,check=False,fast=False):
        opening=False#bisher kein zug aus den opening tables
        start = time.time()
        tchoose=t
        if type(self.ergebnis)!=Tree:
        #len(self.ergebnis.root.children)<=0:
            
            format = "%(asctime)s: %(message)s"
            logging.basicConfig(format=format, level=logging.INFO,
                                datefmt="%H:%M:%S")
            logging.info("Main    : start turn " + str(start - start))
            ergebnis,tchoose=self.turn(FEN,t,tt,name,check)
            if ergebnis==False:
                return False
            if name:
                names=[]    
            moves=[]
            if type(ergebnis)!=Tree:#[move,name] from opening table
                if name:
                    test=FENtoBit(ergebnis)
                    for x,y in generate_moves_verbose(FENtoBit(FEN),self.current):
                        if x==test:
                            first=y
                            if fast:
                                return first
                            else:
                                moves.append(test)
                                names.append(first)
                            break
                else:
                    if fast:
                        return ergebnis
                    else:
                        moves.append(ergebnis)
                opening=[moves,names]
                ergebnis,tchoose=self.turn(FEN,t,tt,name,check,opening=False)
                if ergebnis==False:
                    return False
                    
            self.ergebnis=ergebnis
        tleft =start-time.time()
        logging.info("Main    : choosing good move " + str(tchoose))
        node=best_node(self.ergebnis,self.current,name,tchoose,opening)
        self.ergebnis.delete_node(node)
        #FEN=node.name
        finish = time.time()
        logging.info("Main    : chosen move: " +str(node.name)+" in "+ str(finish - start) + "s")
        logging.info("Main    : time remaining: " + str(start + t - finish))
        if name:
            #move=node.name.split("-")
            return node.name#move[1]
        else:
            #self.__switch__()
            return BittoFEN(node.b, -self.current)
        self.__switch__()
        
        print("size: ",len(ergebnis.nodes))
        if name:
            return names
        return move
        
    def turn(self, FEN, t=10,tt=True,name=False,check=False,opening=True):  # ein kompletter zug der ki
        print("time: "+str(t))
        # print(FEN)
        #t-=0.5#buffer ping etc
        start = time.time()
        # format = "%(asctime)s: %(message)s"
        # logging.basicConfig(format=format, level=logging.INFO,
        #                     datefmt="%H:%M:%S")
        # logging.info("Main    : start turn " + str(start - start))
        # tmove = t*0.999  # 99.9% move time, 0.1% search and choose time -> 0.3% - 2% time unused
        # #tmove = (t/100)*90  # seconds
        tmove=t*0.99
        
        tmove=tmove*0.98# 2 % slippage in time in movetree function
        # #tsearch = t / 2
        
        
        try:
            [bb, play] = FENtoBit(FEN, True)
        except:
            print("illegal fen")
            return False, False
        # tt=ttable("testtable.mymemmap",32)#erstellen falls noetig, sonst in build tree
        # if not name:
        if self.current != play:#TODO player current richtig setzen
            return False, False
            #and FENtoBit(FEN,True) != False:  # spieler am zug und fen bekommen
        
        if FENtoBit(FEN,True) != False:
            # bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#testFEN
            tree = Tree(bb)  # ,self.tt.starthash)#leerer baum mit b als root
            if t<=0:#panic mode
                #TODO test
                #treebuild until height 1 w/o utility
                build_tree(tree,self.current,depth=1,tt=self.tt)
                return tree
            #     moves, names = generate_moves_verbose(bb, play)
            #     if name:
            #         return random.choice(names)
            #     move=random.choice(moves)
            #     return BittoFEN(move)
               
            if not checkmate(bb, play) or checkmate(bb,play):  # Spielende überprüfen
                if opening:#opening table verwenden
                    hash=self.opening.hash_value(bb,play)
                    info=self.opening.in_table(hash)
                    if len(info)!=0:
                        logging.info("Main    : choosing from opening table: " + str(time.time()-start))
                        FEN=[]
                        moves=info
                        FEN.append(moves)
                        #FEN=random.choice(moves)
                        
                        if name:
                            b=[]
                            for y in range(len(moves)):
                                b.append(moves[y].split(" ")[0])
                            move, names = generate_moves_verbose(bb, play)
                            for x in range(len(move)):
                                for y in range(len(moves)):
                                    if BittoFEN(move[x]).split(" ")[0]==b[y]:
                                        FEN.append(names[x])
                                        #break
                            
                                    
                            
                        logging.info("Main    : finished using opening table: " + str(time.time()-start))
                        return FEN,time.time()-start
            
                if tt!=False:
                    tt=self.tt
                    # tre.print_tree()
                    # arr=p.set_movetree(tre,tmove)
                    # tree.print_tree()
                    #logging.info("Main    : building movetree " + str(time.time() - start))
                    #height, lefttime = build_tree(tree,play,tmove=(start + tmove - time.time()),tt=tt)  # time bzw. depth
                    # arr[1]=tree.h
                    #tree.sort_nodes()
                    tsearch=t-tmove#+lefttime
                    if tsearch<=0:
                        #if not name:
                            return tree,tsearch#BittoFEN(tree.root.children[0].b,play)
                        # else:
                        #     return tree.root.children[0].name
                    if tsearch<0.005:#dauer bis zu ebene 1 zu suchen/bewerten
                        
                        return tree, tsearch
                        # node=best_node(tree,play,time=False,check=check)
                        # FEN = BittoFEN(node.b, play)
                        # if not name:
                        #     return FEN
                        # else:
                        #     return node.name
                    
                    self.current = play
                    # tleft = time.time() - start
                    # logging.info("Main    : movetree finished with height: " + str(height) + " " + str(tleft))
                    # logging.info("Main    : tree build finished in:" + str(time.time() - start) + "s")

                    # tree.print_tree()
                    # print(tree)  
                    # utility auf root?
                    #depth = 1
                    tleft=time.time()-start
                    logging.info("Main    : doing tree search " + str(tleft))
                    #tree.sort_nodes() #FEhler bei invertet=True
                    sstart = time.time()
                    self.tree=tree
                    #tree.print_tree()
                    depth,tree= search(self, tmove, tsearch)
                    self.tree=tree
                    if tsearch<0:
                        tleft= (time.time()-sstart)
                        
                        return tree,t-tleft#BittoFEN(tree.root.children[0].b,play)
                    #tree.print_node(tree.root.children[0])
                    #tree.print_tree()
                    self.current=play
                    # tree.print_node(tree.nodes[2])#teste tree nach search
                    tleft = time.time() - start
                    logging.info("Main    : tree search finished with depth: " + str(depth)+" and "+ str((tree.nodes))+ " Nodes in " + str(
                        time.time() - sstart) + "s")
                    # logging.info("Main    : sorting nodes " + str(tleft))
                    # sstart= time.time()
                    # tree.sort_nodes(tree.root)
                    # fin=time.time()
                    # logging.info("Main    : finished sorting "+str((tree.nodes))+" in " + str(fin-sstart))
                    tleft= time.time()-start
                    return tree, t-tleft
                    node = best_node(tree,self.current,check)  # besten zug auswaehlen
                    # move=tree.find_node(node.index)
                    # logging.info("Main    : finished turn "+str(start+t))
                    finish = time.time()
                    self.__switch__()
                    if name:
                        #move=node.name.split("-")
                        FEN=node.name#move[1]
                    else:
                        FEN = BittoFEN(node.b, self.current)
                    self.__switch__()
                    logging.info("Main    : finished turn in " + str(finish - start) + "s")
                    logging.info("Main    : time remaining: " + str(start + t - time.time()))
                    print("size: ",len(tree.nodes))
            else:
                return False, False#FEN=False
        else:  # Spieler nicht dran
            return False, False#FEN = False
        # self.__switch__()#Spieler wechseln (egal ob zug gemacht odeer nicht
        # logging.info("Main    : chosen move: " +str(FEN)+" "+ str(start + t - time.time()))
        # return tree
    
    
    def test_turn(self, FEN, t=10,tt=True,name=False,check=False,opening=True):  # ein kompletter zug der ki
        print("time: "+str(t))
        # print(FEN)
        t-=0.5#buffer ping etc
        start = time.time()
        # format = "%(asctime)s: %(message)s"
        # logging.basicConfig(format=format, level=logging.INFO,
        #                     datefmt="%H:%M:%S")
        # logging.info("Main    : start turn " + str(start - start))
        # tmove = t*0.999  # 99.9% move time, 0.1% search and choose time -> 0.3% - 2% time unused
        # #tmove = (t/100)*90  # seconds
        tmove=t*0.99
        
        tmove=tmove*0.98# 2 % slippage in time in movetree function
        # #tsearch = t / 2
        
        
       
        [bb, play] = FENtoBit(FEN, True)
        
        # tt=ttable("testtable.mymemmap",32)#erstellen falls noetig, sonst in build tree
        # if not name:
        if self.current != play:#TODO player current richtig setzen
            return False, False
            #and FENtoBit(FEN,True) != False:  # spieler am zug und fen bekommen
        
        if FENtoBit(FEN,True) != False:
            # bb=FENtoBit("r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w")#testFEN
            tree = Tree(bb)  # ,self.tt.starthash)#leerer baum mit b als root
            if t<=0:#panic mode
                #TODO test
                #treebuild until height 1 w/o utility
                build_tree(tree,self.current,depth=1,tt=self.tt)
                return tree
            #     moves, names = generate_moves_verbose(bb, play)
            #     if name:
            #         return random.choice(names)
            #     move=random.choice(moves)
            #     return BittoFEN(move)
               
            if not checkmate(bb, play):  # Spielende überprüfen
                if opening:#opening table verwenden
                    hash=self.opening.hash_value(bb,play)
                    info=self.opening.in_table(hash)
                    if len(info)!=0:
                        logging.info("Main    : choosing from opening table: " + str(time.time()-start))
                        FEN=[]
                        moves=info
                        FEN.append(moves)
                        #FEN=random.choice(moves)
                        
                        if name:
                            b=[]
                            for y in range(len(moves)):
                                b.append(moves[y].split(" ")[0])
                            move, names = generate_moves_verbose(bb, play)
                            for x in range(len(move)):
                                for y in range(len(moves)):
                                    if BittoFEN(move[x]).split(" ")[0]==b[y]:
                                        FEN.append(names[x])
                                        #break
                            
                                    
                            
                        logging.info("Main    : finished using opening table: " + str(time.time()-start))
                        return FEN,time.time()-start
            
                if tt!=False:
                    tt=self.tt
                    # tre.print_tree()
                    # arr=p.set_movetree(tre,tmove)
                    # tree.print_tree()
                    logging.info("Main    : building movetree " + str(time.time() - start))
                    height, lefttime = build_tree(tree,play,tmove=(start + tmove - time.time()),tt=tt)  # time bzw. depth
                    # arr[1]=tree.h
                    tree.sort_nodes()
                    tsearch=t-tmove+lefttime
                    if tsearch<=0:
                        #if not name:
                            return tree,tsearch#BittoFEN(tree.root.children[0].b,play)
                        # else:
                        #     return tree.root.children[0].name
                    if tsearch<0.005:#dauer bis zu ebene 1 zu suchen/bewerten
                        
                        return tree, tsearch
                        # node=best_node(tree,play,time=False,check=check)
                        # FEN = BittoFEN(node.b, play)
                        # if not name:
                        #     return FEN
                        # else:
                        #     return node.name
                    
                    self.current = play
                    tleft = time.time() - start
                    logging.info("Main    : movetree finished with height: " + str(height) + " " + str(tleft))
                    logging.info("Main    : tree build finished in:" + str(time.time() - start) + "s")

                    # tree.print_tree()
                    # print(tree)  
                    # utility auf root?
                    #depth = 1
                    logging.info("Main    : doing tree search " + str(tleft))
                    #tree.sort_nodes() #FEhler bei invertet=True
                    sstart = time.time()
                    #tree.print_tree()
                    depth,tree= search(tree,self, height, tsearch)
                    if tsearch<0:
                        tleft= (time.time()-sstart)
                        
                        return tree,t-tleft#BittoFEN(tree.root.children[0].b,play)
                    #tree.print_node(tree.root.children[0])
                    #tree.print_tree()
                    self.current=play
                    # tree.print_node(tree.nodes[2])#teste tree nach search
                    tleft = time.time() - start
                    logging.info("Main    : tree search finished with depth: " + str(depth) + " in " + str(
                        time.time() - sstart) + "s")
                    logging.info("Main    : sorting nodes " + str(tleft))
                    sstart= time.time()
                    tree.sort_nodes()
                    fin=time.time()
                    logging.info("Main    : finished sorting "+str((tree.nodes))+" in " + str(fin-sstart))
                    tleft= time.time()-start
                    return tree, t-tleft
                    node = best_node(tree,self.current,check)  # besten zug auswaehlen
                    # move=tree.find_node(node.index)
                    # logging.info("Main    : finished turn "+str(start+t))
                    finish = time.time()
                    self.__switch__()
                    if name:
                        #move=node.name.split("-")
                        FEN=node.name#move[1]
                    else:
                        FEN = BittoFEN(node.b, self.current)
                    self.__switch__()
                    logging.info("Main    : finished turn in " + str(finish - start) + "s")
                    logging.info("Main    : time remaining: " + str(start + t - time.time()))
                    print("size: ",len(tree.nodes))
            else:
                return False, False#FEN=False
        else:  # Spieler nicht dran
            return False, False#FEN = False
        # self.__switch__()#Spieler wechseln (egal ob zug gemacht odeer nicht
        # logging.info("Main    : chosen move: " +str(FEN)+" "+ str(start + t - time.time()))
        # return tree
    
    
    
