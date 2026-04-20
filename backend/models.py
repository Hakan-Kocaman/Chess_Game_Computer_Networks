from abc import ABC, abstractmethod

game_board = [[None for _ in range(8)] for _ in range(8)]
     # Abstract Taş Class
class ChessPiece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.move_pattern = None
        self.possible_moves = []
    def get_possible_moves(self, player_color):
        pass

    # Piyon Class
class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(0, 1), (0, 2),(1, 1),(-1, 1)]  # Piyon sadece ileri hareket eder
        self.FirstMove = True  # Piyonun ilk hamlesi 

    def get_possible_moves(self,player_color):
        self.possible_moves.clear()
        for dx, dy in self.move_pattern:
            for step in range(1, 8):
                nx = self.position[0] + dx * step
                ny = self.position[1] + dy * step
            
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
            
                target = game_board[nx][ny]
            
                if target is None:
                    self.possible_moves.append((nx, ny))  # boş kare ve dur
                    break
                elif target.color != player_color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur
                    break
                else:
                    break  # kendi taşı, dur 
        return self.possible_moves
        
    # At Class    
class Knight(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]  # Atın hareket paterni

    def get_possible_moves(self, player_color):
        self.possible_moves.clear()
        for dx, dy in self.move_pattern:
            for step in range(1, 8):
                 nx = self.position[0] + dx * step
                 ny = self.position[1] + dy * step
            
                 if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
            
                 target = game_board[nx][ny]
            
                 if target is None:
                    self.possible_moves.append((nx, ny))  # boş kare ve dur
                    break
                 elif target.color != player_color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur
                    break
                 else:
                    break  # kendi taşı, dur
        return self.possible_moves

    # Fil Class
class Bishop(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Fil çapraz hareket eder
    
    def get_possible_moves(self, player_color):
        self.possible_moves.clear()
        for dx, dy in self.move_pattern:
            for step in range(1, 8):
                nx = self.position[0] + dx * step
                ny = self.position[1] + dy * step
            
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
            
                target = game_board[nx][ny]
            
                if target is None:
                    self.possible_moves.append((nx, ny))  # boş kare devam
                    
                elif target.color != player_color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur
                    break
                else:
                    break  # kendi taşı, dur
        return self.possible_moves

        

    # Kale Class
class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Kale düz hareket eder
    
    def get_possible_moves(self, player_color):
        self.possible_moves.clear()
        for dx, dy in self.move_pattern:
            for step in range(1, 8):
                nx = self.position[0] + dx * step
                ny = self.position[1] + dy * step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
                target = game_board[nx][ny]
                if target is None:
                    self.possible_moves.append((nx, ny))  # boş kare devam
                elif target.color != player_color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur
                    break
                else:
                    break  # kendi taşı, dur
        return self.possible_moves

    # Vezir Class
class Queen(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Vezir hem düz hem çapraz hareket eder
    
    def get_possible_moves(self, player_color):
        self.possible_moves.clear()
        for dx, dy in self.move_pattern:
            for step in range(1, 8):
                nx = self.position[0] + dx * step
                ny = self.position[1] + dy * step
            
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
            
                target = game_board[nx][ny]
            
                if target is None:
                    self.possible_moves.append((nx, ny))  # boş kare devam
                    
                elif target.color != player_color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur
                    break
                else:
                    break  # kendi taşı, dur
        return self.possible_moves

    # Şah Class
class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Şah hem düz hem çapraz hareket eder
    
    def get_possible_moves(self, player_color):
        self.possible_moves.clear()
        for dx, dy in self.move_pattern:
            for step in range(1, 8):
                nx = self.position[0] + dx * step
                ny = self.position[1] + dy * step
            
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
            
                target = game_board[nx][ny]
            
                if target is None:
                    self.possible_moves.append((nx, ny))  # boş kare ve dur
                    break

                elif target.color != player_color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur
                    break
                else:
                    break  # kendi taşı, dur
        return self.possible_moves
    
