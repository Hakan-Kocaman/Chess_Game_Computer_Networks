import sys
import os
sys.path.append(os.path.dirname(__file__)) 

from GameBoard import game_board
    # Şah Class
from ChessPiece import ChessPiece
from Queen import Queen
from Bishop import Bishop
from Rook import Rook
from Knight import Knight
from Pawn import Pawn




class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Şah hem düz hem çapraz hareket eder
    
    def get_possible_moves(self):
        self.possible_moves = []
        for dx, dy in self.move_pattern:
            for step in range(1, 8):
                nx = self.position[0] + dx * step
                ny = self.position[1] + dy * step
            
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı

                if self.is_threatened((nx, ny)):
                    break

                target = game_board[nx][ny]
            
                if target is None:
                    self.possible_moves.append((nx, ny))  # boş kare ve dur
                    break

                elif target.color != self.color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur
                    break
                else:
                    break  # kendi taşı, dur
        return self.possible_moves
    def is_threatened(self, target_position):

        linear_threats =[(0,1), (1,0), (0,-1), (-1,0)]
        for dx, dy in linear_threats:
            for step in range(1,8):
                nx = target_position[0] + dx * step
                ny = target_position[1] + dy * step
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = game_board[nx][ny]
                    if target is not None and target.color == self.color:# aynı renk taş
                        break
                    if step==1:
                        if target is not None and target.color != self.color and isinstance(target, King):
                            return True
                    if target is not None and target.color != self.color and (isinstance(target, Queen) or isinstance(target, Rook)):
                         return True
                    elif target is not None:
                        break
                    
        diagonal_threats =[(1,1), (1,-1), (-1,1), (-1,-1)]
        for dx, dy in diagonal_threats:
            for step in range(1,8):
                nx = target_position[0] + dx * step
                ny = target_position[1] + dy * step
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = game_board[nx][ny]
                    if target is not None and target.color == self.color:# aynı renk taş
                        break
                    if step==1:
                        if target is not None and target.color != self.color and (isinstance(target, King) or isinstance(target, Pawn)):
                            return True
                    if target is not None and target.color != self.color and (isinstance(target, Queen) or isinstance(target, Bishop)):
                         return True
                    elif target is not None:
                        break
                    
        L_shaped_threats = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        for dx, dy in L_shaped_threats:
            for step in range(1,2):
                nx = target_position[0] + dx * step
                ny = target_position[1] + dy * step
                if 0 <= nx < 8 and 0 <= ny < 8:

                    target = game_board[nx][ny]
                    if target is not None and target.color == self.color:# aynı renk taş
                        break
                    if target is not None and target.color != self.color and isinstance(target, Knight):
                         return True
        
        return False
    def die(self):
        pass

