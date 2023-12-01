"""
Tic Tac Toe
"""

class TicTacToe():

    def __init__(self, player_symbol):
        # initialize the board
        self.board = [["0"] * 3 for _ in range(3)]

        # initializes the player symbol
        self.player_symbol = player_symbol


    def restart(self):
        self.board = [["0"] * 3 for _ in range(3)]


    def display_board(self):
        board_str = "\n".join(" ".join(row) for row in self.board)
        print(board_str)


    def edit_board(self, position):
        row, col = divmod(int(position), 3)
        if self.board[row][col] == "0":
            self.board[row][col] = self.player_symbol


    def update_board(self, new_board):
        self.board = new_board


    def check_win(self, player_symbol):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player_symbol:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player_symbol:
                return True

        if (self.board[0][0] == self.board[1][1] == self.board[2][2] == player_symbol or
            self.board[0][2] == self.board[1][1] == self.board[2][0] == player_symbol):
            return True

        return False


    def is_draw(self):
        # see if all the spaces are used up 
        num_blanks = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "0":
                    num_blanks = 1

        # if the player didn't win and no spaces are left, it's a draw
        if self.check_win(self.player_symbol) == False and num_blanks == 0:
            return True
        else:
            return False