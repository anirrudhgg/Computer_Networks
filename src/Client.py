import socket
import threading

# Configuration
# change this to raspberry pi's IP address (e.g., 192.168.101.174)
HOST = '127.0.0.1' 
PORT = 9619  # Matching the server

# Socket setup
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    print("❌ Connection failed! Is the server running?")
    exit()

# Nickname
nickname = input("Choose your nickname: ")

def receive():
    """Listens for messages from Server."""
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred! Disconnected.")
            client.close()
            break

def write():
    """Sends user input to Server."""
    while True:
        try:
            text = input('') # Raw input
            
            # Formatting: "Name: Message"
            
            if text.startswith('/') or text.lower() in ['rock', 'paper', 'scissors']:
                client.send(text.encode('ascii'))
            else:
                message = f'{nickname}: {text}'
                client.send(message.encode('ascii'))
        except:
            client.close()
            break

# Threading
# There are two threads: one for listening, one for speaking.
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
