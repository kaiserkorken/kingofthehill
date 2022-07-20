#from http.client import responses
from re import T
from player import *
#from tt import ttable
#from json import *
import asyncio
from websockets import connect
import time

class Game(Player):
    def __init__(self,websocket, current=1):
        super().__init__(current)
        self.name="gruppeAN"+str(current)
        self.ID=48265171
        self.playertype=0
        self.stage=1
        self.websocket=websocket
        self.zug=False
        self.look=False
    def step(self):
        return 0
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
                try:#falls currentPlaer leer
                    self.zug=self.ID==d["currentPlayer"]["playerID"]
                except:
                    self.zug=False
                self.fen=d["fen"]
                if self.zug:
                    try:
                        self.t=d["timeLeft"][self.playertype]
                    except:
                        self.t=20;
            self.gameID=d["ID"]
            if len(d["activePlayerList"])<2:
                return "empty"
            return True
        else:
            return False
    def join(self):
        a=["type","3","username",self.name,"playerID",self.ID,"joinAsPlayer","1","gameID",self.gameID]
        return a
    def move(self):
        move=self.turn(self.fen,self.t,name=True)
        if move ==False:
            move= self.turn(self.fen,t=0,name=True)
        self.fen=move
        data=["type","4","username",self.name,"playerID",self.ID,"gameID",self.gameID,"move",self.fen]
        return data
    # message= "{"type":"0","stamp?=""}"
   

    def message(self,type,stamp=""):
        di= dict()
        di["type"]=type
        
        self.stamp=time.time()
        di["stamp?"]=self.stamp
        #str="\"type\":{},\"stamp?\":{}".format(type,stamp)
        str=json.dumps(di)
        return str
            
    def login(self):
        # str=message(0)[:-1]
    
        # str=str+"username:{},playerID?:{}".format(name,int(ID))+"}"
        # return str
        di= dict()
        di["type"]=0
        di["username"]=self.name
        di["playerID"]=self.ID
        self.stamp=time.time()
        di["stamp?"]=self.stamp
        #str="\"type\":{},\"stamp?\":{}".format(type,stamp)
        str=json.dumps(di)
        return str
    def messaging(self,dic):
        # m=""
        d=dict()
        for x in range(0,len(dic)-1,2):
            d[dic[x]]=dic[x+1]
        self.stamp=time.time()
        dic["stamp?"]=self.stamp    
        return json.dumps(d)

async def hello(uri):
    async with connect(uri) as websocket:
        try:
            game=Game(websocket,current=0)#player 1
            resp="{\"type\":\"-1\"}"
            data=response(resp)
            error= await handle(data,game)
            if error==False:
                return True
            print("error: "+game.messaging(error))
        except:
            game=Game(websocket)#player 2
            resp="{\"type\":\"-1\"}"
            data=response(resp)
            error= await handle(data,game)
            if error==False:
                return True
            print("error: "+game.messaging(error))
        #return False
        #game zu ende
        
        #game.reset()
    print("connection lost")
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

async def handle(resp,game):
    data=int(resp["type"])
    count=0
    
    while( count<=5):# mehr als 5 mal in folge fehler -> abbruch
        while(data<0 or data>4):#fehler -> nochmal versuchen
            if data>4:#nachricht nicht an uns/irrelevant
                count-=1
                if data==8: #game started
                    game.zug=True
            if count >=5:
                return data
            if game.stage==3:
                if(data<=-5):#sonstige fehlerbehandlung
                    return data#create game hat nicht funktioniert
            if game.stage==2:
                if(data==-10):#kein game mehr zum joinen
                    break
                elif(data==-11):#game started
                    break
                
                count-=1
            
            resp= await sending(game)
            if resp=="over":
                return False
            data=response(resp)["type"]
            count+=1
        count=0
        if game.stage==2 and data!=-10:#join erfolgreich -> move
            game.stage+=1 
        if game.stage<4:# or game.zug:
            game.stage+=1
            #game.zug=False
            
        resp= await sending(game)
        data=response(resp)["type"]
        if resp=="over":
                return False

    return resp

        #TODO type 6, tournament started, type 8, game started
        #do reset
        
async def getinfo(game, new=False):#aktualisiere aktuelle game infos
    await game.websocket.send(game.message(1))
    resp= await game.websocket.recv()
    data= response(resp)
    while (data["type"]!=1):
        if data["type"]!=8:
            print("wrong recv")
            resp= await game.websocket.recv()
            data= response(resp)
        else:
            if new:
                return "ready"
    return game.info(data,new)

    
async def sending(game):
        if game.stage==1:#login
                print("login")
                await game.websocket.send(game.messaging(game.login()))
                
        elif game.stage==2:#join game
            print("join game")
            x= await getinfo(game,new=True)
            if x==True:
                await game.websocket.send(game.messaging(game.join()))
                game.playertype=1
            elif x=="ready":
                d=dict()
                d["type"]=-10#no game found
                d["type"]=-11#game automatically initiated
                return d

        elif game.stage==3:#create game
            
            print("create game")
            #x= await getinfo(game)
            await game.websocket.send(game.messaging(game.create())) 
            game.playertype=0
            game.stage-=2#wieder joinen
        
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
                if x=="empty":
                    print("no player joined yet")   
            z= game.messaging(game.move())
            print(z)
            await game.websocket.send(z)
          
        
        
        resp= await game.websocket.recv()
        data= response(resp)
        
        while (data["type"]==4 and data["activePlayerList"]["playerID"]!=game.ID):#nicht an uns
            print("wrong recv")
            resp= await game.websocket.recv()
            data= response(resp)
        return data
        
asyncio.run(hello("ws://koth.df1ash.de:8026"))
#asyncio.run(hello("ws://chess.df1ash.de:8025"))