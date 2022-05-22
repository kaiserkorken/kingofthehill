import socket 
import threading
from player import *
host = '127.0.0.1'
port = 59455
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []


def broadcast(message):
    for client in clients:
        client.send(message)

# Funktion für die Clients Connection


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the game!'.encode('utf-8'))
            aliases.remove(alias)
            break
# Funktion um die Nachrichten der Clients zu empfangen


def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the game'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()

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
