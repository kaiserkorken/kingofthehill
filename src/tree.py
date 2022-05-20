from re import M
from tkinter.messagebox import NO
from anytree import NodeMixin, RenderTree

class knoten(object):  # Just an example of a base class
    foo=0
        
class Node(knoten, NodeMixin):  # Add Node feature
    def __init__(self, value, parent=None, children=None):
        super(knoten, self).__init__()
        self.parent = parent
        if children:
            self.children = children
        self.values=value
        self.index=value[0]
        self.b=value[1]
        self.value=value[2]
        self.h=value[3]
class Tree(object):
    def __init__(self,bb) -> None:
        self.nodes=[]
        self.value=None
        self.root=Node([0,bb,None,0])
        self.nodes.append(self.root)
        self.index=1
        self.h=1
        #print(RenderTree(self.root))
        #self.node beinhaltet festen index, value und dict
        #node.value=value
        #node.h=height

    def generate_search_tree(self,b, player):
        # generate a searchtree and search for possible pseudolegal moves
        moves = Node('root')
        
        return moves

    def insert_node(self,parent,input):#value=[index,b,value,h]
        self.h=parent.h+1#neue ebene erstellen
        values=[self.index,input[0],input[1],input[2]]
        new_node=Node(values,parent)
        #print(parent.children)
        #parent.children+=(new_node,)
        self.nodes.append(new_node)
        self.index+=1

    def find_node(self,index):
        return self.nodes[index]
    
    def delete_node(self,node):
        node.parent=None

    def print_tree(self):
        print("tree:")
        for pre, fill, node in RenderTree(self.root):
            print((u"%s%s"%(pre,node.index)).ljust(8),node.value,node.h)





            
