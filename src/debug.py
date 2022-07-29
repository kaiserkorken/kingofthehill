from bitboard import FENtoBit
from player import * 
from tree import *
from treebuild import *
from movegen_verbose import generate_moves_verbose


class Gamestate():
    def __init__(self, FEN, unittest_move_names=None, verbose=False):
        self.FEN = FEN
        self.reset()
        
        if unittest_move_names() != None:
            self.unittest_move_names = unittest_move_names
        
        if verbose:
            self.print_info()
            
    def build_tree(self, tree_height=1, utilities=False, verbose=False):
        self.height = build_tree(self.tree, self.player, depth=tree_height, utilities=utilities)
        
        if verbose:
            print('starte Baumaufbau zu FEN: ')
            print(self.FEN)
            self.tree.print_tree()
            
    def generate_moves(self, verbose=False):
        self.possible_moves, self.possible_move_names = generate_moves_verbose(self.b, self.player.current)
        return self.possible_moves, self.possible_move_names
        
    def reset(self, verbose=False):
        
        [self.b, player_current] = FENtoBit(self.FEN, True)
        self.player = Player(player_current)
    
        self.tree = Tree(self.b)
        
        self.generate_moves(verbose)
        
        
    def print_info(self):
        print(self.FEN)
        print(self.player)
        print(self.possible_moves)
        print(self.possible_move_names)
