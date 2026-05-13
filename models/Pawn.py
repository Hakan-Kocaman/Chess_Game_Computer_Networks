import sys
import os
sys.path.append(os.path.dirname(__file__)) 

    # Piyon Class
from ChessPiece import ChessPiece



class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(-2, 0), (-1, 0)]  # Kale düz hareket eder
        self.attack_pattern = [(-1, 1), (-1, -1)]
        if self.color.startswith('b'):
            self.move_pattern = [(1, 0), (2, 0)]  # Kale düz hareket eder
            self.attack_pattern = [(1, 1), (1, -1)]
        self.first_move = True
        self.possible_moves = []

    
    def get_possible_moves(self):
        from GameBoard import game_board      

        self.possible_moves = []
        for dx, dy in self.move_pattern:
            for step in range(1, 8):
                nx = self.position[0] + dx * step
                ny = self.position[1] + dy * step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
                target = game_board.board[nx][ny]
                if target is None:
                    self.possible_moves.append((nx, ny))  # boş kare dur
                    break
                else:
                    break  # kendi taşı, dur

        for dx, dy in self.attack_pattern:
            for step in range(1, 8):
                nx = self.position[0] + dx * step
                ny = self.position[1] + dy * step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
                target = game_board.board[nx][ny]
                if target is None:
                    break
                if  target.color != self.color:
                    self.possible_moves.append((nx, ny))
                    break

        return self.possible_moves


