import sys
import os
sys.path.append(os.path.dirname(__file__)) 

from models.ChessPiece import ChessPiece
from models.Queen import Queen
from models.Bishop import Bishop
from models.Rook import Rook
from models.Knight import Knight
from models.Pawn import Pawn

class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

    def get_possible_moves(self):
        from models.GameBoard import game_board
        self.possible_moves = []
        for dx, dy in self.move_pattern:
            nx = self.position[0] + dx
            ny = self.position[1] + dy
            if not (0 <= nx < 8 and 0 <= ny < 8):
                continue
            if self.is_threatened((nx, ny)):
                continue
            target = game_board.board[nx][ny]
            if target is None or target.color != self.color:
                self.possible_moves.append((nx, ny))
        return self.possible_moves

    def is_threatened(self, target_position):
        from models.GameBoard import game_board

        # Düz tehditler: Kale, Vezir, Şah
        linear_threats = [(0,1),(1,0),(0,-1),(-1,0)]
        for dx, dy in linear_threats:
            for step in range(1, 8):
                nx = target_position[0] + dx * step
                ny = target_position[1] + dy * step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                target = game_board.board[nx][ny]
                if target is None:
                    continue
                if target.color == self.color:
                    break
                if step == 1 and isinstance(target, King):
                    return True
                if isinstance(target, (Queen, Rook)):
                    return True
                break  # başka taş yolu kesiyor

        # Çapraz tehditler: Fil, Vezir, Şah, Piyon
        diagonal_threats = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for dx, dy in diagonal_threats:
            for step in range(1, 8):
                nx = target_position[0] + dx * step
                ny = target_position[1] + dy * step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                target = game_board.board[nx][ny]
                if target is None:
                    continue
                if target.color == self.color:
                    break
                if step == 1 and isinstance(target, King):
                    return True
                if step == 1 and isinstance(target, Pawn) and target.color != self.color:
                    expected_dir = 1 if target.color == "black" else -1  
                    if -dx == expected_dir:
                       return True
                    break
                if isinstance(target, (Queen, Bishop)):
                    return True
                break  # başka taş yolu kesiyor

        # At tehdidi
        L_threats = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for dx, dy in L_threats:
            nx = target_position[0] + dx
            ny = target_position[1] + dy
            if not (0 <= nx < 8 and 0 <= ny < 8):
                continue
            target = game_board.board[nx][ny]
            if target is not None and target.color != self.color and isinstance(target, Knight):
                return True

        return False

