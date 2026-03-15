from Game import Game
import streamlit as st
from AIPlayer import AIPlayer
from utils import check_win_from_last_move, check_tie, available_moves

def new_board() -> list[list[str]]:
    return [
            [".",".",".",".",".",".","."],
            [".",".",".",".",".",".","."],
            [".",".",".",".",".",".","."],
            [".",".",".",".",".",".","."],
            [".",".",".",".",".",".","."],
            [".",".",".",".",".",".","."]
        ]

def reset_game():
    sync_symbols()
    st.session_state.board = new_board()
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.status = ""
    st.session_state.active = st.session_state.start_player
    match st.session_state.difficulty:
        case 1:
            st.session_state.depth = 1
        case 2:
            st.session_state.depth = 2
        case 3:
            st.session_state.depth = 3
        case 4:
            st.session_state.depth = 4
        case 5:
            st.session_state.depth = 5
            
def reset_session():
    reset_game()
    st.session_state.ai_win_num = 0
    st.session_state.human_win_num = 0

def sync_symbols():
    st.session_state.ai = "●" if st.session_state.human == "○" else "○"

def ensure_state():
    if "board" not in st.session_state:
        st.session_state.board = new_board()
    if "human" not in st.session_state:
        st.session_state.human = "○"
    sync_symbols()
    if "depth" not in st.session_state:
        st.session_state.depth = 9
    if "start_player" not in st.session_state:
        st.session_state.start_player = "○"
    if "active" not in st.session_state:
        st.session_state.active = st.session_state.start_player
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "status" not in st.session_state:
        st.session_state.status = ""
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = 5
    if "ai_win_num" not in st.session_state:
        st.session_state.ai_win_num = 0
    if "human_win_num" not in st.session_state:
        st.session_state.human_win_num = 0
    if "tie_num" not in st.session_state:
        st.session_state.tie_num = 0
    if "ai_playstyle" not in st.session_state:
        st.session_state.ai_playstyle = "normal"
    if "last_move" not in st.session_state:
        st.session_state.last_move = None
    if "prev_player" not in st.session_state:
        st.session_state.prev_player = None
        
    if "prev_human" not in st.session_state:
        st.session_state.prev_human = st.session_state.human
    if "prev_start_player" not in st.session_state:
        st.session_state.prev_start_player = st.session_state.start_player
    if "prev_difficulty" not in st.session_state:
        st.session_state.prev_difficulty = st.session_state.difficulty
    
def end_checks():
    w = check_win_from_last_move(st.session_state.board, st.session_state.prev_player, st.session_state.last_move)
    if w:
        st.session_state.game_over = True
        st.session_state.winner = st.session_state.prev_player
        if st.session_state.winner == st.session_state.human:
            st.session_state.human_win_num += 1
        else:
            st.session_state.ai_win_num += 1
    if check_tie(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = None
        st.session_state.tie_num += 1
        
def ai_move():
    if st.session_state.game_over:
        return
    if st.session_state.active != st.session_state.ai:
        return
    
    ai = AIPlayer(st.session_state.ai, st.session_state.human, st.session_state.ai_playstyle)
    moves = available_moves(st.session_state.board)
    
    if not moves:
        end_checks()
        return
    
    r,c = ai.get_best_move(st.session_state.board, st.session_state.depth)
    st.session_state.board[r][c] = st.session_state.ai
    st.session_state.last_move = (r,c)
    st.session_state.prev_player = st.session_state.ai
    
    end_checks()
    if not st.session_state.game_over:
        st.session_state.active = st.session_state.human
    st.rerun()
        
def human_move(c: int):
    r = None
    for row in range(len(st.session_state.board) -1, -1, -1):
        if st.session_state.board[row][c] == ".":
            r = row
            break
    if st.session_state.game_over:
        return
    if st.session_state.active != st.session_state.human:
        return
    if st.session_state.board[r][c] != ".":
        return
    
    st.session_state.board[r][c] = st.session_state.human
    st.session_state.last_move = (r,c)
    st.session_state.prev_player = st.session_state.human
    
    end_checks()
    if not st.session_state.game_over:
        st.session_state.active = st.session_state.ai
    st.rerun()
    

if __name__ == "__main__":
    ensure_state()
    
    st.title("4 in a row minimax")
    st.caption("#####  Click a column to start playing")
    
    with st.sidebar:
        st.header("Settings")
        st.radio("Your Symbol", ["○", "●"], key="human")
        sync_symbols()
        st.radio("Starting Player", ["○", "●"], key="start_player")
        st.selectbox("AI Difficulty", options=list(range(1,6)), key="difficulty")
        st.radio("AI Playstyle", ["aggressive", "normal"], key="ai_playstyle")
        
        if st.button("New Game"):
            reset_game()
        if st.button("New Session"):
            reset_session()
            
        settings_changed = (
            st.session_state.human != st.session_state.prev_human
            or st.session_state.start_player != st.session_state.prev_start_player
            or st.session_state.difficulty != st.session_state.prev_difficulty
            )
        
        if settings_changed:
            reset_game()
            st.session_state.prev_human = st.session_state.human
            st.session_state.prev_start_player = st.session_state.start_player
            st.session_state.prev_difficulty = st.session_state.difficulty
            
    if st.session_state.active == st.session_state.ai and not st.session_state.game_over:
        ai_move()
            
    with st.container():
        for r in range(6):
            cols = st.columns(7, gap=None)
            for c in range(7):
                cell = st.session_state.board[r][c]
                label = " " if cell == "." else cell
                disabled = st.session_state.game_over or (st.session_state.active != st.session_state.human) or (cell != ".") 
                if cols[c].button(label, key = f"cell_{r}_{c}", use_container_width = True, disabled=disabled):
                    human_move(c)
            
        
    
    
    
    
    
    
    