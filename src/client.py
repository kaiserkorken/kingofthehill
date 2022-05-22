import threading
import socket
from player import *
alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59566))
startFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
player = Player()
win = True

def client_receive():
    while True:
        #try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            elif message =="1":
                print("Sie spielen Weiß!")
                player.current=1

            elif message == "-1":
                print("Sie spielen Schwarz!")
                player.current=-1
            elif FENtoBit(message):
                if not checkmate(message,player):
                    turn = player.turn(message)
                    client.send(turn).encode('utf-8')
                elif checkmate(message,player):
                    win = False
                    client.send(f'{alias}: has lost the game!!'.encode('utf-8'))
                    client.close()
            elif message.split(" ")[2] == "lost":
                if win:
                    print(f'{alias}: has won the game!!')
            else:
                print(message)

        # except:
        #     print('Error!')
        #     client.close()
        #     break


def client_send():
    while True:
        bsp= "9999888766"
        message = bsp
        time.sleep(1)
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

#send_thread = threading.Thread(target=client_send)
#send_thread.start()

# spielerunterscheidung
# FENTOBIT unterscheidung
# Schachunterscheidung

