import socket
import pickle

# import the game
from tictactoe import TicTacToe

HOST = '127.0.0.1'  # the server's IP address 
PORT = 12000        # the port we're connecting to 

# connect to the host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"\nConnected to {client_socket.getsockname()}!")

# set up the game
player_B = TicTacToe("B")

# allow the player to suggest playing again
rematch = True

while rematch == True:
    # a header for an intense tic-tac-toe match! 
    print(f"\n\n T I C - T A C - T O E ")

    # draw the grid
    player_B.display_board()

    # host goes first, client receives first
    print(f"\nWaiting for other player...")
    A_board = client_socket.recv(1024)
    A_board = pickle.loads(A_board)
    player_B.update_board(A_board)

    # the rest is in a loop; if either player has won, it exits 
    while player_B.check_win("A") == False and player_B.check_win("B") == False and player_B.is_draw() == False:
        # draw grid, ask for coordinate 
        print(f"\nYour turn!")
        player_B.display_board()
        move = input(f"Enter your move (0-8): ")
        player_B.edit_board(move)

        # draw grid again
        player_B.display_board()

        B_board = pickle.dumps(player_B.board)
        client_socket.send(B_board)

        # if the player won with the last move or it's a draw, exit the loop 
        if player_B.check_win("B") == True or player_B.is_draw() == True:
            break

        # wait to receive the symbol list and update it
        print(f"\nWaiting for other player...")
        A_board = client_socket.recv(1024)
        A_board = pickle.loads(A_board)
        player_B.update_board(A_board)

    # end game messages
    if player_B.check_win("B") == True:
        print(f"Congrats, you won!")
    elif player_B.is_draw() == True:
        print(f"It's a draw!")
    else:
        print(f"the A won.")

    # host is being asked for a rematch, awaiting response 
    print(f"\nWaiting for host...")
    host_response = client_socket.recv(1024).decode()
    client_response = "N"

    # if the host wants a rematch, then the client is asked 
    if host_response == "Y":
        print(f"\nThe host would like a rematch!")
        client_response = input("Rematch? (Y/N): ")
        client_response = client_response.capitalize()
        temp_client_resp = client_response

        # let the host know what the client decided 
        client_socket.send(client_response.encode())

        # if the client wants a rematch, restart the game
        if temp_client_resp == "Y":
            player_B.restart()

        # if the client said no, then no rematch 
        else:
            rematch = False

    # if the host said no, then no rematch 
    else:
        print(f"\nThe host does not want a rematch.")
        rematch = False

spacer = input(f"\nPress enter to quit...\n")

client_socket.close()
