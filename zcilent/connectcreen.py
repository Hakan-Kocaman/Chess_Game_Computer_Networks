
import os
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QStackedWidget
from PySide6.QtUiTools import QUiLoader
import socket

from PySide6.QtCore import QThread, Signal
from frame import Frame
from requestss import request, move_request_body,get_possible_moves_request_body,chat_request_body


import pickle

class Connect:

    

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.play_screen= Frame()
        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), "connectscreen.ui")
        self.window = loader.load(ui_path)

        self.stack = QStackedWidget()
        self.stack.setWindowTitle("Ag Laboratuvari - Satranc")
        self.stack.resize(800, 600)

        

        self.stack.addWidget(self.window)                       #Stack yapisina iki ekran da eklendi 
        self.stack.addWidget(self.play_screen.window)

        self.button=QPushButton()
        self.button=self.window.pushButton
        self.button.clicked.connect(self.connect_pressed)
        self.username = ""
        self.server_ip = ""
        self.stack.setCurrentIndex(0)

    def connect_pressed(self):
            server_ip=self.window.lineEdit_2.text().strip()
            username=self.window.lineEdit.text().strip()
            server_port=5050
            print(f"IP: '{server_ip}'")  # tırnaklar arasında ne var gör
            print(f"Username: '{username}'")

            if username =="":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: enter username")
                msg.setWindowTitle("Error")
                msg.exec()
                return
            if server_ip == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: enter server ip")
                msg.setWindowTitle("Error")
                msg.exec()
                return

            
            
            
            try :
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        
                self.socket.connect((server_ip, server_port)) 
                        
                    
                print(f"[CLIENT] Connected to server {server_ip}:{server_port}") 
                print(f"[CLIENT] Servera baglanildi {server_ip}:{server_port}") 
                print() 
                            
                #ilk paket hazirlanip gonderiliyor
                connection_packet=request(URL="/login",sender=self.username,body=None)
                pickled_packet=pickle.dumps(connection_packet)
                self.socket.sendall(pickled_packet)
                print(f"[CLIENT] Login isteği gönderildi: Oyuncu -> {self.username}")
                
                #Serverdan onay cevabi bekleniyor
                received_pickle=self.socket.recv(1024)
                server_response=pickle.loads(received_pickle)
                if server_response["type"] == "game_start":
                    print("[CLIENT] Erişim onaylandi! Tahtaya geçiliyor...")
                    self.stack.setCurrentIndex(1)

                    starter_game_board=server_response["game_board"]
                    self.play_screen.my_color=server_response["color"]
                    self.play_screen.myturn=server_response["your_turn"]
                    

                    self.play_screen.load_board(starter_game_board)

                    self.play_screen.move_signal.connect(self.send_move)
                    self.play_screen.possible_moves_signal.connect(self.send_possible_moves_request)



                                    # thread başlat
                    self.msg_thread = messagethread(self.socket,self.username)
                    self.msg_thread.possible_moves_received.connect(self.play_screen.highlight_moves)
                    self.msg_thread.move_received.connect(self.play_screen.update_board)
                    self.msg_thread.turn_received.connect(self.play_screen.handle_turn)
                    self.msg_thread.chat_received.connect(self.play_screen.handle_chat)
                    self.msg_thread.start()
                                    ###############


                else:
                    print("[CLIENT] Sunucu erişimi reddetti.")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Sunucu erişimi reddetti.")
                    msg.setWindowTitle("Reddedildi")
                    msg.exec()
                            

            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Error: cannot connect\n\n{str(e)}")
                msg.setWindowTitle("Error")
                msg.exec()



    def send_move(self, from_x,from_y,to_x,to_y):

        #Pozisyon tuple olarak gonderiliyor ama server tarafinda position kullanilmis buna karar verilecek############################

        packet_body=move_request_body(selected_piece=(from_x,from_y),new_position=(to_x,to_y))
        packet= request(URL="move",sender=self.username,body=packet_body)
        self.socket.sendall(pickle.dumps(packet))
                
    def send_possible_moves_request(self,from_x,from_y):
        packet_body=get_possible_moves_request_body(selected_piece=(from_x,from_y))
        packet=request(URL="get_possible_moves",sender=self.username,body=packet_body)
        self.socket.sendall(pickle.dumps(packet))

    def send_chat(self,message_content):
        packet_body=chat_request_body(message=message_content)
        packet=request(URL="chat",sender=self.username,body=packet_body)
        self.socket.sendall(pickle.dumps(packet))
            

                







class messagethread(QThread):
    possible_moves_received = Signal(list)
    move_received = Signal(int,int,int,int)
    turn_received=Signal(bool)
    chat_received=Signal(str,str)

    
    def __init__(self, socket,username):
        super().__init__()
        self.socket = socket
        self.my_username=username

    
    
    def run(self):
        while True:
            try:
                received_pickle=self.socket.recv(1024)
                received_packet=pickle.loads(received_pickle)
                if received_packet.URL=="move":
                        if received_packet.move_result:
                            self.move_received.emit(received_packet.body.from_pos[0],
                                                    received_packet.body.from_pos[1],
                                                    received_packet.body.to_pos[0],
                                                    received_packet.body.to_pos[1])
                            
                        # sender ben miyim?
                        if received_packet.sender != self.my_username:
                            # rakip oynadı, sıra bende
                            self.turn_received.emit(True)
                        else:
                            # ben oynadım, sıra rakipte
                            self.turn_received.emit(False)

                elif received_packet.URL=="get_possible_moves":
                    self.possible_moves_received.emit(received_packet.body.possible_moves)

                elif received_packet.URL=="chat":
                    self.chat_received.emit(received_packet.sender,received_packet.body.message)
                    

            except:
                pass



if __name__ == "__main__":
    game = Connect()
    game.stack.show() 
    sys.exit(game.app.exec())