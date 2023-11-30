import os
from socket import *
from _thread import *

def start_server():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("localhost",serverPort))
    serverSocket.listen()
    print("The server is ready to receive")

    player1, addr1 = serverSocket.accept()
    print(f"Player 1 connected from {addr1}")
    player2, addr2 = serverSocket.accept()
    print(f"Player 2 connected from {addr2}")

    play_game(player1, player2)


def play_game(player1, player2):
    current_player = player1

    # Initialize the game board
    board = [[" "] * 3 for _ in range(3)]

    while True:
        # Send the current board to the current player
        send_board(current_player, board)

        # Receive the player's move
        move = current_player.recv(1024).decode()

        # Update the board with the player's move
        row, col = divmod(int(move), 3)
        if board[row][col] == " ":
            board[row][col] = "X" if current_player == player1 else "O"

        # Check for a win or a tie
        if check_win(board):
            current_player.send("Congratulations! You win!".encode())
            break
        elif all(all(cell != " " for cell in row) for row in board):
            player1.send("It's a tie! The game is over.".encode())
            player2.send("It's a tie! The game is over.".encode())
            break

        # Switch to the other player
        current_player = player2 if current_player == player1 else player1

    # Close the connections
    player1.close()
    player2.close()

# Function to send the current board to a player
def send_board(player, board):
    board_str = "\n".join(" ".join(row) for row in board)
    player.send(board_str.encode())

# Function to check for a win
def check_win(board):
    # Check rows, columns, and diagonals for a win
    # for i in range(3):
    #     if board[i][0] == board[i][1] == board[i][2] != " ":
    #         return True
    #     if board[0][i] == board[1][i] == board[2][i] != " ":
    #         return True

    # if board[0][0] == board[1][1] == board[2][2] != " " or board[0][2] == board[1][1] == board[2][0] != " ":
    #     return True

    return False

if __name__ == "__main__":
    start_server()
