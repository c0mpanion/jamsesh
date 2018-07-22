from socket import *
from socket import error as socket_error
import threading
import pickle

"""
Global variables that are used throughout the program.
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

"""
Function: This function continuously accepts a new TCP connection. It spawns a new 
send_messages thread every time a new connection is created. It adds every new TCP
connection to a list.

Output: A send_messages thread.
"""

def accept_client():
    # Infinite thread, always accepting clients (up to 10)
    while True:
        try:

        # Accept connections, save socket number and address to a list
            client_socket, address = server_socket.accept()

            # Timeout for each client will be 5 minutes
            client_socket.settimeout(300)
            lock.acquire()
            sockets.append((client_socket, address))
            lock.release()

            # Prints who joined the chatroom
            print(str(address) + " connected to the chatroom.")

            # Start thread that allows client to send messages
            thread_client = threading.Thread(target=send_messages, args=[client_socket, address])
            thread_client.start()

        except Exception as exp:
            print("Error: ", exp)

"""
Input: This function takes a client socket and its address as an argument and
runs until the server is shutdown.

Function: It sends text messages to all clients in a TCP message except for the original sender.

Output: Text messages over UDP.
"""
def send_messages(client_socket, address):
    username = ''
    while True:
        """
        If we've received data from a client, check the client list and
        send to all clients in the list except for the one who sent it
        """
        try:
            content = client_socket.recv(1024)
            if not content:
                continue
            else:
                # Sends message to everyone except the client who sent it initially
                try:
                    for (client, address) in sockets:
                        if client != client_socket:
                            client.send(content)

                    # Unpacks the data to save the username to the dictionary
                    content = pickle.loads(content)
                    username = str(content[0])

                    # Adds username to dictionary
                    lock.acquire()
                    users[username] = address
                    lock.release()

                    # Prints each message to the console along with user list
                    print(username + " said '" + str(content[1]) + "'")
                    print("Current user list: " + str(users))

                # Removes a user from the users list if it times out
                except socket_error:
                    lock.acquire()
                    users.pop(username)
                    lock.release()

        # Removes a user from a sockets list if it times out
        except socket_error:
            print(str(address) + " has disconnected from the chat.")
            lock.acquire()
            sockets.remove((client_socket, address))
            lock.release()
            client_socket.close()
            break

"""
Input: This function takes a UDP socket as an argument and runs until the server is shutdown.

Function: It sets a timeout on the UDP socket for 300 seconds (5 minutes).
It tries to receive an input from the socket and will add the connecting client to the list of
UDP "connections." It locks the parts of the code that add and remove connections from a list.

Output: It sends audio messages out over UDP to all the people in the connection except for the person who
sent it.
"""
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

"""

Function: Creates a TCP socket and binds it to an address. It also binds the UDP connection to an
address. It spawns the accept_client and accept_audio threads.
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

    # Start thread for listening to audio messages with the UDP socket
    c_thread = threading.Thread(target=accept_audio, args=[instruments])
    c_thread.start()


