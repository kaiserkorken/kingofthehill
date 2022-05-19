## to read: https://anytree.readthedocs.io/en/latest/api/anytree.node.html#anytree.node.anynode.AnyNode
## -> statt Node('root) -> AnyNode(id=..)

from tkinter.messagebox import NO
from anytree import Node, RenderTree
# TODO: Umbenennung tree -> Tree
class tree(object):
    def __init__(self,FEN) -> None:
        self.index=0
        self.nodes=[]
        self.h=0
        self.value=None
        self.init_tree(FEN)
        #self.node beinhaltet festen index, value und dict
        #node.value=value
        #node.h=height

    def generate_search_tree(self,b, player):
        # generate a searchtree and search for possible pseudolegal moves
        moves = Node('root')
        
        return moves
    def init_tree(self,b):
        #TODO implement function
        root=Node([self.index,b,self.value,self.h])
        self.nodes[0]=root
        self.index+=1
        self.h+=1

    def insert_node(self,parent,input):#value=[b,value,h]
        self.h=parent.h+1#neue ebene erstellen
        values=[self.index,parent,input[0],input[1],input[2]]
        self.nodes.append(Node(values))
        self.index+=1

    def findNode(self,index):
        return self.nodes[index]
    
    def delete_node(self,node):
        node.parent=None

    
