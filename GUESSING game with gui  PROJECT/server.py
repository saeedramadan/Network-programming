import socket
import threading
import random

# Server configuration
host = 'localhost'
port = 7001

# Generate a random number
number = random.randint(1, 100)

# List to store connected clients
clients = []
guesses = {}

# Locks for thread safety
lock = threading.Lock()
guess_lock = threading.Lock()


def handle_client(client_socket):
    # Add client to the list
    with lock:
        clients.append(client_socket)

    while True:
        try:
            # Receive client's guess
            guess = int(client_socket.recv(1024).decode())

            # Store the guess for the client
            with guess_lock:
                guesses[client_socket] = guess

            # Check if the guess is correct
            if guess == number:
                # Send win message to the client
                client_socket.send('Correct guess! You win!'.encode())

                # Send lose message to the other player
                for client in clients:
                    if client != client_socket:
                        client.send('You lose! Better luck next time.'.encode())

                # Close all client sockets
                close_all_clients()

                break
            elif guess < number:
                client_socket.send('Too low! Guess higher.'.encode())
            else:
                client_socket.send('Too high! Guess lower.'.encode())

        except ValueError:
            client_socket.send('Invalid guess! Try again.'.encode())

    # Close the client socket
    client_socket.close()


def close_all_clients():
    with lock:
        for client in clients:
            client.close()
        clients.clear()


def start_server():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print('Server started. Waiting for connections...')

    while len(clients) < 2:
        # Accept a client connection
        client_socket, address = server_socket.accept()

        print('Connected to', address)

        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(client_socket,)).start()


# Start the server
start_server()

