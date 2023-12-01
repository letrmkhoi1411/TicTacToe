import socket
import pickle
from tictactoe import TicTacToe

HOST = '127.0.0.1'
PORT = 12000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5) 
client_socket, client_address = server_socket.accept()
print(f"\nConnected to {client_address}!")

# set up the game
player_A = TicTacToe("A")

end_game = False

while not end_game == True: 
    print(f"\nT I C   T A C   T O E ")
    print(f"\nBoard index:")
    print("0 1 2")
    print("3 4 5")
    print("6 7 8")

    while (player_A.check_win("A") == False and 
           player_A.check_win("B") == False and 
           player_A.is_draw() == False):
        print(f"\nYour turn!")
        player_A.display_board()

        valid_move = False
        while not valid_move == True:
            move = input(f"Enter your move (0-8):")
            valid_move = player_A.edit_board(move)
        
        player_A.display_board()

        A_board = pickle.dumps(player_A.board)
        client_socket.send(A_board)

        if player_A.check_win("A") == True or player_A.is_draw() == True:
            break

        # wait to receive the symbol list and update it
        print(f"\nWaiting for other player...")
        B_board = client_socket.recv(1024)
        B_board = pickle.loads(B_board)
        player_A.update_board(B_board)

    # end game messages
    if player_A.check_win("A") == True:
        print(f"\nCongrats, you won!")
    elif player_A.check_win("B") == True:
        print(f"\nPlayer B won.")
    else:
        print(f"\nIt's a draw.")

    # ask for a rematch 
    host_response = input(f"\nRematch? (Y/N):")

    client_socket.send(host_response.encode())

    # if the host doesn't want a rematch, done
    if host_response == "N":
        end_game = True

    # if the host does want a rematch, ask the client for their opinion
    else: 
        print(f"Waiting for client response...")
        client_response = client_socket.recv(1024).decode()
        if client_response == "N":
            print(f"\nPlayer B does not want to rematch.")
            end_game = True

        # if both the host and client want a rematch, restart the game
        else:
            player_A.restart()

quit = input(f"\nGame end\nPress enter to quit...\n")

client_socket.close()
