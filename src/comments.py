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
    
    ###zob tables ###
    
    ##implements transposition tables and saves them to files##
#https://numpy.org/doc/stable/reference/generated/numpy.memmap.html
#TODO hashes speichern, depth dazuschreiben
import random
from bitboard import *
import json
class ttable(object):
    def __init__(self,location="table",dict=False,bits=False):
        random.seed()
        self.bits=64
        if bits:
            self.bits=bits
        self.location=location#TODO auf syntax checken
        self.file=self.location
        self.dict=dict
        #self.file=path.join(mkdtemp(),self.location)
        #random.getstate()
        #print(self.rand)
        #if dict:
        
        self.location+=".json"#".npy"
        #else:
            
            #self.location+=".mymemmap"
        if self.dict:
            self.rand=(3, (2147483648, 740739888, 2063981967, 1600749517, 3123965064, 485359283, 894777725, 1512459936, 3276968069, 1880623715, 3373806884, 619175452, 929208763, 2126939311, 3394186341, 3581929110, 3280108440, 543781379, 280883797, 1037763408, 3817203414, 2734860660, 3772160557, 3279657269, 3240843350, 2152781180, 1811441848, 2278150820, 67356578, 3604598442, 648653649, 2488877346, 1358518412, 2410755478, 4235430459, 404054294, 1823631926, 3934941069, 540177018, 1539090055, 2999528328, 565721774, 4194883450, 1413466282, 3713910556, 813927380, 3308051987, 557451169, 2931102151, 3605051969, 2957318770, 128769231, 3472046393, 1844460317, 1347595827, 486112714, 1489209251, 3110614388, 240979180, 1399596702, 2217960314, 4230744384, 1908944995, 2236395601, 3134017482, 4030770220, 4177881190, 1656405800, 3043351831, 20201871, 2545654296, 226592387, 2234873682, 175241793, 2943564210, 80565300, 1327731731, 1325501066, 2889663859, 2752706326, 3508494444, 2637384794, 596605504, 2389605324, 3334098987, 3897581936, 1732446278, 2203090896, 995016186, 1085185435, 4060276665, 1013110690, 1097531311, 2127324760, 4021156011, 2804838638, 3096481999, 3530037358, 2933379125, 4151868796, 1872704010, 17853353, 1104967904, 2450439435, 3051909919, 3656251779, 751005962, 2624944267, 113097078, 1508403620, 3007663552, 2649087942, 2193227494, 1421632197, 2494093039, 230562624, 2307785385, 3397936871, 3913892102, 1459221147, 127721132, 1882059182, 1414870370, 1660086803, 943671938, 1016914877, 2267395757, 2352087819, 977035139, 3554855877, 4093892431, 2299105826, 1760399613, 1413401388, 3013660748, 3450813507, 798065234, 3189246211, 1246273452, 2335734468, 2060519845, 3924022466, 3381648381, 1885986135, 1757265960, 1760226545, 2580443804, 1946573950, 899220420, 1001058688, 3670388013, 2879733409, 1687482396, 394071663, 2426426448, 3617494288, 1500737294, 279347054, 1473294011, 2505255791, 2974157948, 1473225781, 782172778, 532886200, 3683938906, 3503588656, 2470414874, 1268731542, 2746601821, 3499016255, 2564387782, 130014568, 2426363908, 
2667274345, 3053388788, 3430297060, 1090133034, 3787674748, 3921536044, 3001977420, 1752474041, 3588235139, 242825164, 1603529295, 2381018004, 1363050015, 619538696, 1319188660, 1142177564, 1405575321, 653941972, 750259275, 526461555, 2146281943, 534079721, 2797008818, 2834472407, 2451079617, 3041923454, 1385192, 2439599787, 3897897294, 600092456, 2128163276, 2333290403, 2821367273, 3824220595, 3074288379, 561602938, 3361315992, 3480785876, 678996371, 3408972473, 697346477, 3161778477, 3018184165, 713241326, 2453654744, 675302948, 1847023316, 1711204961, 4187261254, 1700374680, 2872888844, 2951511286, 3441533148, 3727110945, 572394319, 3152857641, 1896982236, 21032661, 2734470912, 1780444757, 1463593016, 846237092, 1053425497, 809396022, 3689628492, 945471179, 3444924087, 561293235, 1833575452, 2009226151, 1710676631, 2357115654, 2053317667, 3474063825, 856470880, 1691608307, 672215538, 1025511267, 4075511662, 697207199, 1874301551, 3419391363, 306363034, 1807335997, 2567278365, 494620125, 3954540229, 2924810199, 526656173, 2401414307, 2848141470, 3516237717, 156090388, 2485004800, 248233763, 3377667256, 3758505965, 3830229709, 1445871753, 2244390592, 2099320861, 2255643925, 1154184202, 1120913335, 2963568174, 3814434028, 4255910823, 1961528957, 2985344141, 2053102264, 2770216485, 4029338135, 4285347173, 3839886763, 1588170876, 4130573250, 2351585299, 3913019057, 2426951753, 1575860625, 3984553, 210689329, 3173969003, 2386085559, 2106305624, 3848585797, 3231878108, 3249933932, 442826206, 1025851179, 781420393, 1575564692, 428171017, 4042895703, 950762521, 3016813956, 3331251075, 1772494514, 357754039, 679388344, 4285158506, 1280176815, 4035345499, 4234588028, 1063705500, 3465435812, 3295988021, 2708750090, 1724671552, 2467352576, 860827769, 770927074, 3334574660, 4045868052, 2287552332, 3077123525, 2061263760, 829084158, 2735413128, 3178907691, 3130811646, 2363668406, 2342074717, 1912021977, 2485605216, 2107109182, 83605899, 4222589083, 2480367200, 1354200379, 2380511583, 2201717841, 1433197305, 1405951529, 813285327, 3472105405, 3483082610, 1414849009, 4240034499, 3877719643, 2714342951, 2079139832, 1129820667, 1488308769, 4118168119, 2798728395, 1341768737, 2835714669, 3516769379, 432903164, 3326041730, 952146623, 3441707002, 2409823160, 
1072816463, 3260401598, 1868769179, 2328641141, 1004236816, 3758970940, 1003040292, 3454140049, 3473391200, 4060847206, 
1031794611, 1268942390, 168957511, 604066662, 709352092, 3069848693, 593448487, 1171172692, 3860985080, 3959618800, 3807183079, 3465433201, 3300835154, 180906434, 1623894095, 2920585387, 1079690813, 179340150, 2980355641, 4247167807, 3529753195, 1415941059, 2806155210, 3776827745, 407042081, 2283589959, 3127963129, 111615592, 3810975718, 3561252942, 1128494763, 4168261310, 2191224990, 876655941, 3805264218, 2706448125, 1823139022, 3605711639, 2621213687, 806387509, 2219789292, 4291430057, 4109113652, 2727320241, 1306740823, 390054111, 33648781, 2978904186, 140661468, 3669629288, 3493305316, 1808805457, 952611924, 3020138952, 4129270134, 2872199023, 2847876497, 3988833103, 1805078230, 1667743725, 1197470671, 1678704071, 547977344, 1870513958, 3787595385, 2707588441, 1464351179, 4122940226, 674150045, 3189061168, 2123484335, 1810609641, 2402246357, 1326075358, 1058063160, 4234894645, 3154272683, 972580495, 942177120, 3298619458, 2881946984, 3527300498, 2447428598, 1999199156, 752461181, 3496045965, 951511875, 3737109461, 1377816180, 1201835943, 1787789281, 483068958, 1521618379, 3694163103, 956551767, 355358686, 3376905084, 4084682360, 3126991227, 34965736, 2761313805, 1314332119, 4261004863, 2497872671, 1482737948, 2300760315, 958584277, 1030023163, 177426537, 3238683790, 3742638265, 3489749485, 1987872572, 3936158192, 446878089, 2300446322, 1916629547, 2054265318, 359516782, 303146901, 2735250192, 2078688279, 513698917, 2846860051, 1612859752, 3025649100, 4089498487, 4083502679, 957417006, 1645438900, 3112676917, 3668757292, 2798003191, 1259683591, 3725080026, 2549820140, 2375241210, 2158230206, 1487794072, 4086323620, 3372317567, 4111251397, 140526666, 1765297615, 3078606584, 1961767847, 4080576967, 3306710606, 3983278493, 1529804913, 1498056745, 2166383383, 3744648003, 394726493, 2977075026, 4175065214, 1724476319, 577388489, 568140277, 1664447482, 1632188531, 227171822, 1419421955, 619288330, 1130322952, 586345171, 2674582171, 3260285779, 446039843, 3520188554, 3990184686, 3385053486, 587483545, 2041896781, 1764904934, 1633331187, 3307100110, 1979175462, 1755794745, 2706548787, 3661829767, 2209764470, 3523357673, 3194957078, 3875091647, 3170655481, 778281092, 2110483515, 3712849283, 1584005872, 722219705, 3979379914, 918671637, 188967440, 1272150539, 215841390, 1116003955, 1674844800, 2538913898, 3765301114, 3431431883, 931253985, 2508781921, 4273960913, 
1913297848, 476756986, 3659456674, 53042883, 4159154121, 259096126, 592101509, 4202824252, 3284799133, 2077883448, 3754829409, 977594828, 3735829885, 1804337456, 3461395918, 788790334, 56153880, 3645896125, 1036292400, 515457042, 3998701555, 2993452895, 107484246, 1797111786, 2383807316, 11859820, 1594258179, 2944567874, 2049689067, 2664143795, 1996639538, 539488091, 1086144828, 722658595, 2758180626, 2267798438, 530922579, 83051673, 1357654734, 188940971, 2393472447, 3687896826, 1627402622, 624), None)
            random.setstate(self.rand)
            self.zobTable = self.init_table()# zobTable.append(random.randint(1,2**64 - 1)for x in range(8))#,[8*enpassant]]
            self.tokens=np.asarray(['p','b','r','n','q','k'])#umgedreht, weil pawns oefter als kings gesucht werden
        
        b = init_game()#TODO wrong start board, missing black tokens
        self.starthash = 0
        self.init_hash(b)
        # if not self.init_hash(b):
        #     return False
        #print(hashValue)
        #print("hash in table?:")
        #self.table=self.create_table(self.bits)
        try:
            print("loading")
            self.table=self.load_table()
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
            print("create new")
            self.table=self.create_table()
        

        if self.starthash:
            #print((2**32)-self.starthash)
            #print(self.table[(2**self.bits)-self.starthash])
            self.to_table(self.starthash,0,-1)
            #self.table[(2**self.bits)-self.starthash]=[0,-1]
            #print(self.table[(2**self.bits)-self.starthash])
        #self.save_table(self.table)#?
        #self.table=self.load_table()#TODO datei bereits vorhanden checken
    
    def init_hash(self,b):
        if self.dict:
            board = np.empty((8,8), dtype=str)
            board[:] = '_'
            
            # black player: lower case, white player: UPPER CASE
            
            board[b['B'] & b['k']] = 'k'
            board[b['B'] & b['q']] = 'q'
            board[b['B'] & b['n']] = 'n'
            board[b['B'] & b['r']] = 'r'
            board[b['B'] & b['b']] = 'b'
            board[b['B'] & b['p']] = 'p'
            
            board[b['W'] & b['k']] = 'K'
            board[b['W'] & b['q']] = 'Q'
            board[b['W'] & b['n']] = 'N'
            board[b['W'] & b['r']] = 'R'
            board[b['W'] & b['b']] = 'B'
            board[b['W'] & b['p']] = 'P'
            for i in range(8):
                for j in range(8):
                    if board[i,j]!="_":
                        piece = self.indexing(board[i,j])
                        if piece==-1:#TODO zu teuer?
                            return False
                        self.starthash^= self.zobTable[i][j][piece]
        else:
            self.starthash=self.hash_value(b)

    def indexing(self,piece):
        ''' mapping token to a particular number'''
        index=0
        if piece.islower():
            index=5
        else:
            piece=piece.lower()
        #try:
        newindex=np.where(self.tokens==piece)
        if len(newindex)==0:#tokenerror
            print("\""+piece+"\"is not a valid token!")
            return -1
        index+=newindex[0][0]
        # except Exception as inst:
        #     print(type(inst))    # the exception instance
        #     print(inst.args)     # arguments stored in .args
        #     print(inst)          # __str__ allows args to be printed directly,
        #                          # but may be overridden in exception subclasses
        #     # x, y = inst.args     # unpack args
        #     # print('x =', x)
        #     # print('y =', y)
        #     return -1
        return index

    def init_table(self):
        random.setstate(self.rand)
        #                           von,bis (64 bit)         i Zufallszahlen                 m*              n grossens feld
        zobTable = [[[random.randint(1,2**self.bits - 1) for i in range(2*6)]for m in range(8)]for n in range(8)]
        # array= [[[whitepawn0,..., blackking0],...,[whitepawn7,...,blackking7]],...,[...,[...,blackking7]]
        # array[y][x][t]= zufallszahl fuer token t an position(x,y)
        # token 0-8 white, 9-15 black, reihenfolge tokens: pawn,,queen,king

        # zobTable.append(random.randint(1,2**64 - 1))# ,blacksturn
        # zobTable.append(random.randint(1,2**64 - 1)for x in range(4))#,[kleine,grosse,Rochade,W/B]
        # zobTable.append(random.randint(1,2**64 - 1)for x in range(8))#,[8*enpassant]]
        return zobTable#save

    def create_table(self):
    
        #table=np.arange(2**bits-1)
        #table.fill(0.0001)
        #table=np.full_like(2**bits-1,None)
        #table[]=None
        #table=np.full(2**bits-1,None) #ValueError: Maximum allowed dimension exceeded
    
        #table = np.memmap('test.mymemmap', dtype="int16", mode='w+', shape=(2000,2),offset=2*16/8)#maximal 65535
        #if self.dict:
        self.table=dict()
            #np(self.file, dtype='int8', mode='w+', shape=(2**self.bits-1,2))
            #alternativ numpy structured array
        #else:
            #self.table= np.memmap(self.file, dtype='int8', mode='w+', shape=(2**self.bits-1,2))
        #32 bit:4294967295, 16bit: 65535, 64 bit 18446744073709551615
        return self.table


    def set_location(self,location):
        self.location=location

    def save_table(self,location=False):
        # st=self.location
        # if location != False:
        #     st=location
        # np.save(st,self.table)
        #if self.dict:
            
        self.table= dict(self.table)
        string=json.dumps(self.table)
        with open(self.location, 'w+') as outfile:
            json.dump(string, outfile)
                
            # dtype= dict(names=["id","value","depth"],formats=["f8","f8","f8"])
            # self.table=np.array(list(self.table),dtype=dtype)
            # np.save(self.location,self.table,allow_pickle=True)
        #else:
            #self.table.flush()

    def load_table(self):
        #if self.dict:
        with open(self.location, 'r') as j:
            content = json.loads(j.read())   
        self.table=json.loads(content)
        #else:
            #self.table= np.memmap(self.file, dtype='int8', mode='r+', shape=(2**self.bits-1,2))
        
        return self.table

    def in_table(self,hash,h):
        #if self.dict:
        try:
            value=self.table[str(hash)]
        except:
            return []
        #else:
            #value=self.table[hash]
            
        depth=value[1]
        #if depth!=0:#depth ungleich 0 (sonst nicht initialisiert)
        if h<=depth:#aelterer wert bereits sicherer(tiefer)
            return value
        #print(value)
        #print(h,depth)
        return []
        
        4294967295
    def to_table(self,hash,value,depth):
        #if self.dict:
        if len(self.table)<=588823529:#-> kleiner 2 GB
            self.table[str(hash)]=[int(value),int(depth)]
        else:
            return False
            
        # else:
        #     self.table[hash]=[value,depth]

    def hash_value(self,b,x=None,y=None,token=None):#to = [pos x, pos y, "K"], deshalb von vorteil: node.name -> a1a2K=to
        if self.dict:#-> b=hash
            h=b
            return self.zobhash(h,x,y,token)
        else:
            return hash(BittoByte(b,x))#BittoFEN(b))#hash=b#x=Player
       
    def zobhash(self,hash,x,y,token):
        #value=self.starthash
        hash^= self.zobTable[y][x][self.indexing(token)]
        #print(hash)
        return hash
    
def in_table(table,hash):
    if dict:
        value=table[str(hash)]
    else:
        value=table[hash]
    if value!=0:
        return value
    else:
        return False
if __name__ == "__main__":
    #tt=ttable("testtable.mymemmap")
    #tt.create_table()
    #print(tt.in_table(569765))
    tt=ttable("testtable",dict=True)
    if tt.starthash:
        tt.to_table(569765,127,9)#hier utility einsetzen
        print(tt.in_table(569765,1))
        print("save table")
        tt.save_table()
        del tt.table
        tt.table=tt.load_table()
        #table=tt.load_table()
        print(tt.in_table(569765,1))
        #print(tt.in_table(3531))

    ### minimax implementation (Pseudocode): ### 
    # hash=tt.hash_value(parenthash,[x,y,"K"] bzw. "a1a2K")
    # new=tt.in_table(hash)
    # if not new:
    #     new=utility()
    
from player import *
player = Player()  
def newGame():#unsere KI gegen sich selbst
    time=10
    player=[]
    player[0]=Player()
    player[1]=Player()
    FEN=BittoFEN(init_game())
    x=0
    while (not checkmate(FENtoBit(FEN),player[x])):
        FEN=player[x].turn(FEN,time)#TODO hier zeitbeschränkung z.B. per threads einbauen
        x=(x+1)%2#wechsel zwischen 0 und 1
        #print_bitboard(FEN)
    print("Spieler"+x+"hat verloren!")

### DEMO ###
#TODO Demo kompatibel mit neuen klassen
    

if __name__ == "__main__":
    pass