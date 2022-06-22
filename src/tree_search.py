import time
import numpy as np
import random
import copy

from utility import *
from tree import *
from bitboard import *
from treebuild import *
from checkmate import checkmate



### constants
inf = 100000



def best_node(tree, player_code=1):
    #tree.print_tree()
    # nodes height 1 sammeln
    #print(tree.root.children)
    children = list(tree.root.children)
    # print(children)
    # print(children)
    if len(children) > 0:  # falls Züge vorhanden
        values = player_code * np.array([x.value for x in children])
        #"""
        #"""
        # values = [value for index,parent,b,value,h in children]
        # print(tree)
        # print(children)
        # return best node of nodes of tree height 1 
        best_nodes = []
        # print(children)
        while len(children) > 0:
            possible_best_node = children[np.argmax(values)]
            children.pop(np.argmax(values))  # bzw. values.remove(node.index)
            # print(children)
            values = player_code * np.array([x.value for x in children])
            #"""
            if best_nodes:  # falls Liste schon Element enthält
                if possible_best_node.value == best_nodes[0].value:  # falls ein weiterer gleichwertiger Zug existiert
                    best_nodes.append(possible_best_node)
                else:  # falls nächstbester Zug schlechter
                    break  # alle besten Züge gefunden
            else:  # falls Liste noch leer
                #print(possible_best_node.value)
                #print(checkmate(possible_best_node.b,(-1) ** possible_best_node.h))
                if checkmate(possible_best_node.b,(-1) ** possible_best_node.h) == False:  # erster Zug muss auf jeden Fall legal sein
                    best_nodes.append(possible_best_node)  # ,player)=(-1)^höhe
        # best_nodes sollte nun mindestens einen Zug enthalten. Dieser ist immer legal
        #print(best_nodes)
        if len(best_nodes) == 1:  # falls nur ein Zug vorhanden
            #print("best0:", best_nodes[0].value)
            return best_nodes[0]  # gib Zug zurück
        elif len(best_nodes) > 1:
            while len(best_nodes) > 0:  # entferne Züge von Liste bis zufälliger legaler Zug gefunden
                best_node = random.choice(best_nodes)  # wähle zufällig besten Zug
                if checkmate(best_node.b, (-1) ** best_node.h) == False:  # falls Zug legal
                    #print("best:", best_node.value)
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
def search(root_node, player, max_depth, search_time=30, old=False, verbose=False):
    # iterative Tiefensuche
    time_last_run = 0.0 # benötigte Zeit für letzten Durchlauf
    time_left = search_time - time_last_run # Zeit bis Abbruch
    time_expected_next_run = time_expected_next(time_last_run) # Zeit, die voraussichtlich für nächste Ebene benötigt wird
    
    depth = 0
    alpha = -inf
    beta = inf
    
    ### DEEP COPY TREE VON ALTER ITERATION

    if verbose:
        print("search initiated with time to run: " + str(time_left))
    while (time_left > time_expected_next_run and depth <= max_depth): # Erhöhe Tiefe so lange wie Fertigstellung der Ebene noch realistisch
        time_start = time.time()
        ### Suche
        if old:
            best_val = a_b_search(root_node, player)
        else:
            if depth > 0: # aspiration window suche um besten wert aus der letzten Tiefeniteration
                best_val, aw_failed_left, aw_failed_right = a_b_search_aspiration_window(root_node, player, best_val, depth)
                if verbose:
                    print("     aspiration bounds failed [left/right]: " + str(aw_failed_left) + " / " + str(aw_failed_right))
            else: # kein aspiration window, da Wert geraten werden müsste
                best_val = a_b_search_principal_variation(root_node, player, depth, alpha, beta)
        
        
        time_stop = time.time()
        time_last_run = time_stop - time_start # benötigte Zeit für letzten Durchlauf
        
        time_left -= time_last_run # Zeit bis Abbruch
        time_expected_next_run = time_expected_next(time_last_run) # Zeit, die voraussichtlich für nächste Ebene benötigt wird
        if verbose:
            print("  depth : " + str(depth) + " took " + str(time_last_run) + " to complete.")
            print("  best value found: " + str(best_val))
            print("  time left: " + str(time_left) + ". next estimate: " + str(time_expected_next_run))
        depth += 1
           
        
    if verbose:
        print("search completed at depth: " + str(depth) + " with total time left: " + str(time_left))
        print("best value found: " + str(best_val))
        
    return depth#best_val



def minimax(node, player, depth=0):
        if depth == 0 or node.children == None:
            if node.value == None:
                node.value = utility(node.b, player)
            return node.value
        if player == 1:
            v = -1000000
            for x in node.children:
                v = max(v, minimax(x, depth - 1, -player))
                node.value = v
            return v
        else:
            v = 1000000
            for x in node.children:
                v = min(v, minimax(x, depth - 1, -player))
                node.value = v
            return v
     
def minimax_bak(node, depth=0, ismax=True):
        if depth == 0 or node.children == None:
            if node.value == None:
                node.value = utility(node.b, player)
            return node.value
        if ismax:
            v = 1000000
            for x in node.children:
                v = max(v, minimax(x, depth - 1, False))
                node.value = v
            return v
        else:
            v = -1000000
            for x in node.children:
                v = min(v, minimax(x, depth - 1, True))
                node.value = v
            return v
        
        


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
#    print(node)
#    print(player)
#    print(depth)
    if depth==0 or len(node.children)==0: 
        if node.value == None:
            node.value = utility(node.b, player)
        print(depth, node.value)
        return node.value
    #val=1000000
    for child in node.children:
        #print(a_b_search(child, -player, depth-1, -beta, -alpha,))
        val = -a_b_search(child, -player, depth-1, -beta, -alpha,)
        node.value = val
        if (val > alpha):
            alpha = val
            if (alpha >= beta):
                break
    print(depth, val)
    return val



# principal variation
def a_b_search_principal_variation(node, player, depth=0, alpha=-inf, beta=inf):
    ###TEST
    #return a_b_search(node, player, depth)
    
    ####
    if depth==0 or node.children==None:
        if node.value == None:
            node.value = utility(node.b, player)
        return node.value
    PV_gefunden = False
    best = -inf
    for child in node.children:
        if PV_gefunden:
            val = -(a_b_search_principal_variation(child, -player, depth-1, -alpha-1, -alpha,))
            #node.value = val
            if (val > alpha and val < beta):
                val = -(a_b_search_principal_variation(child, -player, depth-1, -beta, -val,))
                #node.value = val
        else:
            val = -(a_b_search_principal_variation(child, -player, depth-1, -beta, -alpha,))
            #node.value = val
        if (val > best):
            if (val >= beta):
                return val
            best = val
            if val > alpha:
                alpha = val
                PV_gefunden = True
    return best

# aspriation window suche 
def a_b_search_aspiration_window(node, player, expected_value, depth=0, widening_constant=1.5):
    
    alpha = expected_value - widening_constant
    beta = expected_value + widening_constant
    a_w_failed_alpha = 0
    a_w_failed_beta = 0
    a_w_window_too_small = True
    while a_w_window_too_small:

        best = a_b_search(node, player, depth, alpha, beta)
        
        if best < alpha: # tief gescheitert
            a_w_failed_alpha += 1
            alpha -= widening_constant**a_w_failed_alpha
        elif best > beta: # hoch gescheitert
            a_w_failed_beta += 1
            beta += widening_constant**a_w_failed_beta
        else:
            a_w_window_too_small = False
    return best, a_w_failed_alpha, a_w_failed_beta
            
    
    
    
    
def bench_tree_search_list(tree_dict_list, tree_height=None, search_time=30, search_mode='search', verbose=True):
    if verbose: 
        print('- initiate benchmark -')
        print('-- no. of benchmarks: ' + str(len(tree_dict_list)))
        print('--- search mode is: ' + search_mode)
    t_bench = [bench_tree_search(tree_dict, tree_height, search_time, search_mode, verbose=True) for tree_dict in tree_dict_list]
    t_avg = sum(t_bench) / len(t_bench)
    if verbose:
        print("AVERAGE TIME IN seconds: " + str(t_avg))
    return t_avg

def bench_tree_search(tree_dict, tree_height=None, search_time=30, search_mode='search', verbose=True):
    
    tree = tree_dict['tree']
    player_code = tree_dict['player_code']
    if tree_height == None:
        tree_height = tree_dict['tree_height']
        
    if verbose:
        print('----- initiate search -----')
        print('------ search mode is: ' + search_mode)
        print('------ maximum search height is: ' + str(tree_height))
#    print(tree)
#    print(player_code)
#    print(tree_height)
#   print('==========')
    t_start = time.time()
    if search_mode == 'search':
        best_value = search(tree.root, player_code, tree_height, search_time)
    elif search_mode == 'minimax':
        best_value = minimax(tree.root, player_code, tree_height)
    elif search_mode == 'alpha_beta':
        best_value = a_b_search(tree.root, player_code, tree_height, alpha=-inf, beta=inf)
    elif search_mode == 'principal_variation':
        best_value = a_b_search_principal_variation(tree.root, player_code, tree_height, alpha=-inf, beta=inf)
    elif search_mode == 'aspiration_windows':
        [best_value, failed_left, failed_right] = a_b_search_aspiration_window(tree.root, player_code, 0, tree_height)
    else:
        print('ERROR: no search_mode found')
        pass
    t_bench = time.time() - t_start
    
    if verbose:
        print('search took:')
        print(t_bench)
        print('best value found: ' + str(best_value))
        print('should have found something with sign of: ' + str(best_node(tree, player_code).value))
    return t_bench

def build_bench_tree_list(FEN_list, tree_height=3, verbose=True):
    bench_tree_list = [build_bench_tree(FEN, tree_height, verbose) for FEN in FEN_list]
    return bench_tree_list

def build_bench_tree(FEN, tree_height=3, verbose=True):
    [b, player_code] = FENtoBit(FEN, True)
    if verbose:
        print('starte Baumaufbau mit FEN: ')
        print(FEN)
    tree = Tree(b)
    
    height = build_tree(tree, player_code, depth=tree_height)
    dep = len(tree.nodes)
    if verbose:
        print("baum fertig")

    #for i in tree.nodes:
    #    i.value = utility(i.b, player_code)
    if verbose:
        print('baum bewertet')
        
    tree_dict = {'tree':tree, 'player_code':player_code, 'tree_height':tree_height}
    return tree_dict

# Stellung 1: 
FEN_1 = 'rnbqkbnr/p4ppp/1p1pp3/2p5/3P4/NQP1PNPB/PP3P1P/R1B1K2R b'
# Stellung 2: 
FEN_2 = 'r1b1kbnr/pN2pp1p/2P5/1p4qp/3P3P/2P5/PP3PP1/R1B1K1NR w'

if __name__ == "__main__":
    FEN_list = [FEN_1, FEN_2]
    
    tree_height = 3
    search_time = 30
    verbose = True

    
    if 'tree_dict_list' in globals():
        pass
    elif 'tree_dict_list' in locals():
        pass
    else:
        tree_dict_list = build_bench_tree_list(FEN_list, tree_height, verbose)
        
    
    search_mode = 'search'
    t_bench = bench_tree_search_list(copy.deepcopy(tree_dict_list), tree_height, search_time, search_mode, verbose)

    search_mode = 'minimax'
    t_bench = bench_tree_search_list(copy.deepcopy(tree_dict_list), tree_height, search_time, search_mode, verbose)
    search_mode = 'alpha_beta'
    t_bench = bench_tree_search_list(copy.deepcopy(tree_dict_list), tree_height, search_time, search_mode, verbose)
    
    search_mode = 'principal_variation'
    t_bench = bench_tree_search_list(copy.deepcopy(tree_dict_list), tree_height, search_time, search_mode, verbose)
    search_mode = 'aspiration_windows'
    t_bench = bench_tree_search_list(copy.deepcopy(tree_dict_list), tree_height, search_time, search_mode, verbose)
