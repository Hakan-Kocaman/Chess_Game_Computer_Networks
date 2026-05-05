
import os
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QStackedWidget
from PySide6.QtUiTools import QUiLoader
import socket
from frame import Frame
from requests import move_request

import pickle

class Connect:

    

    def __init__(self):
        self.app = QApplication(sys.argv)

        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), "connectscreen.ui")
        self.window = loader.load(ui_path)

        self.stack = QStackedWidget()
        self.stack.setWindowTitle("Ag Laboratuvari - Satranc")
        self.stack.resize(800, 600)

        self.play_screen= Frame()

        self.stack.addWidget(self.window)                       #Stack yapisina iki ekran da eklendi 
        self.stack.addWidget(self.play_screen.window)

        self.button=QPushButton()
        self.button=self.window.pushButton
        self.button.clicked.connect(self.connect_pressed)
        self.username = ""
        self.server_ip = ""
        self.stack.setCurrentIndex(0)

    def connect_pressed(self):
            server_ip=self.window.lineEdit.text()
            username=self.window.lineEdit_2.text()
            server_port=5050


            if username =="":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: enter username")
                msg.setWindowTitle("Error")
                msg.exec()
            if server_ip == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: enter server ip")
                msg.setWindowTitle("Error")
                msg.exec()

            
            
            
            try :
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        
                self.socket.connect((server_ip, server_port)) 
                        
                    
                print(f"[CLIENT] Connected to server {server_ip}:{server_port}") 
                print(f"[CLIENT] Servera baglanildi {server_ip}:{server_port}") 
                print() 
                            
                #ilk paket hazirlanip gonderiliyor
                connection_packet=move_request(
                    URL="/login",
                    sender=self.username,
                    selected_piece=None,
                    new_position=None
                    )
                pickled_packet=pickle.dumps(connection_packet)
                self.socket.send(pickled_packet)
                print(f"[CLIENT] Login isteği gönderildi: Oyuncu -> {self.username}")
                
                #Serverdan onay cevabi bekleniyor
                received_pickle=self.socket.recv(1024)
                server_response=pickle.loads(received_pickle)
                if server_response["type"] == "game_start":
                    print("[CLIENT] Erişim onaylandi! Tahtaya geçiliyor...")
                    self.stack.setCurrentIndex(1)

                    starter_game_board=server_response["game_board"]

                    self.play_screen.load_board(starter_game_board)

                    self.play_screen.move_signal.connect(self.send_move)
                    self.play_screen.possible_moves_signal.connect(self.send_possible_moves_request)


                else:
                    print("[CLIENT] Sunucu erişimi reddetti.")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Sunucu erişimi reddetti.")
                    msg.setWindowTitle("Reddedildi")
                    msg.exec()
                            

            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: cannot connected")
                msg.setWindowTitle("Error")
                msg.exec()



    def send_move(self, from_x,from_y,to_x,to_y):

        #Pozisyon tuple olarak gonderiliyor ama server tarafinda position kullanilmis buna karar verilecek############################

        request=move_request(
            URL="move",
            sender=self.username,
            selected_piece=from_x,
            new_position=to_x
        )
        self.socket.sendall(pickle.dumps(request))
                
    def send_possible_moves_request(self):
        pass
            

                



if __name__ == "__main__":
    game = Connect()
    game.stack.show() 
    sys.exit(game.app.exec())



class messagethread:
    def __init__(self, soket):
        super().__init__()
        self.soket = soket
    
    def run(self):
        while True:
            try:
                received_pickle=self.socket.recv(1024)
                received_packet=pickle.loads(received_pickle)
            except:
                pass