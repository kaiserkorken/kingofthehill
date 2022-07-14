#from anytree import NodeMixin, RenderTree

# class knoten(object):  # Just an example of a base class
#     foo=0
        
class Node(object):  # Add Node feature
    def __init__(self, index,parent,bitb,util,h,name,hash=None):
        #super(knoten, self).__init__()
        self.parent = parent
        # if children:
        #     self.children = children
        self.index=index
        self.b=bitb
        self.value=util
        self.h=h
        self.hash=hash
        self.name=name
        self.children=()
        if self.parent != None:
            self.parent.children+=self,
        #TODO aus bitboard rauslesen
        #self.name
        #self.name=value[4]
class Tree(object):
    def __init__(self,bb,starthash=False) -> None:
        self.nodes=[]
        self.value=None
        self.root=Node(0,None,bb,self.value,0,"Wstart",starthash)
        self.nodes.append(self.root)
        self.index=1
        self.h=1
        #self.children=None
        #self.name="root"
        #print(RenderTree(self.root))
        #self.node beinhaltet festen index, value und dict
        #node.value=value
        #node.h=height

    def insert_node(self,parent,bitb,util,h,name,hash=None):#value=[index,b,value,h]
    #def insert_node(self,parent,input):#value=[index,b,value,h,name]
        self.h=parent.h+1#neue ebene erstellen
        new_node=Node(self.index,parent,bitb,util,h,name,hash)
        #print(parent.children)
        #parent.children+=(new_node,)
        self.nodes.append(new_node)
        self.index+=1
        return new_node

    def find_node(self,index):
        return self.nodes[index]
    
    def delete_node(self,node):
        node.parent=None

    # def print_tree(self):
    #     print("tree:")
    #     for pre, fill, node in RenderTree(self.root):
    #         print((u"%s%s"%(pre,node.name)).ljust(8),node.value,node.h)
    #         # print((u"%s%s"%(pre,node.name)).ljust(8),node.value,node.h)
    # def print_node(self,node):
    #     print("node",node.index,": ")
    #     for pre, fill, n in RenderTree(node):
    #         print((u"%s%s"%(pre,n.name)).ljust(8),n.value,n.h)
    #         # print((u"%s%s"%(pre,node.name)).ljust(8),node.value,node.h)
    def sort_nodes(self):
        for x in self.nodes:
            #sortiere tupel x.children
            # if x.h%2==0:#max spieler
            #     x.children=sorted(x.children,reverse=True)#TODO implement eigene schnellere sortieragorithmen
            # else: #min spieler
            #     x.children=sorted(x.children)
            oldchilds=x.children
            values=[]
            for index, z in enumerate(x.children):
                values.append((z.value,index))
                
            if x.h%2==0:#max spieler
                values=sorted(values,reverse=True)#TODO implement eigene schnellere sortieragorithmen
            else: #min spieler
                values=sorted(values)
            del x.children
            x.children=[]
            for y in values:
                x.children+=(oldchilds[y[1]],)
            x.children=list(x.children)
            
