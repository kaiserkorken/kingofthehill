class interface(object):
    def __init__(self) -> None:
        self.FEN=[63]
    
    #turns bitboard into FEN Strings
    #bitboard: 
    #bit[0]== unten links
    #bit[7] == unten rechts
    #bit[63]== oben rechts
    #FEN:
    def BittoFEN(type,board):
        for x in board:
            if board[x]:
                self.FEN(type,x)
        return board
    def FEN(x,y):
        #speichert x an der stelle y im FEN string
        self.FEN[y]=x