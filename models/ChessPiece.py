from abc import ABC, abstractmethod

import sys
import os
sys.path.append(os.path.dirname(__file__)) 


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

        new_position = (int(new_position[0]), int(new_position[1]))

        if new_position in possible_moves:
            pos_title = f"{self.position[0]},{self.position[1]},{new_position[0]},{new_position[1]}"
            move_result = "move," + pos_title + "," + self.color

            if game_board.board[new_position[0]][new_position[1]] is not None:
                move_result = "capture," + pos_title + "," + self.color
                game_board.board[new_position[0]][new_position[1]].die()

            game_board.board[self.position[0]][self.position[1]] = None
            self.position = new_position
            game_board.board[self.position[0]][self.position[1]] = self

            if isinstance(self, Pawn):
                self.first_move = False

            possible_moves = self.get_possible_moves()

            found_king = False
            for row in game_board.board:
                for chesspiece in row:
                    if isinstance(chesspiece, King) and chesspiece.color != self.color:
                        found_king = True
                        if chesspiece.position in possible_moves:
                            move_result = "check," + pos_title + "," + self.color
                            if not chesspiece.get_possible_moves() and self.is_checkmate(chesspiece):
                                move_result = "checkmate," + pos_title + "," + self.color
                        break
                if found_king:
                    break
    # move_result olası değerler:
    # "unsuccessful move"                          → hamle geçersiz (possible moves dışı)
    # "move,fx,fy,tx,ty,color"                     → normal hamle
    # "capture,fx,fy,tx,ty,color"                  → düşman taş yendi
    # "check,fx,fy,tx,ty,color"                    → rakip şah altında
    # "checkmate,fx,fy,tx,ty,color"                → rakip mat, oyun bitti

        return move_result

    def is_checkmate(self, king):
        from models.GameBoard import game_board

        # Şahın hamlesi varsa mat değil
        if king.get_possible_moves():
            return False

        # Dost taşlardan biri şahı kurtarabilir mi?
        for row in game_board.board:
            for piece in row:
                if piece is None or piece.color != king.color or piece is king:
                    continue
                for move in piece.get_possible_moves():
                    # Hamleyi simüle et
                    original_pos = piece.position
                    target_piece = game_board.board[move[0]][move[1]]

                    game_board.board[original_pos[0]][original_pos[1]] = None
                    game_board.board[move[0]][move[1]] = piece
                    piece.position = move

                    still_in_check = king.is_threatened(king.position)

                    # Geri al
                    game_board.board[move[0]][move[1]] = target_piece
                    game_board.board[original_pos[0]][original_pos[1]] = piece
                    piece.position = original_pos

                    if not still_in_check:
                        return False  # Bu hamle şahı kurtarıyor

        return True  # Hiçbir şey şahı kurtaramıyor → mat

    def die(self):
        from models.GameBoard import game_board
        game_board.board[self.position[0]][self.position[1]] = None