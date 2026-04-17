from abc import ABC, abstractmethod
     
     # Abstract Taş Class
class ChessPiece(ABC):
    def __init__(self, color, symbol):
        self.color = color
        self.isDead = False
        self.symbol = symbol

    @abstractmethod
    def move(self, board, start_pos, end_pos):
        pass

    @abstractmethod
    def get_possible_moves(self, board, position):
        pass

    @abstractmethod
    def is_valid_move(self, board, start_pos, end_pos):
        pass
    
    # Piyon Class
class Pawn(ChessPiece):
    def __init__(self, color, symbol):
        super().__init__(color, symbol)
    
    def move(self, board, start_pos, end_pos):
        pass
    
    def get_possible_moves(self, board, position):
        pass

    def is_valid_move(self, board, start_pos, end_pos):
        pass

    # At Class    
class Knight(ChessPiece):
    def __init__(self, color, symbol):
        super().__init__(color, symbol)
    
    def move(self, board, start_pos, end_pos):
        pass
    
    def get_possible_moves(self, board, position):
        pass
    
    def is_valid_move(self, board, start_pos, end_pos):
        pass

    # Fil Class
class Bishop(ChessPiece):
    def __init__(self, color, symbol):
        super().__init__(color, symbol)
    
    def move(self, board, start_pos, end_pos):
        pass
    
    def get_possible_moves(self, board, position):
        pass
    
    def is_valid_move(self, board, start_pos, end_pos):
        pass

    # Kale Class
class Rook(ChessPiece):
    def __init__(self, color, symbol):
        super().__init__(color, symbol)
    
    def move(self, board, start_pos, end_pos):
        pass
    
    def get_possible_moves(self, board, position):
        pass
    
    def is_valid_move(self, board, start_pos, end_pos):
        pass

    # Vezir Class
class Queen(ChessPiece):
    def __init__(self, color, symbol):
        super().__init__(color, symbol)
    
    def move(self, board, start_pos, end_pos):
        pass
    
    def get_possible_moves(self, board, position):
        pass
    
    def is_valid_move(self, board, start_pos, end_pos):
        pass

    # Şah Class
class King(ChessPiece):
    def __init__(self, color, symbol):
        super().__init__(color, symbol)
    
    def move(self, board, start_pos, end_pos):
        pass
    
    def get_possible_moves(self, board, position):
        pass
    
    def is_valid_move(self, board, start_pos, end_pos):
        pass

