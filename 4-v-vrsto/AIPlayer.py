from utils import check_tie, check_win_from_last_move, available_moves, score_window
import math
import random

class AIPlayer:
    def __init__(self, ai_symbol = "○", human_symbol = "●", playstyle="basic"):
        self.ai_player = ai_symbol
        self.human_player = human_symbol
        self.playstyle = playstyle
        
    def minimax(self, is_maximising: bool, board: list[list[str]], depth: int, alpha: int, beta: int, last_player: str, last_move: tuple[int,int]) -> int:
        tie = check_tie(board)
        win = check_win_from_last_move(board, last_player, last_move)
        
        if win:
            if last_player == self.ai_player:
                return 1000 + depth
            else:
                return -1000 - depth
        if tie:
            return 0
        if depth == 0:
            return self.evaluate(board, last_move) 
        
        if is_maximising:
            max_eval = -math.inf
            moves = available_moves(board)
            for move in moves:
                board[move[0]][move[1]] = self.ai_player
                eval = self.minimax(False, board, depth - 1, alpha, beta, self.ai_player, move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    board[move[0]][move[1]] = "."
                    break
                board[move[0]][move[1]] = "."
            return max_eval
        
        else:
            min_eval = math.inf
            moves = available_moves(board)
            for move in moves:
                board[move[0]][move[1]] = self.human_player
                eval = self.minimax(True, board, depth - 1, alpha, beta, self.human_player, move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if alpha >= beta:
                    board[move[0]][move[1]] = "."
                    break
                board[move[0]][move[1]] = "."
            return min_eval
        
    def evaluate(self, board: list[list[str]], move: tuple[int,int]) -> int:
        score = 0
        rows = len(board)
        cols = len(board[0])
        if self.playstyle == "aggressive":
            move_r,move_c = move
            
            center_col = cols // 2
            for r in range(rows):
                if board[r][center_col] == self.ai_player:
                    score += 3
                elif board[r][center_col] == self.human_player:
                    score -= 3
            
            windows = self.get_windows(board, move_r, move_c)
    
            for coords in windows:
                window = [board[rr][cc] for rr,cc in coords]
                score += score_window(window, self.ai_player, self.human_player)
                score -= int(0.7 * score_window(window, self.human_player, self.ai_player))
                    
        else:
            # horizontal
            for r in range(rows):
                for c in range(cols - 3):
                    window = [board[r][c+i] for i in range(4)]
                    score += score_window(window, self.ai_player, self.human_player)
                    score -= score_window(window, self.human_player, self.ai_player)
        
            # vertical
            for r in range(rows - 3):
                for c in range(cols):
                    window = [board[r+i][c] for i in range(4)]
                    score += score_window(window, self.ai_player, self.human_player)
                    score -= score_window(window, self.human_player, self.ai_player)
        
            # diagonal down-right
            for r in range(rows - 3):
                for c in range(cols - 3):
                    window = [board[r+i][c+i] for i in range(4)]
                    score += score_window(window, self.ai_player, self.human_player)
                    score -= score_window(window, self.human_player, self.ai_player)
        
            # diagonal down-left
            for r in range(rows - 3):
                for c in range(3, cols):
                    window = [board[r+i][c-i] for i in range(4)]
                    score += score_window(window, self.ai_player, self.human_player)
                    score -= score_window(window, self.human_player, self.ai_player)
                
        return score
        
    def get_windows(self, board:list[list[str]], r: int, c: int) -> list[list[tuple[int, int]]]:
        rows = len(board)
        cols = len(board[0])
        windows = []
        
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # down-right
            (1, -1),  # down-left
        ]
        
        for dr, dc in directions:
            for offset in range(4):
                coords = []
                start_r = r - offset * dr
                start_c = c - offset * dc
    
                for i in range(4):
                    rr = start_r + i * dr
                    cc = start_c + i * dc
                    if 0 <= rr < rows and 0 <= cc < cols:
                        coords.append((rr, cc))
                    else:
                        break
    
                if len(coords) == 4 and (r, c) in coords:
                    windows.append(coords)
        return windows
                
    def get_best_move(self, board: list[list[str]], depth: int) -> tuple[int, int]:
        best_score = -math.inf
        best_h = -math.inf
        best_moves: list[tuple[int, int]] = []
        
        for r,c in available_moves(board):
            board[r][c] = self.ai_player
            
            score = self.minimax(False, board, depth-1, -math.inf, math.inf, self.ai_player, (r,c))
            h = self.evaluate(board, (r,c))
            
            board[r][c] = "."
            
            if score > best_score:
                best_score = score
                best_h = h
                best_moves = [(r, c)]
            elif score == best_score:
                if h > best_h:
                    best_h = h
                    best_moves = [(r, c)]
                elif h == best_h:
                    best_moves.append((r, c))
                
        return random.choice(best_moves)
        