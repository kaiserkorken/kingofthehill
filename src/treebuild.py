from movegen import generate_moves
from movegen_verbose import generate_moves_verbose
from utility import utility
from tt import *
import time

def moves_to_node_h(tree, player, h=0, index=0, tt=False, utilities=True):  # added züge an node(index) mit nodes.value=None
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
            if not tt:
                
                if utilities:
                    util=utility(moves[b],player)      
                else:
                    util=None
                tree.insert_node(node, moves[b], util, h+1, names[b])  # in Node mit bitboard und wertung einsetzen
            else:
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
                            util = utility(moves[b],player)
                        else:
                            util=None
                        tt.to_table(hash, util, h + 1)
                        tree.insert_node(node, moves[b], util, h + 1, names[b], hash)
                    else:
                        tree.insert_node(node, moves[b], util[0], h + 1, names[b], hash)  # in Node mit bitboard und wertung einsetzen
            
            # auch in insert node auskommentieren! (tree.py)
            # print("u:")
            # print(utility(b))
            # print(utility(b))
            # tree.print_tree()
        else:
            print("leerer move")
            moves.remove(moves[b])

    return h+1  # h nötig?

def moves_to_node(tree, player, h=0, index=0, tt=False, utilities=True, t=False):  # added züge an node(index) mit nodes.value=None
    # while (time-(tmax/2)>0):
    node = tree.find_node(index)
    if t !=False:
        start=time.time()
    moves = generate_moves(node.b, player)  # generiere alle Züge aus Position b
    if t !=False:
        fin =time.time()-start
        t=(t+fin)
    # moves=[["a1a2",move(b)],["a2a4",b],...]
    # print("moves")
    #alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for b in range(len(moves)):
        # for b in range (len(moves)):
        if moves[b]:
            # if b[0] and b[1]:
            ### Test der names aus movegen verbose ###
            if not tt:
                
                if utilities:
                    util=utility(moves[b],player)      
                else:
                    util=None
                tree.insert_node(node, moves[b], util, h+1, index+b)  # in Node mit bitboard und wertung einsetzen
            else:
                
                    hash = tt.hash_value(moves[b],player)
                    util = tt.in_table(hash, h + 1)
                    if len(util) != 2:
                        # print(hash)
                        if utilities:
                            util = utility(moves[b],player)
                        else:
                            util=None
                        tt.to_table(hash, util, h + 1)
                        tree.insert_node(node, moves[b], util, h + 1, index+b, hash)
                    else:
                        tree.insert_node(node, moves[b], util[0], h + 1, index+b, hash)  # in Node mit bitboard und wertung einsetzen
            
            # auch in insert node auskommentieren! (tree.py)
            # print("u:")
            # print(utility(b))
            # print(utility(b))
            # tree.print_tree()
        else:
            print("leerer move")
            moves.remove(moves[b])

    return h+1,t  # h nötig?

def build_tree(tree, player,index=0, h=0, tmove=None, depth=None,utilities=True,tt=False, zob=False,gen=False):  # tree ebenen erstellen bis tiefe d
    # tmove=height[4]
    # height=[tree,h,index,step,tmove]
    # logging.info("Thread1    : started")
    # print(height)
    # if h==0:
    #     height=player.set_movetree(tree,tmove,h,index)#ein ausgerechneter zug alle züge ausrechnen
    #     print(height)
    if depth!=None:
        if depth<=0:
            return h,gen
    if depth== None:
        start = time.time()
    #height = altstep  # auskommentieren?
    altstep = len(tree.nodes)
    for z in range(index, altstep):  # eine weitere ebene durchgehen
        # print(height)
        # logging.info("Main    : creating height "+str(h))
        
        if zob:
            height = moves_to_node_h(tree,player, h, z,utilities=utilities,tt=tt)
        else:
            height,tim  = moves_to_node(tree,player, h, z,utilities=utilities,tt=tt,t=gen)
            gen=tim
 
        if depth==None:
            if start + tmove <= time.time():  # zeitlimit überschritten
                print("finished till ebene: " + str((height-1)))
                 # letzte ebene nicht fertig geworden
                return height -1
    if tmove==None:
        if depth > 0:
            index = altstep
            depth -= 1
        # altstep-=altaltstep#-=alt
        #__switch__()  # neue ebene für gegner
            return build_tree(tree,player, index, h + 1,utilities=utilities,tt=tt,tmove=tmove,depth=depth,gen=gen)
    else:
        if tmove >= time.time() - start:
            index = altstep
        #__switch__()  # neue ebene für gegner
            return build_tree(tree,player, index,h + 1,utilities=utilities,tt=tt,tmove=tmove,depth=depth,gen=gen)
    print("finished with ebene: " , height)
    return height,gen