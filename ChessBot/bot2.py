import TreeNode
import EvaluateBoard
from collections import deque

class bot2():

    def get_all_children_for_node(self, node):
        for row in range(len(node.data)):
            for cell in range(len(node.data[row])):
                if len(node.data[row][cell]) > 1:
                    if node.data[row][cell][0] != node.turn: # If the piece we are looking at is not on its turn, it cannot be moved
                        continue

                    else:
                        if node.data[row][cell][1] == "p": # If it is a pawn
                            if node.data[row][cell][0] == "b": # If it is a black pawn, it can only move down one, unless it is on the 2nd row

                                try:

                                    if row == 1: # If it is on this row, it can move two
                                        if node.data[row+2][cell] == "" and node.data[row+1][cell] == "":
                                            self.movePiece(row, cell, 2, 0, node)

                                    if node.data[row+1][cell] == "": 
                                        self.movePiece(row, cell, 1, 0, node)

                                    if node.data[row+1][cell+1] != "":
                                        if node.data[row+1][cell+1][0] == "w":
                                            self.movePiece(row, cell, 1, 1, node)
                                    if node.data[row+1][cell-1] != "":
                                        if node.data[row+1][cell-1][0] == "w":
                                            self.movePiece(row, cell, 1, -1, node)
                                except (IndexError):
                                    pass
                            else: # If is a white pawn
                                try:
                                    if row == 6: # If it is on this row, it can move two
                                        if node.data[row-2][cell] == "" and node.data[row-1][cell] == "":
                                            self.movePiece(row, cell, -2, 0, node)
                                            
                                    if node.data[row-1][cell] == "": 
                                        self.movePiece(row, cell, -1, 0, node)

                                    if node.data[row-1][cell+1][0] == "b":
                                        self.movePiece(row, cell, -1, 1, node)

                                    if node.data[row-1][cell-1][0] == "b":
                                        self.movePiece(row, cell, -1, -1, node)
                                
                                except (IndexError):
                                    pass

                        if node.data[row][cell][1] == "r" or node.data[row][cell][1] == "q": # If it is a rook, doesn't matter what colour they follow the same rules
                            # When a rook is moved, it can move on to another piece but may not pass it
                            # checks along row forwards

                            moves = [(1,0), (-1, 0), (0,1), (0,-1)]

                            for (rowModifier, colModifier) in moves:
                                self.checkAdjacentPieces(row, cell, rowModifier, colModifier, node)

                        if node.data[row][cell][1] == "n": # If knight
                            moves = [(2,1), (1, 2), (-1, -2), (-1,2), (1, -2), (-2, 1), (2, -1), (-2,- 1)]
                            for (rowModifier, colModifier) in moves:
                                self.movePiece(row, cell, rowModifier, colModifier, node)
                        
                        if node.data[row][cell][1] == "b" or node.data[row][cell][1] == "q": # If bishop
                            moves = [(1,1), (1, -1), (-1,1), (-1,-1)]

                            for (rowModifier, colModifier) in moves:
                                self.checkAdjacentPieces(row, cell, rowModifier, colModifier, node)
                        
                        if node.data[row][cell][1] == "k":
                            moves = [(1, 0), (0, 1), (1, 1), (-1,0), (0, -1), (-1, -1), (-1, 1), (1, -1)]
                            for (rowModifier, colModifier) in moves:
                                self.movePiece(row, cell, rowModifier, colModifier, node)


    def getIdenticalSibling(self, node):
        for child in node.parent.children:
            if child.data == node.data and node != child:
                return child
    
    def checkAdjacentPieces(self, row, cell, rowModifier, colModifier, node):
        adjacentPiece = False
        x = rowModifier
        y = colModifier

        while adjacentPiece == False and row+x >= 0 and row+x < 8 and cell+y >=0 and cell+y < 8: # checking across the col down
            self.movePiece(row, cell, x, y, node)
            if node.data[row+x][cell+y] != "": # if it runs in to a piece, that is the end
                adjacentPiece = True

            # Increments x and y values
            if rowModifier == 1:
                x+= 1

            if rowModifier == -1:
                x-=1
            
            if colModifier == 1:
                y += 1
            if colModifier == -1:
                y -= 1

    def movePiece(self, row, cell, rowModifier, colModifier, node):
        # Node is the parent
        def addChild():
            new_board = []
            for i in range(len(node.data)):
                temprow = []
                for j in range(len(node.data[i])):
                    temprow.append(node.data[i][j])
                new_board.append(temprow)

            if new_board[row+rowModifier][cell+colModifier] != "":
                if new_board[row+rowModifier][cell+colModifier][0] == node.turn:
                    return

            new_board[row+rowModifier][cell+colModifier] = node.data[row][cell]
            new_board[row][cell] = ""

            node.add_child(new_board, self.incrementTurn(node.turn)) # add regular child for next turn
            node.add_child(new_board, node.turn) # add ghost child to check for any new checks made from a move in the previous turn

            if node.depth < self.MAXDEPTH:
                self.get_all_children_for_node(node.children[len(node.children)-2]) # gets children of the first node to be added

            
            if node.depth < self.MAXDEPTH:
                self.get_all_children_for_node(node.children[len(node.children)-1]) # gets children of last node to be added

        if row+rowModifier < 8 and cell+colModifier < 8 and row+rowModifier >= 0 and cell+colModifier >= 0: # check move is within bounds of board

            if "k" in node.data[row+rowModifier][cell+colModifier] and node.data[row+rowModifier][cell+colModifier][0] != node.turn:  
                if node.parent != None:
                    if node.turn != node.parent.turn: # checks if node isn't a ghost node
                        node.is_checked(self.incrementTurn(node.turn)) # Opposite turn is in check   
                    else:
                        sibling = self.getIdenticalSibling(node)
                        if sibling:
                            sibling.is_checked(self.incrementTurn(node.turn))

                else:
                    node.is_checked(self.incrementTurn(node.turn)) # Opposite turn is in check   

            else:
                if node.parent != None:
                    if node.turn != node.parent.turn: # checks if node isn't a ghost node
                        addChild()

                else:
                    addChild()

    def incrementTurn(self, turn):
        if turn == "w":
            return "b"
        
        else:
            return "w"

    def terminalState(self, node):
        # Tests for stalemate where there are just kings
        non_king_pieces = "bnrqp"
        stalemate = True
        for row in node.data:
            for cell in row:
                if len(cell) > 0:
                    if cell[1] in non_king_pieces:
                        stalemate = False
        
        # Tests if there any valid moves to be made from the node
        if len(node.get_children()) == 0:
            if node.black_check and node.turn == "b": # White checkmate
                print("White checkmate")
                stalemate = False
                node.evaluation += 100
                return True

            elif node.white_check and node.turn == "w": # Black Checkmate
                print("Black checkmate")
                stalemate = False
                node.evaluation -= 100
                return True
            else:
                stalemate = True

        return stalemate

    def trimIllegalMoves(self, parent):
        filtered = []
        for node in parent.children:
            if (parent.turn == "w" and node.white_check) or (parent.turn == "b" and node.black_check):
                # skip this node
                continue
            else:
                filtered.append(self.trimIllegalMoves(node))
        parent.children = filtered
        return parent

    def trimGhostNodes(self, parent):
        filtered = []
        for node in parent.children:
            if node.turn == parent.turn:
                continue
            else:
                filtered.append(self.trimGhostNodes(node))
        parent.children = filtered
        return parent

    def findTerminalStates(self, parent):
        parent.terminalState = self.terminalState(parent)
        if parent.terminalState == True:
            parent.children = []
            parent.terminalState = True
        else:
            for node in parent.children:
                node = self.findTerminalStates(node)
        
        return parent


    def find_last_generation(self, root):
        if root is None:
            return None

        frontier = deque([root])
        last_level_values = []

        while frontier:
            level_size = len(frontier)
            current_level_values = []

            for _ in range(level_size):
                current_node = frontier.popleft()
                current_level_values.append(current_node)

                for child in current_node.children:
                    frontier.append(child)

            # Update after finishing this level
            last_level_values = current_level_values

        # After loop ends, last_level_values contains values of deepest generation
        return last_level_values

    
    def minimax(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or node.terminalState or len(node.children) == 0:
            return node.evaluation

        if maximizingPlayer:
            maxEval = float("-inf")
            for child in node.children:
                eval = self.minimax(child, depth-1, alpha, beta, False)
                child.evaluation = eval
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            node.evaluation = maxEval
            return maxEval
        else:
            minEval = float("inf")
            for child in node.children:
                eval = self.minimax(child, depth - 1, alpha, beta, True)
                child.evaluation = eval  # Store child evaluation
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            node.evaluation = minEval
            return minEval

    

    def get_best_path(self, root):
        path = [root]
        current = root
        while current.children:
            # Pick the child with the same evaluation as current
            best_child = None
            if current.turn == "w":  # White maximizing
                best_child = max(current.children, key=lambda c: c.evaluation)
            else:  # Black minimizing
                best_child = min(current.children, key=lambda c: c.evaluation)
            path.append(best_child)
            current = best_child
        return path

    def __init__(self, board, turn):


        self.MAXDEPTH = 2

        evaluator = EvaluateBoard.EvaluateBoard(board)


        self.root = TreeNode.TreeNode(board, turn)
        self.root.depth = 0
        self.root.evaluation = evaluator.evaluation
        print(self.root.evaluation)

        self.get_all_children_for_node(self.root)

        self.root = self.trimGhostNodes(self.root)
        self.root = self.trimIllegalMoves(self.root)
        self.root = self.findTerminalStates(self.root)

        if not self.root.terminalState:
            self.minimax(self.root, self.MAXDEPTH, float("-inf"), float("inf"), turn == "b")
            self.bestPath = self.get_best_path(self.root)