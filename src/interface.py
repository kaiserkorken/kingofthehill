from kingofthehill import *
"""
class game(object):
    def __init__(self,fen):§
        self.fen=fen
"""
    #FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    #1. rows 1-8
    #2. w/b
    #3. castling
    #4. en passent (position)
    #5. turns w/out capture/pawn advance
    #6. overall moves

    
    
    #FEN:
def BittoFEN(b):#turns bitboard into FEN Strings
    FENboard=[]
    check=["k","q","n","r","b","p"]
    for z in check:
        for x in range(63):#maybe replace with b[z] and (b["W"] or b["B"])
            for y in range(63):
                if b[z][x,y] and b["W"][x,y]:
                    FENboard[x+y]=z.upper()
                elif b[z][x,y] and b["B"][x,y]:
                    FENboard[y+x]=z
                else:
                    FENboard.append(1)#bis 8 stacken danach /
    #build string
    remember=0
    test=True
    FEN=""
    for x in range(63):
        if test==False and remember!= 0:
            FEN.join(remember)
            remember=0
        elif FENboard[x]==1:
            remember+=1
            test=False
        else:
            FEN.join(x)
            test=True
        #add missing arguments to FEN
    return FEN


def FENtoBit(fen):
    info = fen.split(" ")
    board = info[0].split("/")
    b = giveBitboards()
    ver=0
    for y in range(7):  # a row
        ver=0#versatz, falls int index verschiebt
        for x in range(7):  # a field in a row
            "".islower()
            print(board[y][x])
            try:#int
                ver+=int(board[y][x])# field is a character
                if ver+x>=8:#zeike fertig
                    break
            except:#string
                if (board[y][x]).islower():
                    b["B"][x+ver, y] = True
                else:
                    b["W"][x+ver, y] = True
                b[board[y][x]][x+ver, y] = True#adding specific character
                
    # TODO
    # using the other values in FEN string
    #bitboard: 
    #bit[0]== bottom left
    #bit[7] == bottom right
    #bit[63]== upper right
    return b

#try
x=FENtoBit("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#y=BittoFEN(b)
#print(x)#bzw. printBitboard(x)