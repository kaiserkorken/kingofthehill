import threading
import socket
alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59566))



def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            elif message =="1":
                print("Sie spielen Weiß!")
                est = "etwas"
                client.send(est.encode('utf-8'))
            elif message == "-1":
                print("Sie spielen Schwarz!")
                est = "etwas"
                client.send(est.encode('utf-8'))
                #client send
    #        elif message == "Checkmate!":
    #            print("You have won the game")
    #            client.close()
    #        elif message.split(" "[0]=="FEN"):
    #            sgh = neuerMove(message.split(" ")[1],message.split(" ")[2])
    #            client.send(sgh.encode('utf-8'))
    #        elif checkmate(message.split(" ")[1],message.split(" ")[2]):
    #            client.send(f'{alias}: has won the game!!')
    #            client.close()
            else:
                print(message)

        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = input("")
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()

def neuerMove(bitbrd,player):
    pass

def checkmate():
    pass
