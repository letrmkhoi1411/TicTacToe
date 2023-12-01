import socket
import pickle

# import the game
from tictactoe import TicTacToe

HOST = '127.0.0.1'
PORT = 12000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5) 
client_socket, client_address = server_socket.accept()
print(f"\nConnnected to {client_address}!")

# set up the game
player_A = TicTacToe("A")

# allow the player to suggest playing again
rematch = True

while rematch == True: 
    print(f"\n\n T I C - T A C - T O E ")

    while player_A.check_win("A") == False and player_A.check_win("B") == False and player_A.is_draw() == False:
        print(f"\nYour turn!")
        player_A.display_board()
        move = input(f"Enter your move (0-8): ")
        player_A.edit_board(move)

        # draw the grid again
        player_A.display_board()

        A_board = pickle.dumps(player_A.board)
        client_socket.send(A_board)

        # if the player won with the last move or it's a draw, exit the loop 
        if player_A.check_win("A") == True or player_A.is_draw() == True:
            break

        # wait to receive the symbol list and update it
        print(f"\nWaiting for other player...")
        B_board = client_socket.recv(1024)
        B_board = pickle.loads(B_board)
        player_A.update_board(B_board)

    # end game messages
    if player_A.check_win("A") == True:
        print(f"Congrats, you won!")
    elif player_A.is_draw() == True:
        print(f"It's a draw!")
    else:
        print(f"The B won.")

    # ask for a rematch 
    host_response = input(f"\nRematch? (Y/N): ")
    host_response = host_response.capitalize()
    temp_host_resp = host_response
    client_response = ""

    client_socket.send(host_response.encode())

    # if the host doesn't want a rematch, done
    if temp_host_resp == "N":
        rematch = False

    # if the host does want a rematch, ask the client for their opinion
    else:
        # receive client's response 
        print(f"Waiting for client response...")
        client_response = client_socket.recv(1024).decode()

        # if the client doesn't want a rematch, exit the loop 
        if client_response == "N":
            print(f"\nThe client does not want a rematch.")
            rematch = False

        # if both the host and client want a rematch, restart the game
        else:
            player_A.restart()

spacer = input(f"\nThank you for playing!\nPress enter to quit...\n")

client_socket.close()
