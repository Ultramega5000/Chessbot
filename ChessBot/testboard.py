import tkinter as tk
from bot2 import bot2

originalBoard = [["brw", "bnb", "bbw", "bq", "bk", "bbb", "bnw", "brb"],
            ["bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8"],
            ["wrb", "wnw", "wbb", "wq", "wk", "wbw", "wnb", "wrw"]]   

# Define chess pieces as Unicode characters
PIECES = {
    'wrb': '♖', 'wrw': '♖', 'wnb': '♘', 'wnw': '♘', 'wbb': '♗', 'wbw': '♗', 'wq': '♕', 'wk': '♔', 'p': '♙',
    'brw': '♜', 'brb': '♜', 'bnb': '♞', 'bnw': '♞', 'bbb': '♝', 'bbw': '♝', 'bq': '♛', 'bk': '♚', 'P': '♟'
}
originalBoard = [["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "bk"],
            ["", "", "", "", "wq", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""]]   

# Create the main window
window = tk.Tk()
window.title("Chessboard")

chessbot = bot2(originalBoard, "w")
# IntVars to track child indices
childNum_var = tk.IntVar(value=0)
subChildNum_var = tk.IntVar(value=0)

# Get chessboard data
def get_chessboard():
    try:
        child = chessbot.root.children[childNum_var.get()]
        grandchild = child.children[subChildNum_var.get()]
        return grandchild.data
    except (IndexError, AttributeError, KeyError):
        return [['' for _ in range(8)] for _ in range(8)]

# Draw board
def create_chessboard():
    global chessboard
    chessboard = get_chessboard()
    for widget in board_frame.winfo_children():
        widget.destroy()

    for row in range(8):
        for col in range(8):
            piece = chessboard[row][col]
            text = PIECES.get(piece, '')  
            fgColour = "#000000"
            if piece != "":
                if piece[0] == 'w':
                    fgColour = "#CFCA61"
                else:
                    fgColour = "#000000"

            if 'p' in piece:
                if 'b' not in piece:
                    text = '♙'
                else:
                    text = '♟'

            color = "#EEEED2" if (row + col) % 2 == 0 else "#769656"

            button = tk.Button(
                board_frame, text=text, font=("Arial", 12), width=8, height=4,
                bg=color, fg=fgColour, command=lambda r=row, c=col: on_square_click(r, c)
            )
            button.grid(row=row, column=col)

# Piece movement
selected_piece = None
selected_position = None

def on_square_click(row, col):
    global selected_piece, selected_position
    piece = chessboard[row][col]

    if selected_piece is None:
        if piece:
            selected_piece = piece
            selected_position = (row, col)
            print(f"Selected {piece} at {row}, {col}")
    else:
        prev_row, prev_col = selected_position
        chessboard[prev_row][prev_col] = ''
        chessboard[row][col] = selected_piece
        print(f"Moved {selected_piece} to {row}, {col}")
        selected_piece = None
        selected_position = None
        create_chessboard()

# Layout
board_frame = tk.Frame(window)
board_frame.pack()

# First-level child slider
slider1 = tk.Scale(
    window, from_=0, to=len(chessbot.root.children), orient="horizontal", label="childNum (1st gen)",
    variable=childNum_var, command=lambda e: create_chessboard()
)
slider1.pack()

# Second-level child slider
slider2 = tk.Scale(
    window, from_=0, to=len(chessbot.root.children[0].children), orient="horizontal", label="subChildNum (2nd gen)",
    variable=subChildNum_var, command=lambda e: create_chessboard()
)
slider2.pack()

# Initial draw
create_chessboard()

# Tkinter event loop
window.mainloop()