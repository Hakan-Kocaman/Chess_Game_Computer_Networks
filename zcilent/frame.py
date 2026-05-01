import os
import sys
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon





class App:



    def __init__(self):
        

        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), "main.ui")
        self.window = loader.load(ui_path)

        self.buttons=[]
        row_dict = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h",
        }
        piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

        self.piece_icons = {
        # Siyah Taşlar
        "♜": "zcilent/chess_pieces_pngs/black-rook.png",
        "♞": "zcilent/chess_pieces_pngs/black-knight.png",
        "♝": "zcilent/chess_pieces_pngs/black-bishop.png",
        "♛": "zcilent/chess_pieces_pngs/black-queen.png",
        "♚": "zcilent/chess_pieces_pngs/black-king.png",
        "♟": "zcilent/chess_pieces_pngs/black-pawn.png",
        
        # Beyaz Taşlar
        "♖": "zcilent/chess_pieces_pngs/white-rook.png",
        "♘": "zcilent/chess_pieces_pngs/white-knight.png",
        "♗": "zcilent/chess_pieces_pngs/white-bishop.png",
        "♕": "zcilent/chess_pieces_pngs/white-queen.png",
        "♔": "zcilent/chess_pieces_pngs/white-king.png",
        "♙": "zcilent/chess_pieces_pngs/white-pawn.png",
        
        # Boş Kare
        "·": None, 
        ".": None
        }


        for i in range(8):
            row=[]
            for j in range(8):
                btn=QPushButton(f"button{row_dict.get(j)}{i+1}")
                btn.setFixedSize(60,60)
                btn.setProperty("x",row_dict.get(j))
                btn.setProperty("y",i+1)
                
                btn.clicked.connect(self.on_click)
                self.window.gridLayout_4.addWidget(btn,7 - j,i)
                row.append(btn)
            self.buttons.append(row)

        


    def on_click(self):
        pass

    def load_board(self,server_game_board):
        for i in range(8):
            for j in range(8):
                button=self.buttons[i][j]
                button.setProperty("piece",server_game_board[i][j])
                if server_game_board[i][j] in self.piece_icons:
                    button.setIcon(QIcon(self.piece_icons[server_game_board[i][j]]))
                else:
                    button.setIcon(QIcon())

        





