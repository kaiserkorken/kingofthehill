"""Responsible for handling user input and displaying the current GameState object"""

import pygame as p

class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element of the list has 2 characters.
        # First is color
        # Second is the type
        #"--" - represents an emprty space with no piece.
        self.startboard = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.board=self.startboard
        self.whiteToMove = True
        self.moveLog = []

    # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1




    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap turns

    def undoMove(self):
        if len(self.moveLog)!=0: #make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back

    #All moves considering checks
    def getValidMoves(self):
        pass

    #All moves withour considering checks
    def getAllPossibleMoves(self):
        moves = []


class Move():
    # maps keys for values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


WIDTH = HEIGHT = 512
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE, SQ_SIZE))

    # We can load images by calling 'IMAGES['wp']
class GUI():
    def __init__(self,single=True):
        p.init()
        self.single=single
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.clock = p.time.Clock()
        self.screen.fill(p.Color("white"))
        self.gs = GameState()
        self.klick=False
        self.player=1
        loadImages() #only once
        self.running = True
        self.sqSelected = () # no square is selected, keeps track of the last click on the user
        self.playerClicks =  [] #keeps track of player clicks (two tuples)
       
    def reset(self):
        
        self.klick=False
        self.single=False
        self.player=1
        self.running = True
        self.sqSelected = () # no square is selected, keeps track of the last click on the user
        self.playerClicks =  []
        self.draw(self.gs.startboard)
        
    def draw(self,board):
        self.gs.board=board
        self.drawGameState()
        self.clock.tick(MAX_FPS)
        p.display.flip()
        
    def run(self):
        for e in p.event.get():
            if e.type == p.QUIT:
                self.running = False
            #mouse handler
            if self.single:
                if e.type ==p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if self.sqSelected == (row,col): # square was clicked twice
                        self.sqSelected = () # deselect
                        self.playerClicks = [] #clear the player clicks
                    else:
                        self.sqSelected = (row,col)
                        self.playerClicks.append(self.sqSelected) # append for 1st and 2nd clicks
                    if len(self.playerClicks) == 2: #after the 2nd click
                        move = Move(self.playerClicks[0],self.playerClicks[1],self.gs.board)
                        print(move.getChessNotation())
                        self.gs.makeMove(move)
                        self.sqSelected = () # reset user clicks
                        self.playerClicks = []
                        self.klick=True
                        self.player*=(-1)
                        # move = ChessEngie.Move(bestMoveX,bestMoveY,gs.board
                #key handlers
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z: #undo when key is pressed
                        self.gs.undoMove()


            self.drawGameState()
            self.clock.tick(MAX_FPS)
            p.display.flip()

    def drawGameState(self):
        drawBoard(self.screen)
        drawPieces(self.screen, self.gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    bild = GUI()
    while bild.running:
        bild.run()