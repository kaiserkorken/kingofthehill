from email import message
from player import *
from movegen_verbose import generate_moves_verbose
from tt import *
    
def teste(player, FEN, value=0, search=False, zug=False, utility=False, tree=False, tiefe=False, turn=False,
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
                moves = generate_moves_verbose(FENtoBit(FEN),player)
            zeit = (time.time() - zeit) / value

            # print(moves)
            return zeit
        elif utility and not tree:  # utility only
            tree = Tree(FENtoBit(FEN))
            height = build_tree(tree, 3)#TODO er
            dep = len(tree.nodes)
            print("baum fertig")
            zeit = time.time()
            for i in tree.nodes:
                i.value = utility(i.b)
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
                h= build_tree(t, depth, utility)  # timer einbauen
                # t.print_tree()
                return time.time() - zeit
            else:  # baumspeichern bis time mit utility (Standard)
                zeit = value
                build_tree(t, zeit)
                t.print_node(t.nodes[len(t.nodes) - 1])
                print(len(t.nodes))
                return t.nodes[len(t.nodes) - 1].h
        if search:  # alphabetasearch zeit messen für tiefe
            # if value>=0:
            zeit = time.time()
            tree = Tree(FENtoBit(FEN))
            arr = build_tree(tree, 2)
            dep = len(tree.nodes)
            zeit = time.time() - zeit
            print("baum fertig" + str(zeit))
            zeit = time.time()
            for i in tree.nodes:
                i.value = utility(i.b)
            zeit = time.time() - zeit
            print("utility fertig" + str(zeit))
            searchtime = time.time()
            tiefe = value
            # while(depth<=arr[1] and tiefe>=depth):#noch zeit und noch nicht so tief wie baumhöhe
            search(tree.root, tiefe)  # indizes aktualisieren#wertung des bestmöglichen zuges ausgeben
            # children = list(tree.root.children)
            # print("search:",depth,children[0].value)
            return time.time() - searchtime
        elif turn:  # normaler zug #und alphabetasearch bis zeit um
            FEN = turn(FEN, value)
            print(FEN)
            return (FEN)
            # print_board(FENtoBit(FEN))
        elif baum:  # baum ergebnis printen # teste tree.py
            bb = FENtoBit(FEN)
            if tt:
                tt = ttable("testtable", dict=True)
                tre = Tree(bb, tt.starthash)
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
                build_tree()#TODO efrd
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
            
def bench_utility(FEN):
    
    tt=ttable("testtable")
    tree=Tree(FENtoBit(FEN),tt.starthash)
    
    start=time.time()
    h,gen=build_tree(tree,1,depth=3,tt=tt,gen=True) 
    fin=time.time()
    
    gen=gen/len(tree.nodes)
    average=(fin-start)/len(tree.nodes)-gen
    print("tt on")
    print("average time util per node:",average)
    print("average time gen per node:",gen)
    
    tt.save_table()
    
    start=time.time()
    tree=Tree(FENtoBit(FEN))
    
    h,gen=build_tree(tree,1,depth=3,gen=True) 
    fin=time.time()
    gen=gen/len(tree.nodes)
    average=(fin-start)/len(tree.nodes)-gen
    print("tt off")
    print("average time util per node:",average)
    print("average time gen per node:",gen)
    
    print("sort nodes")
    start=time.time()
    tree.sort_nodes()
    fin=time.time()
    average=(fin-start)/len(tree.nodes)
    print("average time per node:",average)
    
               
if __name__ == "__main__":
    ## DEMO ## TODO andere Demos auf aktualität überprüfen ung ggf. removen
    #                   ich brauch davon nichts mehr

    # inputs:#

    #p = Player()
    
    # FEN="r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR W"
    # FEN="rnb1kbnr/p4ppp/1p1pp3/2p3q1/3P4/NQP1PNPB/PP3P1P/R1B1K2R w"
    # FEN="3q3r/1pp2pb1/3pkn2/1B6/3P4/4PN1P/5K1P/7R b"
    # FEN="rnbqkbnr/pp1p1ppp/4p3/1Pp5/8/2N5/P1PPPPPP/R1BQKBNR w"
    # FEN="8/4k3/8/8/8/8/3K4/8"
    FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
    FEN="rnb2bnr/pppqp2p/3pk1p1/8/3pN3/6N1/PPP1QPPP/R1B1KB1R W"
    player=Player()
    zeit = 1.5
    tiefe = 2
    wdh = 1000
    
   # tt=ttable("testtable")
    player.turn(FEN,t=zeit)
    #ttables-> sucheebene 3 start 0.14 -> 0.02
    player.close()
        #FEN, t=None, depth=None,utilities=True,tt=False,sort=False,windows=False)
    #player.test_turn(FEN, depth=tiefe, tt=tt)
    # tt.save_table()
    # # Stellung 1: 
    # FEN_1 = 'rnbqkbnr/p4ppp/1p1pp3/2p5/3P4/NQP1PNPB/PP3P1P/R1B1K2R b'
    # # Stellung 2: 
    # FEN_2 = 'r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w'
    # bench_utility(FEN_1)
    # bench_utility(FEN_2)
    # tt on
    # average time per node: 0.00048032262470915717
    # tt off
    # average time per node: 0.000621712507699357
    # sort nodes
    # average time per node: 0.0013640800649051114
    # loading
    # tt on
    # average time per node: 0.0004853243456936962
    # tt off
    # average time per node: 0.0007842872908112389
    # sort nodes
    # average time per node: 0.0010878187932980132
    



    #tt neu starten 81 sek
    #tt initialisiert 79 sek.
    #tt ohne verbose neu starten 37 sek.
    #tt ohne verbose ohne tt 35/38 sek
    #tt ohne verbose ohne bittofen 41,37,41   richtig: 44, 39.8, 42 sek. ohne 35,5
    ## tt ohne verbose bittobyte 33, 26 sek.

    ### Unit/Benchmark Tests alt###

    # p.teste(FEN,zeit,turn=True)#turn ausführen
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

# 70700 nodes h 3
# + 20 sek treebuild (tt)
# -> - sek utility