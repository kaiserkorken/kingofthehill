from anytree import Node
from tree import *
import time
import numpy as np
import random

from tree import *
from player import checkmate


### constants
inf = 100000


def best_node(tree):
    #tree.print_tree()
    # nodes height 1 sammeln
    #print(tree.root.children)
    children = list(tree.root.children)
    # print(children)
    # print(children)
    if len(children) > 0:  # falls Züge vorhanden
        values = []
        for x in children:
            values.append(x.value)
        # values = [value for index,parent,b,value,h in children]
        # print(tree)
        # print(children)
        print(values)
        # return best node of nodes of tree height 1 
        best_nodes = []
        # print(children)
        while len(children) > 0:
            possible_best_node = children[np.argmax(values)]
            children.pop(np.argmax(values))  # bzw. values.remove(node.index)
            # print(children)
            values = []
            for x in children:
                values.append(x.value)

            if best_nodes:  # falls Liste schon Element enthält
                if possible_best_node.value == best_nodes[0].value:  # falls ein weiterer gleichwertiger Zug existiert
                    best_nodes.append(possible_best_node)
                else:  # falls nächstbester Zug schlechter
                    break  # alle besten Züge gefunden
            else:  # falls Liste noch leer
                print(possible_best_node.value)
                print(checkmate(possible_best_node.b,
                             (-1) ** possible_best_node.h))
                if checkmate(possible_best_node.b,
                             (-1) ** possible_best_node.h) == False:  # erster Zug muss auf jeden Fall legal sein
                    best_nodes.append(possible_best_node)  # ,player)=(-1)^höhe
        # best_nodes sollte nun mindestens einen Zug enthalten. Dieser ist immer legal
        print(best_nodes)
        if len(best_nodes) == 1:  # falls nur ein Zug vorhanden
            print("best0:", best_nodes[0])
            return best_nodes[0]  # gib Zug zurück
        elif len(best_nodes) > 1:
            while len(best_nodes) > 0:  # entferne Züge von Liste bis zufälliger legaler Zug gefunden
                best_node = random.choice(best_nodes)  # wähle zufällig besten Zug
                if checkmate(best_node, (-1) ** best_node.h) == False:  # falls Zug legal
                    print("best:", best_node)
                    return best_node  # gib Zug zurück
                else:
                    best_nodes.remove(best_node)
        print('kein guter Zug vorhanden!')
        children = list(tree.root.children)
        # print("doof: ",children[0])
        node = random.choice(children)
        return node

    else:
        print('kein Zug vorhanden!')
        print("else: ", children[0])
        return children[0]

def time_expected_next(time_last_run):
    time_exponent = 10   # Exponent mit der benötigte Zeit ansteigt
    time_expected = time_last_run*time_exponent
    return time_expected

### Hauptsuchroutine. Wählt taktisch verschiedene Suchverfahren
def search(root_node, player, max_depth, search_time=30):
    # iterative Tiefensuche
    time_last_run = 0.0 # benötigte Zeit für letzten Durchlauf
    time_left = search_time - time_last_run # Zeit bis Abbruch
    time_expected_next_run = time_expected_next(time_last_run) # Zeit, die voraussichtlich für nächste Ebene benötigt wird
    
    depth = 0
    alpha = -inf
    beta = inf
    
    ### DEEP COPY TREE VON ALTER ITERATION

    
    print("search initiated with time to run: " + str(time_left))
    while (time_left > time_expected_next_run and depth <= max_depth): # Erhöhe Tiefe so lange wie Fertigstellung der Ebene noch realistisch
        time_start = time.time()
        ### Suche
        if depth > 0: # aspiration window suche um besten wert aus der letzten Tiefeniteration
            best_val, aw_failed_left, aw_failed_right = a_b_search_aspiration_window(root_node, player, best_val, depth)
        else: # kein aspiration window, da Wert geraten werden müsste
            best_val = a_b_search_principal_variation(root_node, player, depth, alpha, beta)
        
        
        time_stop = time.time()
        time_last_run = time_stop - time_start # benötigte Zeit für letzten Durchlauf
        
        time_left -= time_last_run # Zeit bis Abbruch
        time_expected_next_run = time_expected_next(time_last_run) # Zeit, die voraussichtlich für nächste Ebene benötigt wird
    
        print("  depth : " + str(depth) + " took " + str(time_last_run) + " to complete.")
        print("  best value found: " + str(best_val))
        if depth > 0:
            print("     aspiration bounds failed [left/right]: " + str(aw_failed_left) + " / " + str(aw_failed_right))
        print("  time left: " + str(time_left) + ". next estimate: " + str(time_expected_next_run))
        
        depth += 1
        
        
    print("search completed at depth: " + str(depth) + " with total time left: " + str(time_left))
    print("best value found: " + str(best_val))
    
    return best_val


def a_b_search_bak(node, depth=0, ismax=True):
    #print("depth: " + str(depth) + ", player: " + str(ismax) + ", node_value: " + str(node.value) + ", value*player: " + str(node.value*ismax))

    if depth == 0 or node.children == None:
        player = -(-1**ismax)
        #print("player: " + str(player) + ", node_value: " + str(node.value) + ", value*player: " + str(node.value*player))
        return node.value
    if ismax:
        v = -1000000
        for x in node.children:
            v = max(v, a_b_search_bak(x, depth - 1, False))
            node.value = v
        return v
    else:
        v = 1000000
        for x in node.children:
            v = min(v, a_b_search_bak(x, depth - 1, True))
            node.value = v
        return v


# alpha beta
def a_b_search(node, player, depth=0, alpha=-inf, beta=inf):
    if depth==0 or node.children==None:
        return node.value*player
    #val=1000000
    for child in node.children:
        val = -(a_b_search(child, -player, depth-1,-beta, -alpha,))
        node.value = val
        if (val > alpha):
            alpha = val
            if (alpha >= beta):
                break
    return val



# principal variation
def a_b_search_principal_variation(node, player, depth=0, alpha=-inf, beta=inf):
    ###TEST
    return a_b_search_bak(node, depth, player)
    
    ####
    if depth==0 or node.children==None:
        print("player: " + str(player) + ", node_value: " + str(node.value) + ", value*player: " + str(node.value*player))
        return node.value*player
    PV_gefunden = False
    best = -inf
    for child in node.children:
        if PV_gefunden:
            val = -(a_b_search_principal_variation(child, -player, depth-1, -alpha-1, -alpha,))
            node.value = val
            if (val > alpha and val < beta):
                val = -(a_b_search_principal_variation(child, -player, depth-1, -beta, -val,))
                node.value = val
        else:
            val = -(a_b_search_principal_variation(child, -player, depth-1, -beta, -alpha,))
            node.value = val
        if (val > best):
            if (val >= beta):
                return val
            best = val
            if val > alpha:
                alpha = val
                PV_gefunden = True
    return best

# aspriation window suche 
def a_b_search_aspiration_window(node, player, expected_value, depth=0, widening_constant=2):
    
    alpha = expected_value - widening_constant
    beta = expected_value + widening_constant
    a_w_failed_alpha = 0
    a_w_failed_beta = 0
    a_w_window_too_small = True
    while a_w_window_too_small:

        best = a_b_search_principal_variation(node, player, depth, alpha, beta)
        
        if best < alpha: # tief gescheitert
            a_w_failed_alpha += 1
            alpha -= widening_constant**a_w_failed_alpha
        elif best > beta: # hoch gescheitert
            a_w_failed_beta += 1
            beta += widening_constant**a_w_failed_beta
        else:
            a_w_window_too_small = False
    return best, a_w_failed_alpha, a_w_failed_beta
            
    
    
    
    