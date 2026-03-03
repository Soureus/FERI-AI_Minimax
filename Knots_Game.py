import random
from utils import winner_from_board
from AIPlayer import AIPlayer

class Game:
    def __init__(self, player_one="x", player_two="o"):
        self.player_one = player_one
        self.player_two = player_two
        
        self.ai_player = AIPlayer(self.player_one, self.player_two) #player1 = AI
        
        self.board = [
                [".",".","."],
                [".",".","."],
                [".",".","."]
            ]
        
        self.scores = [4, 9, 2, 3, 5, 7, 8, 1, 6]
        self.moves = {self.player_one: set(), self.player_two: set()}
        self.search_depth = 9
        
        self.running = True
        
        self.active_player = ""
        
        self.start_player()
        self.run_game()
        
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
        for row in self.board:
            print("".join(row))
            
    def num_to_pos(self, n:int) -> tuple[int, int]:
        n-=1
        return n // 3, n % 3
            
    def get_move(self) -> tuple[int, int]:
        if self.active_player == self.player_one:
            move = self.ai_player.best_move(self.board, self.search_depth)
            return move
        while True:
            raw = input("Choose a spot (1-9): ")
            
            if not raw.isdigit():
                print("Please enter a number")
                continue
            
            n = int(raw)
            if not (1 <= n <= 9):
                print("Number must be from 1-9")
                continue
            
            r, c = self.num_to_pos(n)
            if(self.board[r][c] != "."):
                print("Spot already taken!")
                continue
            
            self.moves[self.active_player].add(self.scores[n-1])
            return r,c
                
    def difficulty_sellect(self):
        difficulty = input("Select a difficulty (1-5), default: 5: ")
        difficulty = int(difficulty)
        match difficulty:
            case 1:
                self.search_depth = 1
            case 2:
                self.search_depth = 2
            case 3:
                self.search_depth = 3
            case 4:
                self.search_depth = 5
            case 5:
                self.search_depth = 9
            
    
    def run_game(self):
        self.difficulty_sellect()
        while self.running:
            self.print_board()
            print("Current turn: {}".format(self.active_player))
            r, c = self.get_move()
            self.board[r][c] = self.active_player
            if winner_from_board(self.board, self.player_one, self.player_two):
                self.print_board()
                print(f"Player {self.active_player} has won the game!")
                self.running = False
                continue
                
            if all(cell != "." for row in self.board for cell in row):
                self.print_board()
                print("It's a draw!")
                self.running = False
                continue
            self.change_player()
            
            
            