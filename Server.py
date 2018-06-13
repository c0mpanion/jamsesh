from socket import *
from _thread import *
import threading


def client_thread(c):

def createServer():
    global sockets
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind((socket.gethostname(), 9000))
    serversocket.listen(10)
    while True:
        # accept connections from outside
        (clientsocket, address) = serversocket.accept()
        sockets.append((clientsocket, address))
        ct = client_thread(clientsocket)
        ct.run()


