import sys
import os
sys.path.append(os.path.dirname(__file__)) 
    # Kale Class
from ChessPiece import ChessPiece
from GameBoard import game_board


class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Kale düz hareket eder
    
    def get_possible_moves(self):
        self.possible_moves = []
        for dx, dy in self.move_pattern:
            for step in range(1, 8):
                nx = self.position[0] + dx * step
                ny = self.position[1] + dy * step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
                target = game_board[nx][ny]
                if target is None:
                    self.possible_moves.append((nx, ny))  # boş kare devam
                elif target.color != self.color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur
                    break
                else:
                    break  # kendi taşı, dur
        return self.possible_moves

