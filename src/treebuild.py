from movegen_verbose import generate_moves_verbose
from utility import utility
from tt import *
import time

def moves_to_node(tree, player, h=0, index=0, tt=True, utilities=True):  # added züge an node(index) mit nodes.value=None
    # while (time-(tmax/2)>0):
    node = tree.find_node(index)
    
    moves, names = generate_moves_verbose(node.b, player)  # generiere alle Züge aus Position b
    # moves=[["a1a2",move(b)],["a2a4",b],...]
    # print("moves")
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for b in range(len(moves)):
        # for b in range (len(moves)):
        if moves[b]:
            # if b[0] and b[1]:
            ### Test der names aus movegen verbose ###
            if tt:
                x = -1
                for z in range(len(alphabet)):
                    if alphabet[z] == names[b][4].lower():
                        x = z
                        break
                if x == -1:
                    print(names[b], "has wrong syntax")
                    print(names[b][4], "is not an column index")
                    break
                else:
                    y = int(names[b][5]) - 1
                    # x=np.where(alphabet==names[b][4])#a->1
                    token = names[b][0]
                    hash = tt.hash_value(node.hash, x, y, token)
                    util = tt.in_table(hash, h + 1)
                    if len(util) != 2:
                        # print(hash)
                        if utilities:
                            util = utility(moves[b])
                        else:
                            util=None
                        tt.to_table(hash, util, h + 1)
                        tree.insert_node(node, moves[b], util, h + 1, names[b], hash)
                    else:
                        tree.insert_node(node, moves[b], util[0], h + 1, names[b], hash)  # in Node mit bitboard und wertung einsetzen
            else:
                if utilities:
                    util=utility(moves[b])      
                else:
                    util=None
                tree.insert_node(node, moves[b], util, h+1, names[b])  # in Node mit bitboard und wertung einsetzen

            # auch in insert node auskommentieren! (tree.py)
            # print("u:")
            # print(utility(b))
            # print(utility(b))
            # tree.print_tree()
        else:
            print("leerer move")
            moves.remove(moves[b])

    return h  # h nötig?


def build_tree(tree, player,index=0, altstep=1, h=0, tmove=None, utilities=True,tt=True):  # tree ebenen erstellen bis tiefe d
    # tmove=height[4]
    # height=[tree,h,index,step,tmove]
    # logging.info("Thread1    : started")
    # print(height)
    # if h==0:
    #     height=player.set_movetree(tree,tmove,h,index)#ein ausgerechneter zug alle züge ausrechnen
    #     print(height)
    if tmove!= None:
        start = time.time()
    height = altstep  # auskommentieren?
    altstep = len(tree.nodes)
    for z in range(index, altstep):  # eine weitere ebene durchgehen
        # print(height)
        # logging.info("Main    : creating height "+str(h))
        
        height = build_tree(tree,player, h + 1, z,utilities=utilities,tt=tt)
 
        if start + tmove <= time.time():  # zeitlimit überschritten
            print("finished till ebene: " + str((h + 1)))
            height -= 1  # letzte ebene nicht fertig geworden
            return height
    if tmove==None:
        depth -= 1
        if depth > 0:
            index = altstep
        # altstep-=altaltstep#-=alt
        #__switch__()  # neue ebene für gegner
            return build_tree(tree,player, h + 1, index,utilities=utilities,tt=tt)
    else:
        if tmove >= time.time() - start:
            index = altstep
        #__switch__()  # neue ebene für gegner
            return build_tree(tree,player, h + 1, index,utilities=utilities,tt=tt)
    print("finished with ebene: " + h + 1)
    return height