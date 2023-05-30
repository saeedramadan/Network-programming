import socket
import tkinter as tk
import threading

# Server configuration
host = 'localhost'
port = 7001

# Create a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

def send_guess():
    # Get the user's guess from the entry field
    guess = entry.get()

    try:
        # Send the guess to the server
        client_socket.send(guess.encode())

    except ConnectionRefusedError:
        result_label.configure(text='Failed to connect to the server.')


def receive_response():
    while True:
        try:
            # Receive and display the server's response
            response = client_socket.recv(1024).decode()

            # Update the result label in the GUI thread
            window.after(0, lambda: result_label.configure(text=response))

            # Check if the response is a win message
            if response.startswith('Correct guess!') or response.startswith('You lose! Better luck next time'):
                # Disable the entry and button
                window.after(0, lambda: entry.configure(state='disabled'))
                window.after(0, lambda: button.configure(state='disabled'))
                break

        except ConnectionResetError:
            # Server connection closed
            window.after(0, lambda: result_label.configure(text='Server connection closed.'))
            break


# Create the Tkinter window
window = tk.Tk()
window.title('Guessing')
window.configure(background='white')

# Create the UI elements
label = tk.Label(window, text='Enter your guess:', font=('Arial', 16), fg='black', bg='white')
label.pack(pady=10)

entry = tk.Entry(window, font=('Arial', 14), width=10)
entry.pack()

button = tk.Button(window, text='Submit', command=send_guess, font=('Arial', 14), fg='black', bg='lightblue')
button.pack(pady=10)

result_label = tk.Label(window, text='', font=('Arial', 16), fg='black', bg='white')
result_label.pack(pady=10)

# Start the thread to receive server responses
threading.Thread(target=receive_response).start()

# Start the Tkinter event loop
window.mainloop()

# Close the client socket
client_socket.close()

