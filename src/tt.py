##implements transposition tables and saves them to files##
#https://numpy.org/doc/stable/reference/generated/numpy.memmap.html
#TODO hashes speichern, depth dazuschreiben
import hashlib
import random
from bitboard import *
import json
import sys
# try: 
#     import cpickle as pickle
    
# except:
#     import pickle
# import mpu


class ttable(object):
    def __init__(self,location="table",open=False,bits=False):
        random.seed()
        self.bits=64
        if bits:
            self.bits=bits
            
        self.location=location#TODO auf syntax checken
        if location=="table" and open:
            self.location="opening"
        self.file=self.location
        self.open=open
        #self.file=path.join(mkdtemp(),self.location)
        #random.getstate()
        #print(self.rand)
        
        self.location+=".json"#".npy"
        #else:
      
        b = init_game()#TODO wrong start board, missing black tokens
        self.starthash = 0
        if open ==False:
            self.init_hash(b)
        # if not self.init_hash(b):
        #     return False
        #print(hashValue)
        #print("hash in table?:")
        #self.table=self.create_table(self.bits)
        try:
            print("loading")
            self.table=self.load_table()
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
            print("create new")
            self.table=self.create_table()
        

        if self.starthash:
            #print((2**32)-self.starthash)
            #print(self.table[(2**self.bits)-self.starthash])
            self.to_table(self.starthash,0,-1)
            #self.table[(2**self.bits)-self.starthash]=[0,-1]
            #print(self.table[(2**self.bits)-self.starthash])
        #self.save_table(self.table)#?
        #self.table=self.load_table()#TODO datei bereits vorhanden checken
    
    def init_hash(self,b):
        self.starthash=self.hash_value(b)

    def create_table(self):
    
        #table=np.arange(2**bits-1)
        #table.fill(0.0001)
        #table=np.full_like(2**bits-1,None)
        #table[]=None
        #table=np.full(2**bits-1,None) #ValueError: Maximum allowed dimension exceeded
    
        #table = np.memmap('test.mymemmap', dtype="int16", mode='w+', shape=(2000,2),offset=2*16/8)#maximal 65535
        #if self.dict:
        self.table=dict()
        with open(self.location, 'w+') as outfile:
            data=json.dump(self.table, outfile)
            #np(self.file, dtype='int8', mode='w+', shape=(2**self.bits-1,2))
            #alternativ numpy structured array
        #else:
            #self.table= np.memmap(self.file, dtype='int8', mode='w+', shape=(2**self.bits-1,2))
        #32 bit:4294967295, 16bit: 65535, 64 bit 18446744073709551615
        return self.table


    def set_location(self,location):
        self.location=location

    def save_table(self,location=False):
        # st=self.location
        # if location != False:
        #     st=location
        # np.save(st,self.table)
        #if self.dict:
            
        self.table= dict(self.table)
        #string=json.dumps(self.table)
        # with open(self.location, 'wb') as handle:
        #     pickle.dump(self.table, handle, protocol=pickle.HIGHEST_PROTOCOL)

        #mpu.io.write(self.location, self.table)
        

        with open(self.location, 'w+') as outfile:
            data=json.dump(self.table, outfile)
            #outfile.write(string)
                
            # dtype= dict(names=["id","value","depth"],formats=["f8","f8","f8"])
            # self.table=np.array(list(self.table),dtype=dtype)
            # np.save(self.location,self.table,allow_pickle=True)
        #else:
            #self.table.flush()

    def load_table(self):
        #if self.dict:
        # with open(self.location, 'rb') as handle:
        #     content = pickle.load(handle)
        #self.table = mpu.io.read(self.location)
        with open(self.location, 'r') as j:
            content = json.loads(j.read())   
        self.table=content
        #else:
            #self.table= np.memmap(self.file, dtype='int8', mode='r+', shape=(2**self.bits-1,2))
        
        return self.table

    def in_table(self,hash,h=False):
        #if self.dict:
        try:
            value=self.table[str(hash)]
        except:
            return []
        #else:
            #value=self.table[hash]
        if not open:
            depth=value[1]
            #if depth!=0:#depth ungleich 0 (sonst nicht initialisiert)
            if h<=depth:#aelterer wert bereits sicherer(tiefer)
                return value
        else:
            return value
        #print(value)
        #print(h,depth)
        return []
        
        4294967295
    def to_table(self,hash,value,depth=None):
        #if self.dict:
        if len(self.table)<=588823529:#-> kleiner 2 GB
            if not open:
                self.table[str(hash)]=[int(value),int(depth)]
            else:
                self.table[str(hash)]=value
        else:
            return False
            
        # else:
        #     self.table[hash]=[value,depth]

    def hash_value(self,b,x=None,y=None,token=None):#to = [pos x, pos y, "K"], deshalb von vorteil: node.name -> a1a2K=to
        byt=BittoByte(b,x)
        byt=byt.encode("utf-8")
        hash=(hashlib.sha256(byt).hexdigest(), 16)
        #print (hash[0])
        #hash=hash[0].decode("utf-8")
        return hash[0]#BittoFEN(b))#hash=b#x=Player
      
    def loadtxt(self):
        leere=[]
        with open('ULTRAMEGA.txt',"r") as f:
            mylist = f.read().splitlines()
        for x in range(len(mylist)):
            z=mylist[x].split(";")[0].split(" ")
            mylist[x]=" ".join(z[0:4])
        
        true=np.empty(len(mylist),dtype=bool)
        for x in range(1,len(mylist)):
            byt=FENtoBit(mylist[x-1],True)
            if byt!=False:
                hash=self.hash_value(byt[0],byt[1])#mylist[x-1])#
                leere.append([hash,mylist[x]])
                true[x-1]=True
            else:
                true[x-1]=False
            
        for y in range(len(leere)):
            # if (y%1500==0):
            #     self.save_table()
            if true[y]:
                hash=leere[y][0]
                arr=self.in_table(hash)
                if len(arr)==0:
                    self.to_table(hash,[leere[y][1]])
                else:
                    if arr[0]!=leere[y][1]:
                        arr.append(leere[y][1])
                        self.to_table(hash,arr)
               
        self.save_table("opening.json")

    
# class recursion_depth:
#     def __init__(self, limit):
#         self.limit = limit
#         self.default_limit = sys.getrecursionlimit()
#     def __enter__(self):
#         sys.setrecursionlimit(self.limit)
#     def __exit__(self, type, value, traceback):
#         sys.setrecursionlimit(self.default_limit)
if __name__ == "__main__":
   # with recursion_depth(3000):
        #tt=ttable("testtable.mymemmap")
        #tt.create_table()
        #print(tt.in_table(569765))
        # tt=ttable("testtable",dict=True)
        # if tt.starthash:
        #     tt.to_table(569765,127,9)#hier utility einsetzen
        #     print(tt.in_table(569765,1))
        #     print("save table")
        #     tt.save_table()
        #     del tt.table
        #     tt.table=tt.load_table()
        #     #table=tt.load_table()
        #     print(tt.in_table(569765,1))
        #     #print(tt.in_table(3531))
        tt=ttable("opening",open=True)
        tt.loadtxt()
            

        ### minimax implementation (Pseudocode): ### 
        # hash=tt.hash_value(parenthash,[x,y,"K"] bzw. "a1a2K")
        # new=tt.in_table(hash)
        # if not new:
        #     new=utility()
