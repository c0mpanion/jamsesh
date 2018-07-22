from socket import *
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

def accept_client():
    # Infinite thread, always accepting clients (up to 10)
    while True:
        # Accept connections, save socket number and address to a list
        client_socket, address = server_socket.accept()
        sockets.append((client_socket, address))
        print(str(address) + " connected to the chat")

        try:
            # Start thread that allows client to send messages
            thread_client = threading.Thread(target=send_messages, args=[client_socket, address])
            thread_client.start()
        except EOFError:
            client_socket.close()
            sockets.remove((client_socket, address))


"""
Sends message from client to all other clients in the chat EXCEPT for the client
that sent it
"""


def send_messages(client_socket, address):
    while True:
        """
        If we've received data from a client, check the client list and
        send to all clients in the list except for the one who sent it
        """
        content = client_socket.recv(1024)

        if not content:
            break
        else:
            # Sends message to everyone except the client who sent it initially
            for (client, address) in sockets:
                if client != client_socket:
                    client.send(content)

            content = pickle.loads(content)
            # Prints the message to server console
            print(str(content[0]) + " said '" + str(content[1]) + "'")

    print(str(address) + " exited the chat.")
    client_socket.close()
    sockets.remove((client_socket, address))


def accept_audio(udp):
    while True:
        try:
            udp.settimeout(120)
            data, addr = udp.recvfrom(1024)
            print(udp_connections)
            if addr not in udp_connections:
                print(str(addr) + " has connected through UDP!")
                lock.acquire()
                udp_connections.append(addr)
                lock.release()
                print("Current UDP connections: " + str(udp_connections))
            print("Received audio from: " + str(addr))
            for address in udp_connections:
                if addr != address:
                    udp.sendto(data, address)
                    print("Sent to: " + str(address))
        except TimeoutError:
            print(str(addr) + " timed out.")
            lock.acquire()
            udp_connections.remove(addr)
            lock.release()

"""
Create server socket, listen for 10 different clients, start accept client thread
"""

if __name__ == '__main__':
    # Initialize socket list for connections
    sockets = []

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


