
    # Piyon Class
from ChessPiece import ChessPiece, game_board


class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_pattern = [(0, 1), (0, 2)]
        self.attacking_pattern = [(-1, 1), (1, 1)]
        if color == "black":
            self.move_pattern = self.move_pattern * -1  # Siyah piyonlar aşağı hareket eder
            self.attacking_pattern = self.attacking_pattern * -1  # Siyah piyonlar çapraz aşağı saldırır
        self.FirstMove = True  # Piyonun ilk hamlesi 

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
                    self.possible_moves.append((nx, ny))  # boş kare ve dur
                    break
                else:
                    break  # taş, dur 
        for dx, dy in self.attacking_pattern:
            nx = self.position[0] + dx
            ny = self.position[1] + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = game_board[nx][ny]
                if target is not None and target.color != self.color:
                    self.possible_moves.append((nx, ny))  # düşman ye, dur

        return self.possible_moves
    
    def move(self, new_position):
        if self.possible_moves == None:
            self.possible_moves = self.get_possible_moves()
       
        if new_position in self.possible_moves:
            if self.FirstMove:
                self.FirstMove = False
            if game_board[new_position[0]][new_position[1]] is not None:
                # Taş yeniyor, tahtadan kaldır
                game_board[new_position[0]][new_position[1]].die()
            self.position = new_position
            self.possible_moves = None  # Hamle yapıldı, olası hamleler sıfırlandı

    def die(self):
        self = None  # Taş öldü, referansı kaldır