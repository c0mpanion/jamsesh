from socket import *
from socket import error as socket_error
import threading
import pickle

"""
Accepts a connection to a client and saves their information;
starts a send message thread
"""
global instruments
instruments = socket(AF_INET, SOCK_DGRAM)
global udp_connections
udp_connections = []
global lock
lock = threading.Lock()
global sockets
sockets = []
global users
users = {}

def accept_client():
    # Infinite thread, always accepting clients (up to 10)
    while True:
        # Accept connections, save socket number and address to a list
        try:
            client_socket, address = server_socket.accept()
            # Timeout for each client will be 5 minutes
            client_socket.settimeout(300)
            sockets.append((client_socket, address))
            print(str(address) + " connected to the chatroom.")
            # Start thread that allows client to send messages
            thread_client = threading.Thread(target=send_messages, args=[client_socket, address])
            thread_client.start()

        except Exception as exp:
            print("Error: ", exp)

"""
Sends message from client to all other clients in the chat EXCEPT for the client
that sent it
"""


def send_messages(client_socket, address):
    username = ''
    users = {}
    while True:
        """
        If we've received data from a client, check the client list and
        send to all clients in the list except for the one who sent it
        """
        try:
            content = client_socket.recv(1024)
            if not content:
                break
            else:
                # Sends message to everyone except the client who sent it initially
                try:
                    for (client, address) in sockets:
                        if client != client_socket:
                            client.send(content)

                    content = pickle.loads(content)
                    # Prints the message to server console
                    username = str(content[0])
                    users[username] = address
                    print(username + " said '" + str(content[1]))
                    print("Current user list: " + str(users))
                except socket_error:
                    users.pop(username)
        except socket_error:
            print(str(address) + " has disconnected from the chat.")
            sockets.remove((client_socket, address))
            client_socket.close()
            break


def accept_audio(udp):
    while True:
        try:
            udp.settimeout(300)
            data, addr = udp.recvfrom(1024)
            if addr not in udp_connections:
                print(str(addr) + " has connected through UDP!" + "\n")
                lock.acquire()
                udp_connections.append(addr)
                lock.release()
                print("Current UDP connections: ")
                print(str(udp_connections) + "\n")
            print("Received audio from: " + str(addr))
            for address in udp_connections:
                if addr != address:
                    udp.sendto(data, address)
                    print("Sent to: " + str(address) + "\n")
        except BaseException:
            print(str(addr) + " timed out.")
            lock.acquire()
            udp_connections.remove(addr)
            lock.release()
            break

"""
Create server socket, listen for 10 different clients, start accept client thread
"""

if __name__ == '__main__':

    # Create socket for listening
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('localhost', 9000))

    # Allow up to 10 clients to create a connection to this socket
    server_socket.listen(10)
    print('Server started on port 9000')

    instruments.bind(('localhost', 9001))

    # Start thread that accepts new clients
    c_thread = threading.Thread(target=accept_client)
    c_thread.start()

    c_thread = threading.Thread(target=accept_audio, args=[instruments])
    c_thread.start()


