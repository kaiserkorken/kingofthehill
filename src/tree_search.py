from anytree import Node, RenderTrees
from tree import *
import time




### constants
inf = 100000


def time_expected_next(time_last_run):
    time_exponent = 2   # Exponent mit der benötigte Zeit ansteigt
    time_expected = time_last_run**time_exponent
    return time_expected

### Hauptsuchroutine. Wählt taktisch verschiedene Suchverfahren
def search(root_node, player, time=30, max_depth):
    # iterative Tiefensuche
    time_last_run = 0.0 # benötigte Zeit für letzten Durchlauf
    time_left = time - time_last_run # Zeit bis Abbruch
    time_expected_next_run = time_expected_next(time_last_run) # Zeit, die voraussichtlich für nächste Ebene benötigt wird
    
    depth = 0
    alpha = -inf
    beta = inf
    

    
    print("search initiated with time to run: " + str(time_left))
    while (time_left > time_expected_next_run and depth <= max_depth): # Erhöhe Tiefe so lange wie Fertigstellung der Ebene noch realistisch
        time_start = time.time()
        ### Suche
        if depth > 0 # aspiration window suche um besten wert aus der letzten Tiefeniteration
            best_val, aw_failed_left, aw_failed_right = a_b_search_aspiration_window(root_node, player, depth, best_val)
        else: # kein aspiration window, da Wert geraten werden müsste
            best_val = a_b_search_principal_variation(root_node, player, depth, alpha, beta)
        depth += 1
        
        time_stop = time.time()
        time_last_run = time_stop - time_start # benötigte Zeit für letzten Durchlauf
        
        time_left -= time_last_run # Zeit bis Abbruch
        time_expected_next_run = time_expected_next(time_last_run) # Zeit, die voraussichtlich für nächste Ebene benötigt wird
    
        print("  depth : " + str(depth) + " took " str(time_last_run) + " to complete.")
        print("  best value found: " + str(best_val))
        print("     aspiration bounds failed [left/right]: " + str(aw_failed_left) + " / " + str(aw_failed_right))
        print("  time left: " + str(time_left) + ". next estimate: " str(int(time_expected_next_run)))
        
    print("search completed at depth: " + str(depth) + " with total time left: " + str(time_left))
    print("best value found: " + str(best_val))
    return best_val

# alpha beta
def a_b_search(node, player, depth=0, alpha=-inf, beta=inf):
    if depth==0 or node.children==None:
        return node.value
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
    if depth==0 or node.children==None:
        return node.value
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
def a_b_search_aspiration_window(node, player, depth=0, expected_value, widening_constant=2):
    
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
            
    
    
    
    