from anytree import Node, RenderTree
class tree(object):
    def __init__(self,FEN) -> None:
        self.init_tree(FEN)
        #self.node beinhaltet festen index, value und dict
    def generate_search_tree(self,b, player):
        # generate a searchtree and search for possible pseudolegal moves
        moves = Node('root')
        
        return moves
    def init_tree(self,FEN):
        #TODO implement function
        #root=FEN
        return False

    def findNode(self,index):
        #return Node.index(index)
        pass
    def insert_node(self,value):
        #insert_node(value[0],value[1])
        pass
    def delete_node(self):
        pass
