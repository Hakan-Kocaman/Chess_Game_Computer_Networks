import os
import sys
from PySide6.QtWidgets import QApplication, QLineEdit, QMessageBox, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, QObject





class Frame(QObject):
    ## Signal slot mantigi ui da yapilan hamlenin soket ile servera gonderilebilmesi icin
    move_signal = Signal(int, int, int, int)
    possible_moves_signal = Signal(int, int)
    chat_signal=Signal(str)



    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), "main.ui")

        self.window = loader.load(ui_path)

        self.my_color=None
        self.myturn=False
        self.selected_button=None

        self.starter_board=[]

        self.buttons=[]
        self.playedbuttons=[]
        self.last_higlighted_buttons=[]
        self.row_dict = {
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
        self.window.gridLayout_4.setSpacing(0)
        self.window.gridLayout_4.setContentsMargins(0, 0, 0, 0)

        self.chat_button=QPushButton("")
        self.chat_button=self.window.pushButton
        self.chat_button.clicked.connect(self.chat_on_click)

        self.line_edit=QLineEdit("")
        self.line_edit=self.window.lineEdit

       
        
    def create_buttons(self,my_color):
         self.my_color=my_color
         for i in range(8):
            row=[]
            for j in range(8):
                btn=QPushButton("")
                btn.setFixedSize(60,60)
                btn.setIconSize(btn.size())
                btn.setProperty("x",i)
                btn.setProperty("y",j)
                btn.setProperty("notation",f"{self.row_dict.get(j)}{8 - i}")
                
                btn.setText("")                                                 #Isimleri kaldir
                if (i + j) % 2 == 0:
                    btn.setStyleSheet("background-color: #eeeed2; border: none;")
                else:
                    btn.setStyleSheet("background-color: #769656; border: none;")   #Karelerin rengini belirle

                btn.clicked.connect(self.on_click)
                if self.my_color == "white":
                    self.window.gridLayout_4.addWidget(btn, i, j)
                else:
                    self.window.gridLayout_4.addWidget(btn, 7 -i, 7 -j)
                row.append(btn)
            self.buttons.append(row)

   
        
        


    def on_click(self):
        clicked=self.sender()
        piece=clicked.property("piece")
        print(clicked.property("notation"))
        
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
            self.get_request_possible_moves(self.selected_button)       ################################################################
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
                    self.get_request_possible_moves(clicked)
                    return
                if self.my_color == "black" and piece in ["♜","♞","♝","♛","♚","♟"]:
                    self.clear_highlights()
                    self.selected_button = clicked
                    clicked.setStyleSheet("background-color: #f6f669; border: none;")
                    self.get_request_possible_moves(clicked)
                    return
                #Tum kontrollerden sonra hamleyi servera gonder
                
                self.send_move(self.selected_button, clicked)
                self.clear_highlights()
                self.selected_button = None

        


    def get_request_possible_moves(self,from_button):
        from_x=from_button.property("x")
        from_y=from_button.property("y")
        self.possible_moves_signal.emit(from_x,from_y)
        

    def send_move(self, from_button, to_button):
        from_x=from_button.property("x")
        from_y=from_button.property("y")
        to_x=to_button.property("x")
        to_y=to_button.property("y")
        self.playedbuttons=[from_x,from_y,to_x,to_y]
        self.move_signal.emit(from_x,from_y,to_x,to_y)




    def highlight_moves(self, moves):
        self.last_higlighted_buttons=moves
        for (x, y) in moves:
            self.buttons[x][y].setStyleSheet(
                "background-color: #f6f669; border: none;"
            )
    def clear_highlights(self):
        for (x, y) in self.last_higlighted_buttons:
            if (x + y) % 2 == 0:
                self.buttons[x][y].setStyleSheet("background-color: #eeeed2; border: none;")
            else:
                self.buttons[x][y].setStyleSheet("background-color: #769656; border: none;")

    

    def handle_turn(self,is_myturn):
        self.myturn=is_myturn
        

    def handle_chat(self,user,message):
        self.window.textEdit.append(f"{user}: {message}")


    def load_board(self,server_game_board):
        for i in range(8):
            for j in range(8):
                button=self.buttons[i][j]
                button.setProperty("piece",server_game_board[i][j])
                if server_game_board[i][j] in self.piece_icons:
                    if self.piece_icons[server_game_board[i][j]] !=None:
                        button.setIcon(QIcon(self.piece_icons[server_game_board[i][j]]))
                    else:
                        button.setIcon(QIcon())
                else:
                    button.setIcon(QIcon())
        print(f"color:{self.my_color}")

    def update_board(self,str):
        oldx=int()
        oldy=int()
        newx=int()
        newy=int()
        self.playedbuttons[0]=oldx
        self.playedbuttons[1]=oldy
        self.playedbuttons[2]=newx
        self.playedbuttons[3]=newy
        
        if (str=="fail") and self.myturn:
            QMessageBox.warning(self.window, "Unsuccesfull move", "Unsuccesfull move")


        

        oldbutton=self.buttons[oldx][oldy]
        newbutton=self.buttons[newx][newy]

        newbutton.setProperty("piece", oldbutton.property("piece"))
        oldbutton.setProperty("piece",None)
        self.buttons[oldx][oldy].setIcon(QIcon())
        self.buttons[newx][newy].setIcon(self.piece_icons[newbutton.property("piece")])


        ##BURAYA GERIYE HAMLENIN NOTASYONU DONDURULEBILIR

    def update_board_with_check(self,str):
        oldx=int()
        oldy=int()
        newx=int()
        newy=int()
        self.playedbuttons[0]=oldx
        self.playedbuttons[1]=oldy
        self.playedbuttons[2]=newx
        self.playedbuttons[3]=newy

        if self.myturn==False and str=="check":
            QMessageBox.warning(self.window, "Check", "You have been checked")
        if self.myturn==False and str=="checkmate":
            QMessageBox.warning(self.window, "Checkmate", "Game over")
        oldbutton=self.buttons[oldx][oldy]
        newbutton=self.buttons[newx][newy]

        newbutton.setProperty("piece", oldbutton.property("piece"))
        oldbutton.setProperty("piece",None)
        self.buttons[oldx][oldy].setIcon(QIcon())
        self.buttons[newx][newy].setIcon(self.piece_icons[newbutton.property("piece")])






    def chat_on_click(self):
        message=self.line_edit.text().strip()
        if message!="":
            self.chat_signal(message)



