
from models.Bishop import Bishop
from models.King import King
from models.Knight import Knight
from models.Pawn import Pawn
from models.Queen import Queen
from models.Rook import Rook


class GameBoard:
    starting_board = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"], # Siyah taşlar
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
    ["·", "·", "·", "·", "·", "·", "·", "·"], # Boş kareler
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"], # Beyaz taşlar
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
    ]
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.init_pieces()
        
    def init_pieces(self):
        # Initialize pawns
        for i in range(8):
            self.board[1][i] = Pawn("white", (1, i))
            self.board[6][i] = Pawn("black", (6, i))
        
        # Initialize rooks
        self.board[0][0] = Rook("white", (0, 0))
        self.board[0][7] = Rook("white", (0, 7))
        self.board[7][0] = Rook("black", (7, 0))
        self.board[7][7] = Rook("black", (7, 7))
        
        # Initialize knights
        self.board[0][1] = Knight("white", (0, 1))
        self.board[0][6] = Knight("white", (0, 6))
        self.board[7][1] = Knight("black", (7, 1))
        self.board[7][6] = Knight("black", (7, 6))
        
        # Initialize bishops
        self.board[0][2] = Bishop("white", (0, 2))
        self.board[0][5] = Bishop("white", (0, 5))
        self.board[7][2] = Bishop("black", (7, 2))
        self.board[7][5] = Bishop("black", (7, 5))
        
        # Initialize queens
        self.board[0][3] = Queen("white", (0, 3))
        self.board[7][3] = Queen("black", (7, 3))
        
        # Initialize kings
        self.board[0][4] = King("white", (0, 4))
        self.board[7][4] = King("black", (7, 4))



