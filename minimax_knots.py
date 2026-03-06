import streamlit as st
from AIPlayer import AIPlayer
from utils import winner_from_board, check_tie, available_moves

# -- helpers -- 
def new_board():
    return [[".",".", "."],
            [".",".", "."],
            [".",".", "."]]

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
            st.session_state.depth = 5
        case 5:
            st.session_state.depth = 9
            
def reset_session():
    reset_game()
    st.session_state.ai_win_num = 0
    st.session_state.human_win_num = 0
    
def sync_symbols():
    st.session_state.ai = "o" if st.session_state.human == "x" else "x"
    
def ensure_state():
    if "board" not in st.session_state:
        st.session_state.board = new_board()
    if "human" not in st.session_state:
        st.session_state.human = "x"
    sync_symbols()
    if "depth" not in st.session_state:
        st.session_state.depth = 9
    if "start_player" not in st.session_state:
        st.session_state.start_player = "x"
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
        
    if "prev_human" not in st.session_state:
        st.session_state.prev_human = st.session_state.human
    if "prev_start_player" not in st.session_state:
        st.session_state.prev_start_player = st.session_state.start_player
    if "prev_depth" not in st.session_state:
        st.session_state.prev_depth = st.session_state.depth
        

#-- Game --
def end_checks():
    w = winner_from_board(st.session_state.board, st.session_state.ai, st.session_state.human)
    if w is not None:
        st.session_state.game_over = True
        st.session_state.winner = w
        if w == st.session_state.ai:
            st.session_state.ai_win_num += 1
        else:
            st.session_state.human_win_num += 1
    if check_tie(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = None

def ai_turn():
    if st.session_state.game_over:
        return
    if st.session_state.active != st.session_state.ai:
        return
    
    ai = AIPlayer(st.session_state.ai, st.session_state.human)
    moves = available_moves(st.session_state.board)
    if not moves:
        end_checks()
        return
    
    r,c = ai.best_move(st.session_state.board, st.session_state.depth)
    st.session_state.board[r][c] = st.session_state.ai
    
    end_checks()
    if not st.session_state.game_over:
        st.session_state.active = st.session_state.human
    st.rerun()
        
def human_move(r,c):
    if st.session_state.game_over:
        return
    if st.session_state.active != st.session_state.human:
        return
    if st.session_state.board[r][c] != ".":
        return
    
    st.session_state.board[r][c] = st.session_state.human
    
    end_checks()
    if not st.session_state.game_over:
        st.session_state.active = st.session_state.ai
    st.rerun()

# -- UI --
ensure_state()

st.title("Tic-Tac-Toe Minimax")
st.caption("Click a square to start playing")

with st.sidebar:
    st.header("Settings")
    
    st.radio("Your symbol", ["x", "o"], key="human")
    sync_symbols()
    st.radio("Starting player", ["x", "o"], key="start_player")
    st.slider("AI Difficulty", 1, 5, key="difficulty")
        
    if st.button("New Game"):
        reset_game()
    if st.button("New Session"):
        reset_session()
        
    settings_changed = (
        st.session_state.human != st.session_state.prev_human
        or st.session_state.start_player != st.session_state.prev_start_player
        or st.session_state.depth != st.session_state.prev_depth
        )

    if settings_changed:
        reset_game()
        st.session_state.prev_human = st.session_state.human
        st.session_state.prev_start_player = st.session_state.start_player
        st.session_state.prev_depth = st.session_state.depth
        
if st.session_state.active == st.session_state.ai and not st.session_state.game_over:
    ai_turn()
    
if st.session_state.game_over:
    if st.session_state.winner is None:
        st.subheader("Result: Draw")
    elif st.session_state.winner == st.session_state.human:
        st.subheader(f"Winner: You! ({st.session_state.human})")
    else:
        st.subheader(f"Winner: AI ({st.session_state.ai})")

st.markdown(
    """
    <style>
    .st-emotion-cache-1n6tfoc{
        gap: 0;
    }
    div[class*="st-key-cell_"] button {
        aspect-ratio: 1 / 1;
        font-size: 200px;
        font-weight: 700;
    }
    div[class*="st-key-cell_"] .stButton > button *{
        font-size: 90px !important;
        font-weight: 800 !important;
        color: white !important;
        line-height: 1 !important;
    }
    .st-emotion-cache-1n6tfoc *{
        border-radius: 0;
        }
    </style>        
    """, unsafe_allow_html=True
)


#board
with st.container():
    for r in range(3):
        cols = st.columns(3, gap=None)
        for c in range(3):
            cell = st.session_state.board[r][c]
            label = " " if cell == "." else cell
            disabled = st.session_state.game_over or (st.session_state.active != st.session_state.human) or (cell != ".") 
            if cols[c].button(label, key = f"cell_{r}_{c}", use_container_width = True, disabled=disabled):
                human_move(r,c)
st.write(f"AI wins: {st.session_state.ai_win_num}  \nHuman Wins: {st.session_state.human_win_num}")
    

    
    