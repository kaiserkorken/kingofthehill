from pydoc import cli
import threading
import socket
from main import *
from bitboard import BoardtoFEN, FENtoBit, FENtoBoard
#TODO checkmate integrieren
#TODO zeitbegrenzung schicken
import logging
#logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.DEBUG)

format = "%(asctime)s: %(message)s"
logging.basicConfig(filename='server.conf',format=format, level=logging.DEBUG,datefmt="%H:%M:%S")
host = '127.0.0.1'
port = 59566
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []
plays=1
single=False
bild=False
answer=False
full=False
def run_gui():
    global bild
    global answer
    global single
    bild=GUI(False)
    while bild.running:
        if single:
            if answer!=False:
                board=FENtoBoard(answer)
                bild.draw(board)
                bild.player*=(-1)
                answer=False
                bild.single=True#spieler ist dran
                #bild.klick=True
            if bild.klick==True:
                #FENtoBit()
                FEN=BoardtoFEN(bild.gs.board,bild.player)
                #bild.player*=(-1)
                print("FEN; ",FEN)
                logging.info("Server    : sending FEN: "+FEN)
                broadcast(FEN)
                bild.single=False#spieler kann nicht mehr klicken, ki ist dran
                bild.klick=False
                
            bild.run()
        else:
            bild.run()
   


def broadcast(message):
    for client in clients:
        client.send(message.encode("utf-8"))
    logging.info("Server    : sending message: "+str(message))
    print("message:"+str(message))
# Function to handle clients'connections

     
def handle_client(client):
    global plays
    global full
    global answer
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message != "False":
                if (FENtoBit(message)):
                    plays+=1
                    print("Starte Runde "+str(plays))
                    logging.info("Server    : Starting round: "+str(plays))
                    if plays>=80:
                        message="remis"
                    else:
                        board=FENtoBoard(message)
                        bild.draw(board)
                        answer=message
                        
                broadcast(message)
                
        except Exception as e:
            print(e)
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the game!')
            bild.reset()
            logging.info("Server    : disconnected player: "+str(alias))
            aliases.remove(alias)
            full=False
            break
# Main function to receive the clients connection


def receive():
    global plays
    global bild
    global full
    global clients
    gui = threading.Thread(target=run_gui, args=())
    gui.start()
    if single==False:
        while True:
            print('Server is running and listening ... s')
            logging.info("Server    : Server is running in AI vs. AI mode ...")
            client, address = server.accept()
            logging.info("Server    : established connection with player:"+str(address))
            print(f'connection is established with {str(address)}')
            client.send('alias?'.encode('utf-8'))
            alias = client.recv(1024).decode("utf-8")
            aliases.append(alias)
            clients.append(client)
            client.send('you are now connected!'.encode('utf-8'))
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
            if len(clients) == 1:
                clients[0].send("1".encode("utf-8"))
            if len(clients) == 2:
                plays=1
                clients[1].send("-1".encode("utf-8"))
                broadcast("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                bild.reset()
                plays=0
                print("startet Runde "+str(plays))
                plays+=1
    else:
        while True:
            print('Server is running and listening ...')
            logging.info("Server    : Server is running in Single Mode...")
            client, address = server.accept()
            logging.info("Server    : established connection with player:"+str(address))
            print(f'connection is established with {str(address)}')
            client.send('alias?'.encode('utf-8'))
            alias = client.recv(1024).decode("utf-8")
            aliases.append(alias)
            clients.append(client)
            print(f'The alias of this client is {alias}'.encode('utf-8'))
            broadcast(f'{alias} has connected to the game, ')
            client.send('you are now connected!'.encode('utf-8'))
            if not full:
                bild.reset()
                thread = threading.Thread(target=handle_client, args=(client,))
                thread.start()
            if len(clients) == 1:
                clients[0].send("-1".encode("utf-8"))
                full=True
                plays=1
                bild.klick=False
                bild.single=True
                broadcast("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                bild.reset()
                bild.player=1
                plays=0
                print("startet Runde "+str(plays))
                plays+=1

if __name__ == "__main__":
    receive()

