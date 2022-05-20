import socket 
import threading
from player import *

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            #aktueller spieler: player[x] # x ist 0 or 1
            #if msg is FEN and player[x] =player[x].current: #FEN ist angekommen von Spieler der dran war
            #FEN=FENtoBit(msg)
            #   if checkmate(FEN,player):#spiel beendet
            #       -->player.current bzw. anderer hat verloren
            #       -->print("Player "+player.index(player[x])+" hat gewonnen!")
            #       -->for z in player:
            #           if z==x:
            #               z.__set__("win")
            #           else:
            #               z.__set__("lose")
            #           player.remove(z)
            #   elif FENtoBit(msg,True)[1]==player[x].current:
            #       FEN=player[x].turn()
            #       conn.send(FEN.encode(FORMAT))
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    #player=[]
    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #player.append(Player())
        #jeder connection einen player() zuweisen
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()