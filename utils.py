from itertools import combinations

def check_win(moves: dict[str, set[int]], active_player: str) -> bool:
    picked = moves[active_player]
    if len(picked) < 3:
        return False
    
    return any(sum(combo) == 15 for combo in combinations(picked, 3))

def magic_sets_from_board(board: list[list[str]], player_one: str, player_two:str)-> dict[str, set[int]]:
    magic = [4, 9, 2, 3, 5, 7, 8, 1, 6]
    sets = {player_one: set(), player_two: set()}
    for row in range(3):
        for col in range(3):
            sym = board[row][col]
            if sym in sets:
                idx = row * 3 + col
                sets[sym].add(magic[idx])
    return sets
    
    
def winner_from_board(board: list[list[str]], player_one: str, player_two:str) -> str | None:
    magic_sets = magic_sets_from_board(board, player_one, player_two)
    for player, picked in magic_sets.items():
        if len(picked) < 3:
            continue
        if any(sum(combo) == 15 for combo in combinations(picked, 3)):
            return player
        
    return None

def check_tie(board: list[list[str]]) -> bool:
    if all(cell != "." for row in board for cell in row):
        return True
    return False

def available_moves(board: list[list[str]]) -> list[tuple[int, int]]:
    return[(r,c) for r in range(3) for c in range(3) if board[r][c] == "."]

def open_lines(board: list[list[str]], player:str, opponent: str) -> int:
    lines = [
        # rows
        [(0,0),(0,1),(0,2)],
        [(1,0),(1,1),(1,2)],
        [(2,0),(2,1),(2,2)],
        # cols
        [(0,0),(1,0),(2,0)],
        [(0,1),(1,1),(2,1)],
        [(0,2),(1,2),(2,2)],
        # diagonals
        [(0,0),(1,1),(2,2)],
        [(0,2),(1,1),(2,0)],
    ]
    
    count = 0
    for line in lines:
        cells = [board[r][c] for r, c in line]
        if opponent not in cells:
            count += 1
    return count
        
    