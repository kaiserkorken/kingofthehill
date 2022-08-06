from player import *
#from tt import ttable
#from json import *
import asyncio
from websockets import connect

#play=0


class Game(Player):
    def __init__(self,websocket, current=0,alone=False):
        super().__init__(current)
        self.name="gruppeAN"
        if current>0:
            self.name+=str(current)
        self.ID=48265171+current
        self.playertype=0
        self.stage=1
        self.websocket=websocket
        self.zug=False
        self.check=False
        #self.look=False
        self.started=False
        self.alone=True
    def step(self):
        return 0
    def create (self):
        data=["type","2","username",self.name,"playerID",self.ID]
        return data
    
    def info(self, data, new=False):
        d=[]
        #if new:# find first game with less than 2 player
        
        for x in data["games"]:
            p=0
            for y in x["activePlayerList"]:
                
                if y["playerID"]==self.ID:
                    self.playertype=p
                    self.current=-1
                    if p!=1:
                        self.current=1
                    if not x["over"]:
                        self.gameID=x["ID"]
                        self.fen=x["fen"]
                    else:
                        return "over"
                    if new:
                        return "already"#bereits einem game zugeweisen
                    d=x
                    break
                p+=1
        if self.alone:
            if d==[]: #join new game
                for x in data["games"]:        
                    if len(x["activePlayerList"])<2 and new:
                        self.gameID=x["ID"]
                        self.fen=x["fen"]
                        return True
                        d=x
                        break
            # else:
            #     for x in data["games"]:
            #         if x["ID"]==self.gameID:
            #             d=x
            #             break
            # if new:
            #     self.gameID=d["ID"]
            #     self.fen=x["fen"]
            #     return True
            
            #data=response(resp)
        if d!=[]:
            if d["over"]:
                return "over"
            if len(d["activePlayerList"])>0:
                try:#falls currentPlaer leer
                    self.zug=self.ID==d["currentPlayer"]["playerID"]
                    
                except:
                    self.zug=False
                self.check=d["check"]
                if self.zug and len(d["activePlayerList"])==d["maxPlayerNumber"]:
                    self.started=True
                fen=d["fen"]
                if fen!="":
                    self.fen=fen
                #if self.zug:
                try:
                    self.t=d["timeLeft"][self.playertype]/(60-len(d["moveHistory"]))#wenn zeitlimit gesetzt max zeit durch predicted anzahl an moves teilen
                    print("timeleft: "+str(self.left))
                except:
                    self.t=2
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
        move=self.do_move(self.fen,self.t,self.tt,name=True)
        #TODO: richtig aus schach moven
        # zuege vorher ausschliessen und moveliste returnen -> nicht neu berechnen 
        if move ==False:
            move= self.do_move(self.fen,0,self.tt,name=True)
        #self.fen=move
        data=["type","4","username",self.name,"playerID",self.ID,"gameID",self.gameID,"move",move]
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
        di["stamp"]=self.stamp
        #str="\"type\":{},\"stamp?\":{}".format(type,stamp)
        #str=json.dumps(di)
        return di
    def messaging(self,dic):
        # m=""
        if type(dic)!=dict:
            d=dict()
            for x in range(0,len(dic)-1,2):
                d[dic[x]]=dic[x+1]
            self.stamp=time.time()
            if d.get("stamp")==None:
                d["stamp"]=self.stamp    
        else:
            d=dic
        x=json.dumps(d)
        print(x)
        return x

async def hello(uri,play):
    async with connect(uri) as websocket:
        #try:
            game=Game(websocket,current=play)#player 1
            resp="{\"type\":\"-1\"}"
            data=response(resp)
            error= await handle(data,game)
            game.close()
            if error==False:
                return True
            print("error: "+str(error))
        # except:
        #     game=Game(websocket)#player 2
        #     resp="{\"type\":\"-1\"}"
        #     data=response(resp)
        #     error= await handle(data,game)
        #     if error==False:
        #         return True
        #     print("error: "+str(error))
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
            
            print("error: ")
            game.messaging(resp)
            if data==8:#game started
                game.started=True
                game.stage=4#move stage
            if data>4:#nachricht nicht an uns/irrelevant
                count-=1
                #if data==8: #game started
                    #game.zug=True
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
                if not game.alone:#wenn tournament, search new game
                    game.stage=2
                    game.fen=None
                    game.gameID=None
                else:
                    return False
                break
            data=response(resp)["type"]
            
            count+=1
        count=0
        if game.stage==4:#move erfolgreich
            game.reset()#letztes ergebnis resetten
        if game.stage==2 and data!=-10:#join erfolgreich -> move
            game.stage+=1 
        if game.stage<4:# or game.zug:
            game.stage+=1
            #game.zug=False
        if resp=="over":
            if not game.alone:#wenn tournament, search new game
                    game.stage=2
                    game.fen=None
                    game.gameID=None
            else:
                return False    
        resp= await sending(game)
        data=response(resp)["type"]
        

    return resp

        #type 6, tournament started, type 8, game started
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
            game.started=True
    return game.info(data,new)

    
async def sending(game):

        if game.stage==1:#login
                print("login")
                
                await game.websocket.send(game.messaging(game.login()))
                
        elif game.stage==2:#join game
            print("join game")
            x= await getinfo(game,new=True)
            if game.alone:
                if x==True:
                    await game.websocket.send(game.messaging(game.join()))
                    #game.playertype=1
                elif x=="ready" or x==False:
                    d=dict()
                    d["type"]=-10#no game found
                    return d
            if x=="already":
                d=dict()
                d["type"]=-11#game automatically initiated
                return d

        elif game.stage==3:#create game
            
            print("create game")
            #x= await getinfo(game)
            z= game.messaging(game.create())
            #print(z)
            await game.websocket.send(z)
            #game.playertype=0
            game.stage-=2#wieder joinen
        
        elif game.stage==4:#make move
            print("move")
            x= await getinfo(game)
            while not game.zug or not game.started:
                x= await getinfo(game)
                if x==False:
                    print("Keinem Spiel verbunden")
                elif x=="over":
                    print("spiel zu ende")    
                    return "over" 
                elif x=="empty":
                    print("no player joined yet")  
                elif game.zug==False:
                    print("not our turn")
                time.sleep(2)
            z= game.messaging(game.move())
            #print(z)
            game.zug==False
            await game.websocket.send(z)
          
        
        
        resp= await game.websocket.recv()
        data= response(resp)
        
        while (data.get("type")==None and data.get("ID")!=game.ID):#nicht an uns#data.get("type")==4 and 
            print("wrong recv")
            resp= await game.websocket.recv()
            data= response(resp)
        return data
        
#asyncio.run(hello("ws://koth.df1ash.de:8026",0))
#asyncio.run(hello("ws://koth.df1ash.de:8026",2))
#asyncio.run(hello("ws://koth.df1ash.de:8026",1))

asyncio.run(hello("ws://chess.df1ash.de:8025",1))