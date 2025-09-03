import EvaluateBoard
class TreeNode():

    def __init__(self, data, turn, parent=None, evaluation=None, depth=None):
        self.data = data
        self.children = []
        self.turn = turn
        self.parent = parent
        self.black_check = False
        self.white_check = False
        self.white_checkmate = False
        self.black_checkmate = False
        self.terminalState = False
        self.evaluation = evaluation
        self.depth = depth

    def add_child(self, data, turn, pdepth=None):
        evaluate = EvaluateBoard.EvaluateBoard(data)
        if pdepth == None:
            self.children.append(TreeNode(data, turn, self, evaluate.evaluation, self.depth+1))
        
        else:
            self.children.append(TreeNode(data, turn, self, evaluate.evaluation, pdepth))

    """
    Returns an array of 2D chess arrays
    """
    def get_children(self):
        return self.children
    
    def get_parent(self):
        return self.parent
    
    def is_checked(self, turn):
        if turn == "b":
            self.black_check = True
        else:
            self.white_check = True
    
    def get_data(self):
        return self.data
