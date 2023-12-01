import socket
import pickle

from tictactoe import TicTacToe

HOST = '127.0.0.1'  # the server's IP address 
PORT = 12000        # the port we're connecting to 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"\nConnected to {client_socket.getsockname()}!")

# set up the game
player_B = TicTacToe("B")

end_game = False

while not end_game == True:
    print(f"\nT I C   T A C   T O E ")
    print(f"\nBoard index:")
    print("0 1 2")
    print("3 4 5")
    print("6 7 8")

    # host goes first, client receives first
    print(f"\nWaiting for other player...")
    A_board = client_socket.recv(1024)
    A_board = pickle.loads(A_board)
    player_B.update_board(A_board)
 
    while (player_B.check_win("A") == False and 
           player_B.check_win("B") == False and 
           player_B.is_draw() == False):
        print(f"\nYour turn!")
        player_B.display_board()

        valid_move = False
        while not valid_move == True:
            move = input(f"Enter your move (0-8):")
            valid_move = player_B.edit_board(move)
        
        player_B.display_board()

        B_board = pickle.dumps(player_B.board)
        client_socket.send(B_board)

        if player_B.check_win("B") == True or player_B.is_draw() == True:
            break

        # wait to receive the symbol list and update it
        print(f"\nWaiting for other player...")
        A_board = client_socket.recv(1024)
        A_board = pickle.loads(A_board)
        player_B.update_board(A_board)

    # end game messages
    if player_B.check_win("B") == True:
        print(f"\nCongrats, you won!")
    elif player_B.check_win("A") == True:
        print(f"\nPlayer A won.")
    else:
        print(f"\nIt's a draw.")

    # host is being asked for a rematch, awaiting response 
    print(f"\nWaiting for rematch...")
    host_response = client_socket.recv(1024).decode()

    # if the host wants a rematch, then the client is asked 
    if host_response == "Y":
        client_response = input("Rematch? (Y/N):")
        client_socket.send(client_response.encode())

        # if the client wants a rematch, restart the game
        if client_response == "Y":
            player_B.restart()
        else:
            end_game = True

    # if the host said no, then no rematch 
    else:
        print(f"\nPlayer A does not want to rematch.")
        end_game = True

quit = input(f"\nGame end\nPress enter to quit...\n")

client_socket.close()
