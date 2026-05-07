from abc import ABC, abstractmethod
from GameBoard import game_board
from King import King
     # Abstract Taş Class
class ChessPiece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.move_pattern = None
    @abstractmethod
    def get_possible_moves(self):
        pass
    def move(self, new_position):
        possible_moves = self.get_possible_moves()
        move_result = "move"
       
        if new_position in possible_moves:
            if game_board[new_position[0]][new_position[1]] is not None:
                # Taş yeniyor, tahtadan kaldır
                move_result = "capture "+game_board[new_position[0]][new_position[1]].color+ " "+game_board[new_position[0]][new_position[1]].__class__.__name__
                game_board[new_position[0]][new_position[1]].die()

            self.position = new_position
            game_board[self.position[0]][self.position[1]] = self
            
        for row in game_board:
            for chesspiece in row:
                if isinstance(chesspiece, King) and chesspiece.color != self.color:

                    if chesspiece.position in possible_moves: # şah kontrolü
                        move_result = "check "+chesspiece.color 

                    if chesspiece.get_possible_moves() == []: # mat kontrolü
                        move_result = "checkmate "+chesspiece.color 

        return move_result

    @abstractmethod
    def die(self):
        pass
