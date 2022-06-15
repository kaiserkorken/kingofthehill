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
            
if __name__ == "__main__":
    ## DEMO ## TODO andere Demos auf aktualität überprüfen ung ggf. removen
    #                   ich brauch davon nichts mehr

    # inputs:#

    #p = Player()
    
    # FEN="r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR W"
    FEN="rnb1kbnr/p4ppp/1p1pp3/2p3q1/3P4/NQP1PNPB/PP3P1P/R1B1K2R w"
    # FEN="3q3r/1pp2pb1/3pkn2/1B6/3P4/4PN1P/5K1P/7R b"
    # FEN="rnbqkbnr/pp1p1ppp/4p3/1Pp5/8/2N5/P1PPPPPP/R1BQKBNR w"
    # FEN="8/4k3/8/8/8/8/3K4/8"
    # FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
    player=Player()
    zeit = 20
    tiefe = 3
    wdh = 1000
    
    tt=ttable("testtable")
    #player.test_turn(FEN, t=None, depth=None,utilities=True,tt=False,sort=False,windows=False)
    player.test_turn(FEN, depth=tiefe, tt=tt)
    tt.save_table()


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