import random
from utils import check_win_from_last_move, available_moves
from AIPlayer import AIPlayer

class Game:
    def __init__(self,  player_one = "○", player_two = "●"):
        self.player_one = player_one
        self.player_two = player_two
        
        self.board = [
                [".",".",".",".",".",".","."],
                [".",".",".",".",".",".","."],
                [".",".",".",".",".",".","."],
                [".",".",".",".",".",".","."],
                [".",".",".",".",".",".","."],
                [".",".",".",".",".",".","."]
            ]
        
        self.running = True
        self.active_player = ""
        
        self.ai_player = AIPlayer(self.player_one, self.player_two) #player1 = AI
        
        self.start_player()
        self.run()
        
    def start_player(self):
        start_player = random.randint(1,2)
        if start_player == 1:
            self.active_player = self.player_one
        else:
            self.active_player = self.player_two
            
    def change_player(self):
        if self.active_player == self.player_one:
            self.active_player = self.player_two
        else:
            self.active_player = self.player_one
        
    def print_board(self):
        print("1 2 3 4 5 6 7")
        for row in self.board:
            print(" ".join(row))
            
    def get_move(self) -> tuple[int, int]:
        if self.active_player == self.player_one:
            move = self.ai_player.get_best_move(self.board, 4)
            return move
        while True:
            raw = input("Enter your move (1-7): ")
            if not raw.isdigit():
                print("Please enter a number")
                continue
            
            n = int(raw)
            if not (1 <= n <= 7):
                print("Number must be from 1-7")
                continue
            
                
            print("Whole column already full")
            continue
            
    def play_move(self, move: tuple[int, int]):
        row, col = move
        self.board[row][col] = self.active_player
    def run(self):
        self.print_board()
        self.start_player()
        while self.running:
            print(f"Current player: {self.active_player}")
            move = self.get_move()
            self.play_move(move)
            if(check_win_from_last_move(self.board, self.active_player, move)):
                self.print_board()
                print(f"Winner: {self.active_player}")
                break
            self.change_player()
            self.print_board()
            print(available_moves(self.board))
            
            