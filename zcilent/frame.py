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
        self.server_game_board=[]
        self.buttons=[]
        self.playedbuttons=[]
        self.last_higlighted_buttons=[]
        self.last_white_king_btn=None
        self.last_black_king_btn=None
        
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
        if self.my_color=="white":
            self.myturn=True
        else:
            self.myturn=False
        for i in range(8):
            row=[]
            for j in range(8):
                btn=QPushButton("")
                btn.setFixedSize(60,60)
                btn.setIconSize(btn.size())
                btn.setProperty("row",i)
                btn.setProperty("col",j)
                val_x = btn.property("row")
                val_y = btn.property("col")
                print(f"set:{i},{j} → get:{val_x},{val_y}")
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
        print(clicked.property("piece"))
        print(self.myturn)

        #ikinci tiklamaysa fonksiyonu cagir
        if self.selected_button is not None:
            self.second_on_click(clicked=clicked,piece=piece)
            return
        #1. tiklama

        #sira bu clientte degilse gec
        if self.myturn == False:
            return
        #Bos kareye tiklandiysa gec
        if (piece == "·" or piece is None):
            return
        
        
        
        if self.my_color=="white" and piece in ["♜","♞","♝","♛","♚","♟"]:
            return
        if self.my_color=="black" and piece in ["♖","♘","♗","♕","♔","♙"]:
            return
            
        self.selected_button=clicked
        self.put_border(clicked)
            
        self.get_request_possible_moves(self.selected_button)       ################################################################
        #2. tiklama
       

    def second_on_click(self,clicked,piece):
            #2. tiklama ayni butona tiklandiysa secimi iptal et
            if clicked==self.selected_button:
                self.remove_border(clicked)
                self.selected_button=None
                
                self.clear_highlights()            ################################################################
                return
            
            



            #2. tiklamada bos kareye tiklamadiysa kendi baska bir tasina tikladiysa digerini sec 
            if self.my_color=="white" and piece in ["♖","♘","♗","♕","♔","♙"]:
                self.remove_border(self.selected_button)

                self.clear_highlights()

                self.selected_button = clicked
                self.put_border(clicked)
                self.get_request_possible_moves(clicked)
                return
            if self.my_color=="black" and piece in ["♜","♞","♝","♛","♚","♟"]:
                self.remove_border(self.selected_button)

                self.clear_highlights()

                self.selected_button = clicked
                self.put_border(clicked)
                self.get_request_possible_moves(clicked)
                return
            

            #2.tiklamada possible_moves dan baska yere tiklarsa
            row=clicked.property("row")
            col=clicked.property("col")
            if (row,col) not in self.last_higlighted_buttons:
                print("hamle yapilamadi")
                self.remove_border(self.selected_button)
                self.selected_button = None
                self.clear_highlights()
                return
                
            
                
            #Tum kontrollerden sonra hamleyi servera gonder    
            self.send_move(self.selected_button, clicked)
            self.remove_border(self.selected_button)
            self.selected_button = None
            self.clear_highlights()
        

        


    def get_request_possible_moves(self,from_button):
        from_x=from_button.property("row")
        from_y=from_button.property("col")
        self.possible_moves_signal.emit(from_x,from_y)
        

    def send_move(self, from_button, to_button):
        from_x=from_button.property("row")
        from_y=from_button.property("col")
        to_x=to_button.property("row")
        to_y=to_button.property("col")
        self.playedbuttons=[from_x,from_y,to_x,to_y]
        self.move_signal.emit(from_x,from_y,to_x,to_y)



    def put_border(self,button):
        x=int(button.property("row"))
        y=int(button.property("col"))
        print(f"x:{x} y:{y} (x+y)%2={(x+y)%2}")
        color=None
        if(x+y)%2==0:
            button.setStyleSheet(f"""background-color: #eeeed2;border: 4px solid red;""")
            color = "#eeeed2"
        else:
            color = "#769656"
            button.setStyleSheet(f"""background-color: #769656;border: 4px solid red;""")
        print(color)
        
    def remove_border(self,button):
        x=int(button.property("row"))
        y=int(button.property("col"))
        color=None
        if(x+y)%2==0:
            color = "#eeeed2"
        else:
            color = "#769656"
        button.setStyleSheet(f"""background-color: {color};border: none;""")
    
    def highlight_moves(self, moves):
        self.last_higlighted_buttons=[(int(x), int(y)) for (x, y) in moves]
        for (x, y) in self.last_higlighted_buttons:
            self.buttons[x][y].setStyleSheet(
                "background-color: #f6f669; border: none;"
            )
    def clear_highlights(self):
        for (x, y) in self.last_higlighted_buttons:
            if (x + y) % 2 == 0:
                self.buttons[x][y].setStyleSheet("background-color: #eeeed2; border: none;")
            else:
                self.buttons[x][y].setStyleSheet("background-color: #769656; border: none;")
        self.last_higlighted_buttons=[]

    

    def handle_turn(self,is_myturn):
        self.myturn=is_myturn
        

    def handle_chat(self,user,message):
        self.window.textEdit.append(f"{user}: {message}")


    def load_board(self,server_game_board):
        self.server_game_board=server_game_board
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



    #move_result = "capture "+game_board[new_position[0]][new_position[1]].color+ " "+game_board[new_position[0]][new_position[1]].__class__.__name__
    def update_board(self,str1):
        parts = str1.split()

        if (str=="fail"):
            if self.myturn:
                QMessageBox.warning(self.window, "Unsuccesfull move", "Unsuccesfull move")
            return
        oldx=int()
        oldy=int()
        newx=int()
        newy=int()
        self.playedbuttons[0]=oldx
        self.playedbuttons[1]=oldy
        self.playedbuttons[2]=newx
        self.playedbuttons[3]=newy
        
        self.remove_border(self.last_white_king_btn)
        self.remove_border(self.last_black_king_btn)
        
        

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
            for row in range(8):
                for col in range(8):
                    if self.my_color=="white":
                        if self.server_game_board[row][col]=="♔":
                            self.last_white_king_btn=self.buttons[row][col]
                            self.put_border(self.last_white_king_btn)
                    if self.my_color=="black":
                        if self.server_game_board[row][col]=="♚":
                            self.last_black_king_btn=self.buttons[row][col]
                            self.put_border(self.last_white_black_btn)
        if self.myturn==False and str=="checkmate":
            QMessageBox.warning(self.window, "Checkmate", "Game over")
            for row in range(8):
                for col in range(8):
                    if self.my_color=="white":
                        if self.server_game_board[row][col]=="♔":
                            self.last_white_king_btn=self.buttons[row][col]
                            self.put_border(self.last_white_king_btn)
                    if self.my_color=="black":
                        if self.server_game_board[row][col]=="♚":
                            self.last_black_king_btn=self.buttons[row][col]
                            self.put_border(self.last_black_king_btn)
        oldbutton=self.buttons[oldx][oldy]
        newbutton=self.buttons[newx][newy]

        newbutton.setProperty("piece", oldbutton.property("piece"))
        oldbutton.setProperty("piece",None)
        self.buttons[oldx][oldy].setIcon(QIcon())
        self.buttons[newx][newy].setIcon(self.piece_icons[newbutton.property("piece")])






    def chat_on_click(self):
        message=self.line_edit.text().strip()
        if message!="":
            self.chat_signal.emit(message)



