# from anytree import NodeMixin, RenderTree

# class knoten(object):  # Just an example of a base class
#     foo=0

class Node(object):  # Add Node feature
    def __init__(self, index, parent, bitb, util, h, name, hash=None):
        # super(knoten, self).__init__()
        self.parent = parent
        # if children:
        #     self.children = children
        self.index = index
        self.b = bitb
        self.value = util
        self.h = h
        self.hash = hash
        self.name = name
        self.children = ()
        if self.parent != None:
            self.parent.children += self,
        # TODO aus bitboard rauslesen
        # self.name
        # self.name=value[4]

def partition(l, r, nums):
    # Last element will be the pivot and the first element the pointer
    pivot, ptr = nums[r][0], l
    for i in range(l, r):
        if nums[i][0] <= pivot:
            # Swapping values smaller than the pivot to the front
            nums[i], nums[ptr] = nums[ptr], nums[i]
            ptr += 1
    # Finally swapping the last element with the pointer indexed number
    nums[ptr], nums[r] = nums[r], nums[ptr]
    return ptr

def quicksort(l, r, nums):
    if len(nums) == 1:  # Terminating Condition for recursion. VERY IMPORTANT!
        return nums
    if l < r:
        pi = partition(l, r, nums)
        quicksort(l, pi - 1, nums)  # Recursively sorting the left values
        quicksort(pi + 1, r, nums)  # Recursively sorting the right values
    return nums

class Tree(object):
    def __init__(self, bb, starthash=False) -> None:
        self.nodes = []
        self.value = None
        self.root = Node(0, None, bb, self.value, 0, "Wstart", starthash)
        self.nodes.append(self.root)
        self.index = 1
        self.h = 1
        # self.children=None
        # self.name="root"
        # print(RenderTree(self.root))
        # self.node beinhaltet festen index, value und dict
        # node.value=value
        # node.h=height

    def insert_node(self, parent, bitb, util, h, name, hash=None):  # value=[index,b,value,h]
        # def insert_node(self,parent,input):#value=[index,b,value,h,name]
        self.h = parent.h + 1  # neue ebene erstellen
        new_node = Node(self.index, parent, bitb, util, h, name, hash)
        # print(parent.children)
        # parent.children+=(new_node,)
        self.nodes.append(new_node)
        self.index += 1
        return new_node

    def find_node(self, index):
        return self.nodes[index]

    def delete_node(self, node):
        node.parent = None

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
            # sortiere tupel x.children
            # if x.h%2==0:#max spieler
            #     x.children=sorted(x.children,reverse=True)#TODO implement eigene schnellere sortieragorithmen
            # else: #min spieler
            #     x.children=sorted(x.children)
            oldchilds = x.children
            values = []
            for index, z in enumerate(x.children):
                values.append((z.value, index))

            quicksort(0, len(values) - 1, values)

            #for i in range(len(values)):
            #    min_idx = i
            #    for j in range(i + 1, len(values)):
            #        if values[i][0] > values[j][0]:
            #            min_idx = j
            #            values[i], values[min_idx] = values[min_idx], values[i]

            # if x.h%2==0:#max spieler
            #     values=sorted(values,reverse=True)#TODO implement eigene schnellere sortieragorithmen
            # else: #min spieler
            #     values=sorted(values)
            # del x.children
            x.children = []
            for y in values:
                x.children += (oldchilds[y[1]],)
            x.children = list(x.children)

