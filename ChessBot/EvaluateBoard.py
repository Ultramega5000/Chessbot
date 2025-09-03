


class EvaluateBoard:
    def __init__(self, board):
        self.board = board
        self.evaluation = self.evaluate("w") - self.evaluate("b")

    def checkAdjacentPieces(self, row, cell, rowModifier, colModifier):
        adjacentPieceIndex = 100
        x = rowModifier
        y = colModifier

        while adjacentPieceIndex == 100 and row+x >= 0 and row+x < 8 and cell >=0 and cell < 8: # checking across the col down
            if self.board[row+x][cell] != "":
                if self.board[row+x][cell][0] != self.board[row][cell][0]:
                    if rowModifier != 0:
                        adjacentPieceIndex = x
                    else:
                        adjacentPieceIndex = y

                if self.board[row+x][cell][0] == self.board[row][cell][0]:
                    if rowModifier != 0:
                        adjacentPieceIndex = x
                    else:
                        adjacentPieceIndex = y
            if rowModifier == 1:
                x+= 1
            if rowModifier == -1:
                x-=1
            
            if colModifier == 1:
                y += 1
            if colModifier == -1:
                y -= 1

        if adjacentPieceIndex == 100:
            if rowModifier == 1:
                return (8-row)*0.1
            
            elif colModifier == 1:
                return 0.1*(8-cell)
            
        
            elif rowModifier == -1:
                return 0.1*(row+1)
        
            else:
                return 0.1*(cell+1)

        else:
            return adjacentPieceIndex*0.1

    
    def evaluate(self, player):
        material = 0
        mobility = 0
        kingSafety = 0
        pawnStructure = 0
        centrality = 0
        for row in range(len(self.board)):
            for cell in range(len(self.board[row])):
                if self.board[row][cell] != "":
                    if self.board[row][cell][0] == player:
                        
                        if self.board[row][cell][1] == "p":
                            material += 1

                            centrality += abs(-0.25*(pow((cell-3.5),2)))*0.1
                            centrality += abs(-0.25*(pow((row-3.5),2)))*0.1
                            

                            if self.board[row][cell][0] == "b": # If it is a black pawn, it can only move down one, unless it is on the 2nd row
                                    try:
                                        if self.board[row-1][cell+1][1] == "p":
                                            pawnStructure += 0.1
                                        
                                        if self.board[row-1][cell-1][1] == "p":
                                            pawnStructure += 0.1
                                            

                                        if row == 1: # If it is on this row, it can move two
                                            if self.board[row+2][cell] == "" and self.board[row-1][cell] == "":
                                                mobility += 0.1

                                        if self.board[row+1][cell] == "": 
                                            mobility += 0.1

                                        if self.board[row+1][cell+1] != "":
                                            if self.board[row+1][cell+1][0] == "w":
                                                mobility += 0.1

                                        if self.board[row+1][cell-1] != "":
                                            if self.board[row+1][cell-1][0] == "w":
                                                mobility += 0.1
                                    except (IndexError):
                                        pass
                            else: # If is a white pawn
                                try:
                                    if self.board[row+1][cell+1][1] == "p":
                                        pawnStructure += 0.1
                                    
                                    if self.board[row+1][cell-1][1] == "p":
                                        pawnStructure += 0.1

                                    if row == 6: # If it is on this row, it can move two
                                        if self.board[row-2][cell] == "" and self.board[row-1][cell] == "":
                                            mobility += 0.1
                                            
                                    if self.board[row-1][cell] == "": 
                                        mobility += 0.1

                                    if self.board[row-1][cell+1] != "":
                                        if self.board[row-1][cell+1][0] == "b":
                                            mobility += 0.1

                                    if self.board[row-1][cell-1] != "":
                                        if self.board[row-1][cell-1][0] == "b":
                                            mobility += 0.1

                                except(IndexError):
                                    pass
                                    

                                    
                        elif self.board[row][cell][1] == "b" or self.board[row][cell][1] == "q":
                            material += 3
                            centrality += abs(-0.25*(pow((cell-3.5),2)))*0.1
                            centrality += abs(-0.25*(pow((row-3.5),2)))*0.1

                            moves = [(1,1), (1, -1), (-1,1), (-1,-1)]
                            for (rowModifier, colModifier) in moves:
                                mobility += abs(self.checkAdjacentPieces(row, cell, rowModifier, colModifier))


                        elif self.board[row][cell][1] == "n":
                            material += 3
                            centrality += abs(-0.25*(pow((cell-3.5),2)))*0.1
                            centrality += abs(-0.25*(pow((row-3.5),2)))*0.1
                        
                            try:
                                moves = [(2,1), (1, 2), (-1, -2), (-1,2), (1, -2), (-2, 1), (2, -1), (-2,- 1)]
                                for (rowModifier, colModifier) in moves:
                                    if self.board[row+rowModifier][cell+colModifier] == "" or self.board[row+rowModifier][cell+colModifier][0] != player:
                                        mobility += 0.1                             
                            
                            except(IndexError):
                                pass
                            

                        elif self.board[row][cell][1] == "r" or self.board[row][cell][1] == "q":
                            material +=5
                            centrality += abs(-0.25*(pow((cell-3.5),2)))*0.1
                            centrality += abs(-0.25*(pow((row-3.5),2)))*0.1

                            moves = [(1,0), (-1, 0), (0,1), (0,-1)]

                            for (rowModifier, colModifier) in moves:
                                mobility += abs(self.checkAdjacentPieces(row, cell, rowModifier, colModifier))


                        elif self.board[row][cell][1] == "q":
                            material += 1
                        
                        elif self.board[row][cell][1] == "k":
                            kingSafety -= ((abs(row - 3.5) + abs(col - 3.5)) * 0.05)
                            try:
                                moves = [(1, 0), (0, 1), (1, 1), (-1,0), (0, -1), (-1, -1), (-1, 1), (1, -1)]
                                for (rowModifier, colModifier) in moves:
                                    if self.board[row+rowModifier][cell+colModifier] == "" or self.board[row+rowModifier][cell+colModifier][0] != player:
                                            mobility += 0.1      
                            
                            except(IndexError):
                                pass
                            


        
        total = material + (centrality*1.5) + (mobility) + pawnStructure+kingSafety
        return total




originalBoard = [["brw", "bnb", "bbw", "bq", "bk", "bbb", "bnw", "brb"],
            ["bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8"],
            ["wrb", "wnw", "wbb", "wq", "wk", "wbw", "wnb", "wrw"]]   

evaluator = EvaluateBoard(originalBoard)
print(evaluator.evaluation)