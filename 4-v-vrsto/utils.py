
def check_win_from_last_move(board: list[list[str]], player_symbol: str, move: tuple[int, int]) -> bool | None:
    directions = [
            (0,1),
            (1,0),
            (1,1),
            (1,-1)
        ]
    
    row, col = move
    rows = len(board)
    cols = len(board[0])
    
    for dr, dc in directions:
        count = 1
        
        r,c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
            
        r,c = row -dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_symbol:
            count += 1
            r -= dr
            c -= dc
            
        if count >= 4:
            return True
    
    return False

def available_moves(board: list[list[str]]) -> list[tuple[int, int]]:
    moves: list[tuple[int, int]] = []
    rows = len(board)
    cols = len(board[0])
    
    for col in range(cols):
        for row in range(rows - 1, -1, -1):
            if board[row][col] == ".":
                moves.append((row, col))
                break
    return moves

def check_tie(board: list[list[str]]) -> bool:
    if all(cell != "." for row in board for cell in row):
        return True
    return False

def score_window(window: list[str], player: str, opponent: str) -> int:
    if opponent in window:
        return 0
    count_player = window.count(player)
    
    if count_player == 4:
        return 100
    elif count_player == 3:
        return 50
    elif count_player == 2:
        return 10
    elif count_player == 1:
        return 1
    else:
        return 0

def is_open_for_player(window: list[str], curr_player:str, opponent: str) -> bool:
    if opponent not in window:
        return True
    return False
                