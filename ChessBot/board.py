import tkinter as tk
from bot2 import bot2

# Define chess pieces as Unicode characters
PIECES = {
    'wrb': '♖', 'wrw': '♖', 'wnb': '♘', 'wnw': '♘', 'wbb': '♗', 'wbw': '♗', 'wq': '♕', 'wk': '♔', 'p': '♙',
    'brw': '♜', 'brb': '♜', 'bnb': '♞', 'bnw': '♞', 'bbb': '♝', 'bbw': '♝', 'bq': '♛', 'bk': '♚', 'P': '♟'
}
global chessboard
chessboard = [["brw", "bnb", "bbw", "bq", "bk", "bbb", "bnw", "brb"],
            ["bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8"],
            ["wrb", "wnw", "wbb", "wq", "wk", "wbw", "wnb", "wrw"]]   
 


# Create the main window
window = tk.Tk()
window.title("Chessboard")


# Function to get chessboard data from `root`
def get_chessboard(root):
    return root.bestPath[1].data

# Function to update board display
def create_chessboard():
    global chessboard
    # Clear previous board
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

            # Base color
            is_light_square = (row + col) % 2 == 0
            color = "#EEEED2" if is_light_square else "#769656"

            # Highlight selected square
            if selected_position == (row, col):
                color = "#F6F669"  # Yellow-ish highlight

            button = tk.Button(
                board_frame, text=text, font=("Arial", 18), width=5, height=2,
                bg=color, fg=fgColour, command=lambda r=row, c=col: on_square_click(r, c)
            )
            button.grid(row=row, column=col)

# Handle square clicks (select/move pieces)
selected_piece = None
selected_position = None

def on_square_click(row, col):
    global selected_piece, selected_position, chessboard
    piece = chessboard[row][col]

    if selected_piece is None:
        # Select piece
        if piece:  # Only allow selecting a piece if one exists on the square
            selected_piece = piece
            selected_position = (row, col)
    else:
        # If the same square is clicked again, deselect the piece
        if selected_position == (row, col):
            selected_piece = None
            selected_position = None
            return
        # Move piece
        prev_row, prev_col = selected_position

        # Make the move (move the piece to the new square)
        oldChessboard = []
        for i in chessboard:
            tempRow = []
            for j in i:
                tempRow.append(j)
            oldChessboard.append(tempRow)
        chessboard[prev_row][prev_col] = ''  # Clear the original square
        chessboard[row][col] = selected_piece  # Place the piece in the new square

        # Deselect the piece after moving
        selected_piece = None
        selected_position = None

        # Get next turn
        oldChessbot = bot2(oldChessboard, "w")
        if searchForChild(oldChessbot.root, chessboard) == True:
            chessbot = bot2(chessboard,  oldChessbot.root.children[0].turn)
            chessboard = get_chessboard(chessbot)
        else:
            chessboard = oldChessboard
        create_chessboard()

def searchForChild(root, chessboard):
    output = False
    for node in root.children:
        if node.data == chessboard:
            if node.terminalState == True:
                print("Terminal State")

            output = True
            return True

    if output == False:    
        return False
                


# Frame to contain the board
board_frame = tk.Frame(window)
board_frame.pack()



# Create the chessboard initially
create_chessboard()

# Start the Tkinter event loop
window.mainloop()
