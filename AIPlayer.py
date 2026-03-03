from utils import available_moves, winner_from_board, check_tie, open_lines
import math
import random

class AIPlayer:
    def __init__(self, ai_symbol = "o", human_symbol= "x"):
        self.ai_player = ai_symbol
        self.human_player = human_symbol
        
    def minimax(self, is_maximizing: bool, board: list[list[str]], depth: int, alpha: int, beta: int) -> int:
        winner = winner_from_board(board, self.ai_player, self.human_player)
        if winner == self.ai_player:
            return 10
        if winner == self.human_player:
            return -10
        if check_tie(board):
            return 0
        if depth == 0:
            return self.evaluate(board, self.ai_player, self.human_player)
        
        if is_maximizing:
            max_eval = -math.inf
            moves = available_moves(board)   #move = [row, col]
            for move in moves:
                board[move[0]][move[1]] = self.ai_player
                eval = self.minimax(False, board, depth-1, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    board[move[0]][move[1]] = "."
                    break
                board[move[0]][move[1]] = "."
                
            return max_eval
        
        if not is_maximizing:
            min_eval = math.inf
            moves = available_moves(board)
            for move in moves:
                board[move[0]][move[1]] = self.human_player
                eval = self.minimax(True, board, depth-1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if alpha >= beta:
                    board[move[0]][move[1]] = "."
                    break
                board[move[0]][move[1]] = "."
                
            return min_eval
        
    def evaluate(self, board: list[list[str]], max_sym: str, min_sym: str) -> int:
        return open_lines(board, max_sym, min_sym) - open_lines(board, min_sym, max_sym)
    
    def best_move(self, board: list[list[str]], depth: int) -> tuple[int, int]:
        best_score = -math.inf
        best = None
        best_h = -math.inf
        best_moves: list[tuple[int, int]] = []
        
        for r, c in available_moves(board): 
            board[r][c] = self.ai_player    #try a move
            
            score = self.minimax(False, board, depth-1, -math.inf, math.inf)
            h = self.evaluate(board, self.ai_player, self.human_player)
            
            board[r][c] = "."
            
            if score > best_score:
                best_score = score
                best_h = h
                best_moves = [(r,c)]
            elif score == best_score:
                if h > best_h:
                    best_h = h
                    best_moves = [(r,c)]
                elif h == best_h:
                    best_moves.append((r,c))
        
        return random.choice(best_moves)
            