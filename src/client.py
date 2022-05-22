import threading
import socket
import time

alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59455))

#Mögliche Lösung, rückgabewert zu speichern
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            counter = int(message)+1
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
                return message
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        msg = alias +" says: Test1"
        message = msg.encode('utf-8')
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (1024 - len(send_length))
        client.send(send_length)
        client.send(message)
        time.sleep(1)


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()

