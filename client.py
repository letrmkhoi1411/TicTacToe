from socket import *


# Function to start the client
def start_client():
    serverName = gethostbyname("localhost")
    serverPort = 12000
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((serverName, serverPort))

    # Play the game
    play_game(client_socket)

# Function for the client to play the Tic Tac Toe game
def play_game(client_socket):
    while True:
        # Receive and display the current board
        board = client_socket.recv(1024).decode()
        print(board)

        # Make a move
        move = input("Enter your move (0-8): ")
        client_socket.send(move.encode())

        # Check for game over
        message = client_socket.recv(1024).decode()
        if message:
            print(message)
        
        if "win" in message or "tie" in message:
            break

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
