import os
import sys
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, QObject





class Frame(QObject):
    ## Signal slot mantigi ui da yapilan hamlenin soket ile servera gonderilebilmesi icin
    move_signal = Signal(str, int, str, int)
    possible_moves_signal = Signal(str, int)



    def __init__(self):
        self.app = QApplication(sys.argv)

        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), "main.ui")

        self.window = loader.load(ui_path)

        self.my_color=None
        self.myturn=False
        self.selected_button=None

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
                btn.setProperty("x",7 - j)
                btn.setProperty("y",i)
                
                btn.setText("")                                                 #Isimleri kaldir
                btn.setStyleSheet("background-color: #769656; border: none;")   #Karelerin rengini belirle

                btn.clicked.connect(self.on_click)
                self.window.gridLayout_4.addWidget(btn,7 - j,i)
                row.append(btn)
            self.buttons.append(row)

        


    def on_click(self):
        clicked=self.sender()
        piece=clicked.property("piece")
        
        #Bos kareye tiklandiysa veya sira bu clientte degilse gec
        if piece=="." or piece==None and self.myturn==False:
            return
        
        if self.selected_button==None:
            if self.my_color=="white" and piece in ["♜","♞","♝","♛","♚","♟"]:
                return
            if self.my_color=="black" and piece in ["♖","♘","♗","♕","♔","♙"]:
                return
            
            self.selected_button=clicked
            clicked.setStyleSheet("background-color: #f6f669; border: none;")
            self.get_request_possible_moves()       ################################################################
        #2. tiklama
        else:
            #2. tiklama ayni butona tiklandiysa secimi iptal et
            if clicked==self.selected_button:
                self.selected_button=None
                self.clear_highlights()            ################################################################
            if piece != "·" and piece != None:
                #2.tiklama kendi baska bir tasina ise secilen tasi degistir
                if self.my_color == "white" and piece in ["♖","♘","♗","♕","♔","♙"]:
                    self.clear_highlights()
                    self.selected_button = clicked
                    clicked.setStyleSheet("background-color: #f6f669; border: none;")
                    self.request_possible_moves(clicked)
                    return
                if self.my_color == "black" and piece in ["♜","♞","♝","♛","♚","♟"]:
                    self.clear_highlights()
                    self.selected_button = clicked
                    clicked.setStyleSheet("background-color: #f6f669; border: none;")
                    self.request_possible_moves(clicked)
                    return
                #Tum kontrollerden sonra hamleyi servera gonder
                self.send_move(self.selected_button, clicked)
                self.clear_highlights()
                self.selected_button = None

        


    def get_request_possible_moves(self):
        pass
    def clear_highlights(self):
        pass
    def send_move(self, from_button, to_button):
        from_x=from_button.property("x")
        from_y=from_button.property("y")
        to_x=to_button.property("x")
        to_y=to_button.property("y")
        self.move_signal.emit(from_x,from_y,to_x,to_y)



    def load_board(self,server_game_board):
        for i in range(8):
            for j in range(8):
                button=self.buttons[i][j]
                button.setProperty("piece",server_game_board[i][j])
                if server_game_board[i][j] in self.piece_icons:
                    button.setIcon(QIcon(self.piece_icons[server_game_board[i][j]]))
                else:
                    button.setIcon(QIcon())

    def update_board(self,oldx,oldy,newx,newy):
        oldbutton=self.buttons[oldx][oldy]
        newbutton=self.buttons[newx][newy]

        newbutton.setProperty("piece", oldbutton.property("piece"))
        oldbutton.setProperty("piece",None)
        self.buttons[oldx][oldy].setIcon(QIcon())
        self.buttons[newx][newy].setIcon(self.piece_icons[newbutton.property("piece")])


        ##BURAYA GERIYE HAMLENIN NOTASYONU DONDURULEBILIR

