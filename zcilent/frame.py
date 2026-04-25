import os
import sys
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtUiTools import QUiLoader





class App:



    def __init__(self):
        self.app = QApplication(sys.argv)

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
        for i in range(8):
            row=[]
            for j in range(8):
                btn=QPushButton(f"button{row_dict.get(j)}{i+1}")
                btn.setFixedSize(60,60)
                btn.setProperty("x",row_dict.get(j))
                btn.setProperty("y",i+1)

                #Tasin turunu belirleme kontrolu
                if i == 1 or i==6:
                    btn.setProperty("piece","pawn")
                elif i==0 or i==7:
                    btn.setProperty("piece",piece_order[j])
                else:
                    btn.setProperty("piece","empty")


                #Tasin rengini belirleme kontrolu
                if i==0 or i==1:
                    btn.setProperty("color","white")
                elif i==6 or i==7:
                    btn.setProperty("color","black")
                else:
                    btn.setProperty("color","none")
                
                #Karenin rengini belirleme kontrolu
                if (i + j) % 2 == 0:
                    btn.setProperty("square_color","White")
                else:
                    btn.setProperty("square_color","Black")
                
                btn.clicked.connect(self.on_click)
                self.window.gridLayout_4.addWidget(btn,7 - j,i)
                row.append(btn)
            self.buttons.append(row)

        


    def on_click(self):
        pass
        





game = App()
game.window.show()
game.app.exec()