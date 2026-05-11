import sys
import os
sys.path.append(os.path.dirname(__file__)) 

    # Piyon Class
from ChessPiece import ChessPiece



class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(0, 1), (0, 2)]
        self.attacking_pattern = [(-1, 1), (1, 1)]
        if color == "black":
            self.move_pattern = [(0,-1), (0,-2)] # Siyah piyonlar aşağı hareket eder
            self.attacking_pattern = [(-1, -1), (1, -1)]  # Siyah piyonlar çapraz aşağı saldırır
        self.FirstMove = True  # Piyonun ilk hamlesi 

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
                    self.possible_moves.append((nx, ny))  # boş kare ve dur
                    break
                else:
                    break  # taş, dur 
        for dx, dy in self.attacking_pattern:
            nx = self.position[0] + dx
            ny = self.position[1] + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = game_board.board[nx][ny]
                if target is not None and target.color != self.color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur

        return self.possible_moves

