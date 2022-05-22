import threading
import socket

from bitboard import FENtoBit
host = '127.0.0.1'
port = 59566
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []
plays=1


def broadcast(message):
    for client in clients:
        client.send(message.encode("utf-8"))
    print("message:"+str(message))
# Function to handle clients'connections


def handle_client(client):
    global plays
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message != "False":
                if (FENtoBit(message)):
                    plays+=1
                    print("Starte Runde "+str(plays))
                    if plays>=80:
                        message="remis"

                broadcast(message)
                

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the game!')
            aliases.remove(alias)
            break
# Main function to receive the clients connection


def receive():
    global plays
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode("utf-8")
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the game, ')
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        if len(clients) == 1:
            clients[0].send("1".encode("utf-8"))
        if len(clients) == 2:
            plays=1
            clients[1].send("-1".encode("utf-8"))
            broadcast("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            print("startet Runde "+str(plays))
            plays+=1


if __name__ == "__main__":
    receive()

