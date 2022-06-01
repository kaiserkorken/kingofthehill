from anytree import Node, RenderTrees
from tree import *

''' alte version: 
    def alphabetasearch(self,node,depth=0,ismax=True):
        if depth==0 or node.children==None:
            return node.value
        if ismax:
            v=1000000
            for x in node.children:
                v=max(v,self.alphabetasearch(x,depth-1,False))
                node.value=v
            return v
        else:
            v=-1000000
            for x in node.children:
                v=min(v,self.alphabetasearch(x,depth-1,True))
                node.value=v
            return v
        
'''

'''
 int miniMax(int spieler, int tiefe,
             int alpha, int beta) {
    if (tiefe == 0 or keineZuegeMehr(spieler))
       return bewerten(spieler);
    int maxWert = alpha;
    Zugliste = generiereMoeglicheZuege(spieler);
    for each (Zug in Zugliste) {
       fuehreZugAus(Zug);
       int wert = -miniMax(-spieler, tiefe-1,
                           -beta, -maxWert);
       macheZugRueckgaengig(Zug);
       if (wert > maxWert) {
          maxWert = wert;
          if (tiefe == gewuenschteTiefe)
             gespeicherterZug = Zug;
          if (maxWert >= beta)
             break;
       }
    }
    return maxWert;
 }

'''


def alpha_beta_search(node, player, depth=0, alpha=-100000, beta=100000):
    if depth==0 or node.children==None:
        return node.value
    #val=1000000
    for child in node.children:
        val = -(alpha_beta_search(child, -player, depth-1,-beta, -alpha,))
        node.value = val
        if (val > alpha):
            alpha = val
            if (alpha >= beta):
                break
    return val



''' principal variation
int AlphaBeta(int tiefe, int alpha, int beta)
{
    if (tiefe == 0)
        return Bewerten();
    BOOL PVgefunden = FALSE;
    best = -unendlich;
    Zugliste = GeneriereMoeglicheZuege();
    for each (Zug in Zugliste)
    {
        FuehreZugAus(Zug);
        if (PVgefunden)
        {
            wert = -AlphaBeta(tiefe-1, -alpha-1, -alpha);
            if (wert > alpha && wert < beta)
                wert = -AlphaBeta(tiefe-1, -beta, -wert);
        } else
            wert = -AlphaBeta(tiefe-1, -beta, -alpha);
        MacheZugRueckgaengig(Zug);
        if (wert > best)
        {
            if (wert >= beta)
                return wert;
            best = wert;
            if (wert > alpha
                
            {
                alpha = wert;
                PVgefunden = TRUE;
            }
        }
    }
    return best;
}
'''

def alpha_beta_search_pv(node, player, depth=0, alpha=-100000, beta=100000):
    if depth==0 or node.children==None:
        return node.value
    PV_gefunden = False
    best = -100000
    for child in node.children:
        if PV_gefunden:
            val = -(alpha_beta_search_pv(child, -player, depth-1, -alpha-1, -alpha,))
            node.value = val
            if (val > alpha and val < beta):
                val = -(alpha_beta_search_pv(child, -player, depth-1, -beta, -val,))
                node.value = val
        else:
            val = -(alpha_beta_search_pv(child, -player, depth-1, -beta, -alpha,))
            node.value = val
        if (val > best):
            if (val >= beta):
                return val
            best = val
            if val > alpha:
                alpha = val
                PV_gefunden = True
    return best