from abc import ABC, abstractmethod

import sys
import os
sys.path.append(os.path.dirname(__file__)) 


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
        from models.Pawn import Pawn
        from models.King import King
        from models.GameBoard import game_board
        possible_moves = self.get_possible_moves()
        move_result = "unsuccessful move"
        pos_title=None

        new_position = (int(new_position[0]), int(new_position[1]))

        if new_position in possible_moves:
            pos_title = f"{self.position[0]},{self.position[1]},{new_position[0]},{new_position[1]}"
            move_result = "move,"+pos_title+","+self.color
            if game_board.board[new_position[0]][new_position[1]] is not None:
                # Taş yeniyor, tahtadan kaldır
                move_result = "capture,"+pos_title+","+self.color
                game_board.board[new_position[0]][new_position[1]].die()
                
            game_board.board[self.position[0]][self.position[1]] = None
            self.position = new_position
            game_board.board[self.position[0]][self.position[1]] = self
            
            possible_moves = self.get_possible_moves()

            found_king = False
            for row in game_board.board:
                for chesspiece in row:
                    if isinstance(chesspiece, King) and chesspiece.color != self.color:
                        found_king=True
                        if chesspiece.position in possible_moves: # şah kontrolü
                            move_result = "check,"+pos_title+","+self.color
                            if chesspiece.get_possible_moves() == []: # mat kontrolü
                                move_result = "checkmate,"+pos_title+","+self.color
                        break
                if found_king:
                    break
        # cases
        # move_result = "unsuccessful move"
        # pos_title = "from_x,from_y,to_x,to_y"
        # move_result = "move,pos_title"
        # move_result = "capture,pos_title"
        # move_result = "check,pos_title"
        # move_result = "checkmate,pos_title"
        return move_result


    def die(self):
        from models.GameBoard import game_board
        game_board.board[self.position[0]][self.position[1]] = None
