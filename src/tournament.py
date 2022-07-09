from http.client import responses
from player import *
#from tt import ttable
#from json import *
import asyncio
from websockets import connect

class Game(Player):
    def __init__(self,websocket, current=1):
        super().__init__(current)
        self.name="GruppeAN"
        self.ID=48265171
        self.playertype=0
        self.stage=1
        self.websocket=websocket
        self.zug=False
        self.look=False
    def step(self):
        return 0
    def login(self):
        self.ID=random.randint(0,99999999)
        data=["type","0","username",self.name,"playerID",self.ID]
        return data
    def create (self):
        data=["type","2","username",self.name,"playerID",self.ID]
        return data
    
    def info(self, data,new=True):
        d=[]
        if not new:# find first game with less than 2 player
            for x in data["games"]:
                if len(x["activePlayerList"])<2:
                    d=x
                    break
        else:
            for x in data["games"]:
                if x["ID"]==self.gameID:
                    d=x
                    break
            
        
        #data=response(resp)
        if d!=[]:
            if d["over"]:
                return "over"
            if len(d["activePlayerList"])>0:
                self.zug=self.ID==d["currentPlayer"]["playerID"]
                self.fen=d["fen"]
                if self.zug:
                    self.t=d["timeLeft"][self.playertype]
            self.gameID=d["ID"]
           
            return True
        else:
            return False
    def join(self):
        a=["type","3","username",self.name,"playerID",self.ID,"joinAsPlayer","1","gameID",self.gameID]
        return a
    def move(self):
        move=self.turn(self.fen,self.t)
        if move ==False:
            move= self.turn(self.fen,t=0)
        data=["type","4","username",self.name,"playerID",self.ID,"gameID",self.gameID,"move",move]
        return data
    # message= "{"type":"0","stamp?=""}"
def response(message):
    dic = message
    if type(message)!=dict:
        dic=json.loads(message)
    # message=message.replace("\"","")
    # message=message[1:-1]
    # message= message.split(",")
    # dic=dict()
    # s=[]
    # for x in range(0,len(message)):
    #     s.append(message[x].split(":"))
    # for y in range(len(s)):
    #     dic[s[y][0]]=s[y][1]
    return dic

def message(type,stamp=""):
    di= dict()
    di["type"]=type
    di["stamp?"]=""
    #str="\"type\":{},\"stamp?\":{}".format(type,stamp)
    str=json.dumps(di)
    return str
        
def login(name,ID=""):
    # str=message(0)[:-1]
   
    # str=str+"username:{},playerID?:{}".format(name,int(ID))+"}"
    # return str
    di= dict()
    di["type"]=0
    di["username"]=name
    di["playerID"]=ID
    #str="\"type\":{},\"stamp?\":{}".format(type,stamp)
    str=json.dumps(di)
    return str
def messaging(dic):
    # m=""
    d=dict()
    for x in range(0,len(dic)-1,2):
         d[dic[x]]=dic[x+1]
    return json.dumps(d)

async def hello(uri):
    async with connect(uri) as websocket:
        game=Game(websocket)
        resp="{\"type\":\"-1\"}"
        data=response(resp)
        error= await handle(data,game)
        if error==False:
            return True
        print("error: "+error)
        #return False
        #game zu ende
        
        #game.reset()
    print("connection lost")

async def handle(data,game):
    data=int(data["type"])
    count=0
    wait=True
    while( count<=5):# mehr als 5 mal in folge fehler -> abbruch
        while(data<0 or data>4):#fehler -> nochmal versuchen
            if data>4:#nachricht nicht an uns/irrelevant
                count-=1
                if data==8: #game started
                    wait=False
            if count >=5:
                return data
            if game.stage==3:
                if(data<=-5):#sonstige fehlerbehandlung
                    return data#create game hat nicht funktioniert
            if game.stage==2:
                if(data<=-10):#kein game mehr zum joinen
                    break
                count-=1
            
            resp= await sending(game)
            if resp=="over":
                return False
            data=response(resp)["type"]
            count+=1
        count=0
        if game.stage<4 or not wait:
            game.stage+=1
            wait=True
            
        resp= await sending(game)
        data=response(resp)["type"]
        if resp=="over":
                return False

    return data

        #TODO type 6, tournament started, type 8, game started
        #do reset
        
async def getinfo(game, new=True):#aktualisiere aktuelle game infos
    await game.websocket.send(message(1))
    resp= await game.websocket.recv()
    data= response(resp)
    while (data["type"]!=1):
        print("wrong recv")
        resp= await game.websocket.recv()
        data= response(resp)
    return game.info(data,new)

    
async def sending(game):
        if game.stage==1:#login
                print("login")
                await game.websocket.send(messaging(game.login()))
                
        elif game.stage==2:#create game
            print("join game")
            x= await getinfo(game,new=False)
            if x!=False:
                await game.websocket.send(messaging(game.join()))
                game.playertype=1
            else:
                d=dict()
                d["type"]=-10#no game found
                return d

        elif game.stage==3:#join game
            print("create game")
            await game.websocket.send(messaging(game.create())) 
            game.playertype=0
        
        elif game.stage==4:#make move
            print("move")
            x= await getinfo(game)
            while not game.zug:
                x= await getinfo(game)
                if x==False:
                    print("Keinem Spiel verbunden")
                if x=="over":
                    print("spiel zu ende")    
                    return "over"                
            await game.websocket.send(messaging(game.move()))
          
        
        
        resp= await game.websocket.recv()
        data= response(resp)
        
        while (data["type"]==4 and data["playerID"]!=game.ID):#nicht an uns
            print("wrong recv")
            resp= await game.websocket.recv()
            data= response(resp)
        return data
        
asyncio.run(hello("ws://koth.df1ash.de:8026"))
#asyncio.run(hello("ws://chess.df1ash.de:8025"))