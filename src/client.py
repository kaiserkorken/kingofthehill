import threading
import socket
from player import *
from tt import ttable
alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59566))
startFEN = "rnb1kbnr/p4ppp/1p1pp3/2p3q1/3P4/NQP1PNPB/PP3P1P/R1B1K2R w"
#startFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
player = Player()
win = True


def client_receive():
    global win
    while True:
        #try:
            message = client.recv(1024).decode('utf-8')
            print("receive:"+str(message))
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            elif message =="1":
                print("Sie spielen Weiß!")
                player.current=1

            elif message == "-1":
                print("Sie spielen Schwarz!")
                player.current=-1
            elif FENtoBit(str(message)):
                if not checkmate(FENtoBit(message),player):
                    #turn = player.turn(message,3)
                    turn = player.turn(message)
                    print("Turn:"+str(turn))
                    client.send(str(turn).encode('utf-8'))
                else:
                    win = False
                    client.send(f'{alias}: has lost the game!!'.encode('utf-8'))
                    player.close()
                    client.close()
            elif len(message.split(" "))>2:#genug leerzeichen
                if message.split(" ")[2] == "lost":
                    if win:
                        print(f'{alias}: has won the game!!')
            elif message=="remis":
                print("Unentschieden!")
                win=False
                client.send(f'{alias}: has lost the game!!'.encode('utf-8'))
                player.close()
                client.close()
            else:
                print("else:"+str(message))

        # except:
        #      print('Error!')
        #      client.close()
        #      break


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

# message:r1b1k1r1/1pp1p3/3q2p1/p1n4p/4Q2P/NP1P1NP1/P2P1PB1/R1B4R B
# Starte Runde 39
# message:r1b1k1r1/1pp5/3qp1p1/p1n4p/4Q2P/NP1P1NP1/P2P1PB1/R1B4R W

# Starte Runde 2
# message:rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR B
# Starte Runde 3
# message:rnbqkbnr/ppp1pppp/8/3p4/8/2P5/PP1PPPPP/RNBQKBNR W
# Starte Runde 4
# message:rnbqkbnr/ppp1pppp/8/3p4/8/1QP5/PP1PPPPP/RNB1KBNR B
# Starte Runde 5
# message:rnbqkbnr/ppp1p1pp/5p2/3p4/8/1QP5/PP1PPPPP/RNB1KBNR W
# Starte Runde 6
# message:rnbqkbnr/ppp1p1pp/1Q3p2/3p4/8/2P5/PP1PPPPP/RNB1KBNR B
# Starte Runde 7
# message:rnbqkbnr/ppp1p1p1/1Q3p1p/3p4/8/2P5/PP1PPPPP/RNB1KBNR W
# Starte Runde 8
# message:rnbqkbnr/ppp1p1p1/1Q3p1p/3p4/2P5/8/PP1PPPPP/RNB1KBNR B
# Starte Runde 9
# message:rnbqkb1r/ppp1p1p1/1Q3p1p/3p4/2P5/8/PP1PPPPP/RNB1nBNR W
# Starte Runde 10
# message:rnbqkb1r/ppp1p1p1/1Q3p1p/3p4/2P5/1P6/P2PPPPP/RNB1nBNR B
# Starte Runde 11
# message:rnbqkbr1/ppp1p1p1/1Q3p1p/3p4/2P5/1P6/P2PPPPP/RNB1nBNR W
# Starte Runde 12
# message:rnbqkbr1/ppp1p1p1/5p1p/Q2p4/2P5/1P6/P2PPPPP/RNB1nBNR B
# Starte Runde 13
# message:rnbqkbr1/ppp1p1p1/5p1p/Q2p4/2P5/1P1n4/P2PPPPP/RNB2BNR W
# Starte Runde 14
# message:rnbqkbr1/ppp1p1p1/5p1p/Q2p4/2P5/1P1P4/P2P1PPP/RNB2BNR B
# Starte Runde 15
# message:rnbqkbr1/ppp1p3/5ppp/Q2p4/2P5/1P1P4/P2P1PPP/RNB2BNR W
# Starte Runde 16
# message:rnbqkbr1/ppp1p3/5ppp/Q2p4/2P5/1P1P2P1/P2P1P1P/RNB2BNR B
# Starte Runde 17
# message:r1bqkbr1/pppnp3/5ppp/Q2p4/2P5/1P1P2P1/P2P1P1P/RNB2BNR W
# Starte Runde 18
# message:r1bqkbr1/pppnp3/5ppp/1Q1p4/2P5/1P1P2P1/P2P1P1P/RNB2BNR B
# Starte Runde 19
# message:r1bqkbr1/pppnp3/5ppp/1Q6/2Pp4/1P1P2P1/P2P1P1P/RNB2BNR W
# Starte Runde 20
# message:r1bqkbr1/pppnp3/5ppp/1QP5/3p4/1P1P2P1/P2P1P1P/RNB2BNR B
# Starte Runde 21
# message:r1bqk1r1/pppnp1b1/5ppp/1QP5/3p4/1P1P2P1/P2P1P1P/RNB2BNR W
# Starte Runde 22
# message:r1bqk1r1/pppnp1b1/5ppp/1QP5/3p4/1P1P1NP1/P2P1P1P/RNB2B1R B
# Starte Runde 23
# message:r1bqk1r1/1ppnp1b1/5ppp/pQP5/3p4/1P1P1NP1/P2P1P1P/RNB2B1R W
# Starte Runde 24
# message:r1bqk1r1/1ppnp1b1/5ppp/pQP5/3p4/NP1P1NP1/P2P1P1P/R1B2B1R B
# Starte Runde 25
# message:r1bqkbr1/1ppnp3/5ppp/pQP5/3p4/NP1P1NP1/P2P1P1P/R1B2B1R W
# Starte Runde 26
# message:r1bqkbr1/1ppnp3/2Q2ppp/p1P5/3p4/NP1P1NP1/P2P1P1P/R1B2B1R B
# Starte Runde 27
# message:r1bqkbr1/1ppnp3/2Q2pp1/p1P4p/3p4/NP1P1NP1/P2P1P1P/R1B2B1R W
# Starte Runde 28
# message:r1bqkbr1/1ppnp3/5Qp1/p1P4p/3p4/NP1P1NP1/P2P1P1P/R1B2B1R B
# Starte Runde 29
# message:r1bqk1r1/1ppnp1b1/5Qp1/p1P4p/3p4/NP1P1NP1/P2P1P1P/R1B2B1R W
# Starte Runde 30
# message:r1bqk1r1/1ppnp1Q1/6p1/p1P4p/3p4/NP1P1NP1/P2P1P1P/R1B2B1R B
# Starte Runde 31
# message:r1bqk1r1/1pp1p1Q1/6p1/p1n4p/3p4/NP1P1NP1/P2P1P1P/R1B2B1R W
# Starte Runde 32
# message:r1bqk1r1/1pp1p3/6p1/p1n4p/3Q4/NP1P1NP1/P2P1P1P/R1B2B1R B
# Starte Runde 33
# message:r1b1k1r1/1pp1p3/3q2p1/p1n4p/3Q4/NP1P1NP1/P2P1P1P/R1B2B1R W
# Starte Runde 34
# message:r1b1k1r1/1pp1p3/3q2p1/p1n4p/3Q4/NP1P1NP1/P2P1PBP/R1B4R B
# Starte Runde 35
# message:r1b1k1r1/1ppnp3/3q2p1/p6p/3Q4/NP1P1NP1/P2P1PBP/R1B4R W
# Starte Runde 36
# message:r1b1k1r1/1ppnp3/3q2p1/p6p/3Q3P/NP1P1NP1/P2P1PB1/R1B4R B
# Starte Runde 37
# message:r1b1k1r1/1pp1p3/3q2p1/p1n4p/3Q3P/NP1P1NP1/P2P1PB1/R1B4R W
# Starte Runde 38
# message:r1b1k1r1/1pp1p3/3q2p1/p1n4p/4Q2P/NP1P1NP1/P2P1PB1/R1B4R B
# Starte Runde 39
# message:r1b1k1r1/1pp5/3qp1p1/p1n4p/4Q2P/NP1P1NP1/P2P1PB1/R1B4R W
# Starte Runde 40
# message:r1b1k1r1/1pp5/3qp1p1/p1n4p/3NQ2P/NP1P2P1/P2P1PB1/R1B4R B
# Starte Runde 41
# message:r1b1k1r1/2p5/1p1qp1p1/p1n4p/3NQ2P/NP1P2P1/P2P1PB1/R1B4R W
# Starte Runde 42
# message:r1b1k1r1/2p5/1p1qp1p1/p1n4p/3N3P/NP1P1QP1/P2P1PB1/R1B4R B
# Starte Runde 43
# message:r1b1k1r1/2p1q3/1p2p1p1/p1n4p/3N3P/NP1P1QP1/P2P1PB1/R1B4R W
# Starte Runde 44
# message:r1b1k1r1/2p1q3/1p2p1p1/p1n4p/3N3P/NP1P1QPB/P2P1P2/R1B4R B
# Starte Runde 45
# message:r1b1kqr1/2p5/1p2p1p1/p1n4p/3N3P/NP1P1QPB/P2P1P2/R1B4R W
# Starte Runde 46
# message:r1b1kqr1/2p5/1p2p1p1/p1n4p/3N3P/NP1P1QPB/P2P1P2/R1B3R1 B
# Starte Runde 47
# message:r1b1kq1r/2p5/1p2p1p1/p1n4p/3N3P/NP1P1QPB/P2P1P2/R1B3R1 W
# Starte Runde 48
# message:r1b1kq1r/2p5/1p2N1p1/p1n4p/7P/NP1P1QPB/P2P1P2/R1B3R1 B
# Starte Runde 49
# message:r1b1kq1r/2p5/1p2N1p1/p6p/7P/NP1n1QPB/P2P1P2/R1B3R1 W
# Starte Runde 50
# message:r1bNkq1r/2p5/1p4p1/p6p/7P/NP1n1QPB/P2P1P2/R1B3R1 B
# Starte Runde 51
# message:r1bNk2r/2p5/1p4p1/p4q1p/7P/NP1n1QPB/P2P1P2/R1B3R1 W
# Starte Runde 52
# message:r1bNk2r/2p5/1p4p1/p2Q1q1p/7P/NP1n2PB/P2P1P2/R1B3R1 B
# Starte Runde 53
# message:r1bNk2r/2p5/1p4p1/p2Qnq1p/7P/NP4PB/P2P1P2/R1B3R1 W
# Starte Runde 54
# message:r1b1k2r/1Np5/1p4p1/p2Qnq1p/7P/NP4PB/P2P1P2/R1B3R1 B
# Starte Runde 55
# message:r1b1k2r/1Np5/1p2q1p1/p2Qn2p/7P/NP4PB/P2P1P2/R1B3R1 W
# Starte Runde 56
# message:r1b1k2r/1Np5/1p2q1p1/Q3n2p/7P/NP4PB/P2P1P2/R1B3R1 B
# Starte Runde 57
# message:r1b1k2r/1Np5/1pn1q1p1/Q6p/7P/NP4PB/P2P1P2/R1B3R1 W
# Starte Runde 58
# message:r1b1k2r/1Np5/1Qn1q1p1/7p/7P/NP4PB/P2P1P2/R1B3R1 B
# Starte Runde 59
# message:r1b1k2r/1N6/1Qn1q1p1/2p4p/7P/NP4PB/P2P1P2/R1B3R1 W
# Starte Runde 60
# message:r1b1k2r/1N6/1Qn1q1p1/2p2B1p/7P/NP4P1/P2P1P2/R1B3R1 B
# Starte Runde 61
# message:r1b1k2r/1N6/1Q2q1p1/2p2B1p/1n5P/NP4P1/P2P1P2/R1B3R1 W
# Starte Runde 62
# message:r1b1k2r/1N6/1Q2q1p1/2p4p/1n5P/NP1B2P1/P2P1P2/R1B3R1 B
# Starte Runde 63
# message:r1b1k2r/1N6/1Qn1q1p1/2p4p/7P/NP1B2P1/P2P1P2/R1B3R1 W
# Starte Runde 64
# message:r1b1k2r/1N6/1Qn1q1p1/2p4p/7P/NP1B2P1/P2P1PR1/R1B5 B
# Starte Runde 65
# message:r1b1k2r/1N1q4/1Qn3p1/2p4p/7P/NP1B2P1/P2P1PR1/R1B5 W
# Starte Runde 66
# message:r1b1k2r/1N1q4/1Qn3p1/1Np4p/7P/1P1B2P1/P2P1PR1/R1B5 B
# Starte Runde 67
# message:r1bqk2r/1N6/1Qn3p1/1Np4p/7P/1P1B2P1/P2P1PR1/R1B5 W
# Starte Runde 68
# message:r1bqk2r/1N6/1Qn3p1/1Np4p/7P/1P1B2P1/P2P1P2/R1B3R1 B
# Starte Runde 69
# message:r2qk2r/1N6/1Qn3p1/1Np4p/6bP/1P1B2P1/P2P1P2/R1B3R1 W
# Starte Runde 70
# message:r2qk2r/1N6/1Qn3p1/1Np4p/6bP/1P4P1/P1BP1P2/R1B3R1 B
# Starte Runde 71
# message:r2qk2r/1N6/1Qn3p1/1Np4p/7P/1P4Pb/P1BP1P2/R1B3R1 W
# Starte Runde 72
# message:r2qk2r/1N6/1Qn3p1/1Np4p/7P/1P1P2Pb/P1B2P2/R1B3R1 B
# Starte Runde 73
# message:r2qk2r/1N6/1Qn5/1Np3pp/7P/1P1P2Pb/P1B2P2/R1B3R1 W
# Starte Runde 74
# message:r2qk2r/1N6/Q1n5/1Np3pp/7P/1P1P2Pb/P1B2P2/R1B3R1 B
# Starte Runde 75
# message:r1bqk2r/1N6/Q1n5/1Np3pp/7P/1P1P2P1/P1B2P2/R1B3R1 W
# Starte Runde 76
# message:r1bqk2r/1N6/Q1n5/1Np3pp/5P1P/1P1P2P1/P1B5/R1B3R1 B
# Starte Runde 77
# message:r1b1k2r/1Nq5/Q1n5/1Np3pp/5P1P/1P1P2P1/P1B5/R1B3R1 W
# Starte Runde 78
# message:r1b1k2r/1Nq5/2n5/QNp3pp/5P1P/1P1P2P1/P1B5/R1B3R1 B
# Starte Runde 79
# message:r1b1k2r/1N5q/2n5/QNp3pp/5P1P/1P1P2P1/P1B5/R1B3R1 W
# Starte Runde 80
# message:remismessage:dsf: has lost the game!!


# rnbqkbnr/pppppppp/8/8/8/4P3/PPP1PPPP/RNBQKBNR B
# FEN;  rnbqkbnr/pppppppp/8/8/8/4P3/PPP1PPPP/RNBQKBNR B
# message:rnbqkbnr/pppppppp/8/8/8/4P3/PPP1PPPP/RNBQKBNR B
# Starte Runde 2
# message:r1bqkbnr/pppppppp/8/8/8/4P3/PPP1PPPP/RNBnKBNR W
# r1bqkbnr/pppppppp/8/8/8/4P3/PPP1PPPP/RNBnKBNR B
# FEN;  r1bqkbnr/pppppppp/8/8/8/4P3/PPP1PPPP/RNBnKBNR B
# message:r1bqkbnr/pppppppp/8/8/8/4P3/PPP1PPPP/RNBnKBNR B
# Starte Runde 3
# message:r1bqkbnr/pppppppp/8/8/8/4P3/PnP1PPPP/RNB1KBNR W
# r1bqkbnr/pppppppp/8/8/8/4P3/PnP1PPPP/RNB1KBNR B
# FEN;  r1bqkbnr/pppppppp/8/8/8/4P3/PnP1PPPP/RNB1KBNR B
# message:r1bqkbnr/pppppppp/8/8/8/4P3/PnP1PPPP/RNB1KBNR B
# Starte Runde 4
# message:r1bq1bnr/pppppppp/8/8/8/4P3/PnP1PkPP/RNB1KBNR W
# r1bq1bnr/pppppppp/8/8/8/4P3/PnP1PkPP/RNB1KBNR B
# FEN;  r1bq1bnr/pppppppp/8/8/8/4P3/PnP1PkPP/RNB1KBNR B
# message:r1bq1bnr/pppppppp/8/8/8/4P3/PnP1PkPP/RNB1KBNR B
# Starte Runde 5
# message:r1bq1bnr/pppppppp/8/8/8/4P3/PnP1P1PP/RNB1KkNR W
# r1bq1bnr/pppppppp/8/8/8/4P3/PnP1P1PP/RNB1KkNR B
# FEN;  r1bq1bnr/pppppppp/8/8/8/4P3/PnP1P1PP/RNB1KkNR B
# message:r1bq1bnr/pppppppp/8/8/8/4P3/PnP1P1PP/RNB1KkNR B
# Starte Runde 6
# message:r1bq1bnr/pppppppp/8/8/8/4P3/PnP1P1PP/RNBkK1NR W
# r1bq1bnr/pppppppp/8/8/8/4P3/PnP1P1PP/RNBkK1NR B
# FEN;  r1bq1bnr/pppppppp/8/8/8/4P3/PnP1P1PP/RNBkK1NR B
# message:r1bq1bnr/pppppppp/8/8/8/4P3/PnP1P1PP/RNBkK1NR B
# Starte Runde 7
# message:r1bq1bnr/ppppp1pp/5p2/8/8/4P3/PnP1P1PP/RNBkK1NR W
# r1bq1bnr/ppppp1pp/5p2/8/8/4P3/PnP1P1PP/RNBkK1NR B
# FEN;  r1bq1bnr/ppppp1pp/5p2/8/8/4P3/PnP1P1PP/RNBkK1NR B
# message:r1bq1bnr/ppppp1pp/5p2/8/8/4P3/PnP1P1PP/RNBkK1NR B