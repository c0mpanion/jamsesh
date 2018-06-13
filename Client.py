from socket import *
import threading
import pickle


"""
Sends username and message to the server
"""


def send(username):
    while True:
        # Prompts user for message to send
        message = input('\n' + username + ' > ')

        # Packages data as a list to send
        total_data = pickle.dumps([username, message])

        # Sends data
        client_socket.sendto(total_data, ('localhost', 9000))


"""
Receives username and message received and prints to client's console
"""


def receive():
    while True:
        # Receives data in a buffer
        received_data = client_socket.recv(1024)

        # Unpacks the buffer into a readable list
        data = pickle.loads(received_data)

        # Prints the data received as 'username > message'
        print('\n' + str(data[0]) + ' > ' + str(data[1]))


"""
Creates a socket, connects to server, gets username of client, and starts 
send and receive threads
"""


if __name__ == "__main__":

    # Creates a socket for receiving messages
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Connects to the server
    client_socket.connect(('localhost', 9000))
    print('Connected to remote host...')

    # Prompts user for username
    username = input('Enter your name > ')

    # Starts thread for sending messages
    thread_send = threading.Thread(target=send, args=[username])
    thread_send.start()

    # Starts thread for receiving messages
    thread_receive = threading.Thread(target=receive)
    thread_receive.start()

