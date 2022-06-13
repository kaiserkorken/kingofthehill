from bitboard import FENtoBit, BittoFEN
def checkmate(bitboard,player):
    counter = 0
    sss = bitboard#FENtoBit(BittoFEN(bitboard))
    mitte = False
    for countA, value in enumerate(sss['k']):
        for countB, info in enumerate(value):
            if info == True:
                counter = counter+1
                if countA==3 and countB ==3 or countA==3 and countB ==4 or countA==4 and countB ==3 or countA==4 and countB ==4:
                    mitte = True
            else:
                pass
    if counter < 2 or mitte == True:
        return True
    else:
        return mitte