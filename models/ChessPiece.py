from abc import ABC, abstractmethod

game_board = [[None for _ in range(8)] for _ in range(8)]
     # Abstract Taş Class
class ChessPiece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.move_pattern = None
        self.possible_moves = None
    @abstractmethod
    def get_possible_moves(self):
        pass

    @abstractmethod
    def move(self, new_position):
        pass

    @abstractmethod
    def die(self):
        pass
