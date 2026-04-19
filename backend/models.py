from abc import ABC, abstractmethod

game_board = [[None for _ in range(8)] for _ in range(8)]
     # Abstract Taş Class
class ChessPiece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position

    # Piyon Class
class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    # At Class    
class Knight(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    # Fil Class
class Bishop(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    # Kale Class
class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    # Vezir Class
class Queen(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    # Şah Class
class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
