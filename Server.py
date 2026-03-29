import socket
import threading

# Configuration
# '0.0.0.0' allows connections from other computers
HOST = '127.0.0.1'
PORT = 9619

# Explicit sockets
# AF_INET = IPv4, SOCK_STREAM = TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Global Lists
clients = []
nicknames = []

# Game State
game_active = False
player1 = None
player2 = None
p1_move = None
p2_move = None

def broadcast(message):
    """Sends a message to all connected clients."""
    for client in clients:
        try:
            client.send(message)
        except:
            # If the link is broken, we can remove the client later
            pass

def determine_winner():
    """The logic to compare moves and announce winner."""
    global game_active, player1, player2, p1_move, p2_move
    
    # Resolve Nicknames
    n1 = nicknames[clients.index(player1)]
    n2 = nicknames[clients.index(player2)]
    
    result = f"\n=== RESULTS ===\n{n1}: {p1_move}\n{n2}: {p2_move}\n"
    
    if p1_move == p2_move:
        result += "It's a TIE!\n"
    elif (p1_move == 'rock' and p2_move == 'scissors') or \
         (p1_move == 'paper' and p2_move == 'rock') or \
         (p1_move == 'scissors' and p2_move == 'paper'):
        result += f"WINNER: {n1}!\n"
    else:
        result += f"WINNER: {n2}!\n"
        
    broadcast(result.encode('ascii'))
    
    # Reset Game
    game_active = False
    player1 = None
    player2 = None
    p1_move = None
    p2_move = None
    broadcast("--- Game Over. Chat resumed. Type /rps to play again. ---\n".encode('ascii'))

def handle(client):
    """Handles messages from a specific client."""
    global game_active, player1, player2, p1_move, p2_move
    
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            
            # Game Logic
            if message.startswith('/'):
                # 1. Start a Game
                if message.strip() == '/rps' and not game_active:
                    game_active = True
                    player1 = client
                    idx = clients.index(client)
                    broadcast(f"\n>>> {nicknames[idx]} wants to play RPS! Type /join to accept.\n".encode('ascii'))
                
                # 2. Joining a game
                elif message.strip() == '/join' and game_active and player2 is None:
                    if client == player1:
                        client.send("You can't play against yourself!\n".encode('ascii'))
                    else:
                        player2 = client
                        idx = clients.index(client)
                        broadcast(f"\n>>> {nicknames[idx]} joined! P1 vs P2.\n".encode('ascii'))
                        broadcast(">>> PLAYERS: Type 'rock', 'paper', or 'scissors' now!\n".encode('ascii'))

            # 3. Handling Game Moves
            elif game_active and (client == player1 or client == player2):
                move = message.strip().lower()
                if move in ['rock', 'paper', 'scissors']:
                    if client == player1:
                        p1_move = move
                        client.send("Move recorded. Waiting for opponent...\n".encode('ascii'))
                    elif client == player2:
                        p2_move = move
                        client.send("Move recorded. Waiting for opponent...\n".encode('ascii'))
                    
                    # Checking if both players have played
                    if p1_move and p2_move:
                        determine_winner()
                else:
                    client.send("Invalid move! Type rock, paper, or scissors.\n".encode('ascii'))
            
            # Standard Chat
            else:
                # Normal broadcasting
                # Formatted to show "Name: Message"
                broadcast(message.encode('ascii'))
                
        except:
            # Disconnection
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('ascii'))
                nicknames.remove(nickname)
            break

def receive():
    """Main loop to accept new connections."""
    print(f"Server is listening on {HOST}:{PORT}...")
    while True:
        # Accept Connection (Explicit Socket)
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Handshake for Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!\n".encode('ascii'))
        client.send("Connected to server! Type /rps to start a game.\n".encode('ascii'))

        # Start Thread
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()