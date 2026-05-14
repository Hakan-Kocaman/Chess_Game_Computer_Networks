
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import os
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QStackedWidget
from PySide6.QtUiTools import QUiLoader
import socket

from PySide6.QtCore import QThread, Signal
from frame import Frame
from dtos.client_requests import move_request,chat_request,get_possible_moves_request


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
        self.button.setText("Connect")
        self.button.clicked.connect(self.connect_pressed)
        self.my_color=None
        self.myturn={"myturn":None}
        self.id = None
        self.server_ip = ""
        self.stack.setCurrentIndex(0)

    def connect_pressed(self):
            server_ip=self.window.lineEdit_2.text().strip()
            print(server_ip)
            server_port=5050
            print(f"IP: '{server_ip}'")  # tırnaklar arasında ne var gör

            if server_ip == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: enter server ip")
                msg.setWindowTitle("Error")
                msg.exec()
                return

            # Eski thread sinyallerini kes, sonra durdur
            if hasattr(self, 'msg_thread'):
                try:
                    self.msg_thread.possible_moves_received.disconnect()
                    self.msg_thread.move_received.disconnect()
                    self.msg_thread.turn_received.disconnect()
                    self.msg_thread.chat_received.disconnect()
                    self.msg_thread.check_received.disconnect()
                    self.msg_thread.connection_lost.disconnect()
                except Exception:
                    pass
                if self.msg_thread.isRunning():
                    self.msg_thread.quit()
                    self.msg_thread.wait(2000)

            # Eski socket'i kapat
            if hasattr(self, 'socket'):
                try:
                    self.socket.close()
                except Exception:
                    pass
            # Sinyalleri bir kez bağlamak için flag
            if not hasattr(self, '_signals_connected'):
                self.play_screen.move_signal.connect(self.send_move)
                self.play_screen.possible_moves_signal.connect(self.send_possible_moves_request)
                self.play_screen.chat_signal.connect(self.send_chat)
                self.play_screen.stackwidget_signal.connect(lambda: self.stack.setCurrentIndex(0))
                self.play_screen.replay_signal.connect(self.connect_pressed)
                self._signals_connected = True
            
            
            try :
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        
                self.socket.connect((server_ip, server_port)) 
                        
                    
                print(f"[CLIENT] Connected to server {server_ip}:{server_port}") 
                print(f"[CLIENT] Servera baglanildi {server_ip}:{server_port}") 
                print() 
                            
                
                
                #Serverdan onay (initial packet) cevabi bekleniyor
                received_pickle=self.socket.recv(4096)
                server_response=pickle.loads(received_pickle)
                if server_response["URL"] == "initial":
                    print("[CLIENT] Erişim onaylandi! Tahtaya geçiliyor...")
                    self.stack.setCurrentIndex(1)
                    self.my_color=server_response["player_color"]
                    self.id=server_response["player_id"]
                    starter_game_board=server_response["game_board"]
                    if server_response["state"] == "game":
                        self.play_screen.game_started = True
                    
                    self.play_screen.create_buttons(self.my_color,self.id)

                    self.play_screen.load_board(starter_game_board)

                    



                                    # thread başlat
                    self.msg_thread = messagethread(self.socket,self.id)
                    self.msg_thread.possible_moves_received.connect(self.play_screen.highlight_moves)
                    self.msg_thread.move_received.connect(self.play_screen.update_board)
                    self.msg_thread.turn_received.connect(self.play_screen.handle_turn)
                    self.msg_thread.chat_received.connect(self.play_screen.handle_chat)
                    self.msg_thread.check_received.connect(self.play_screen.update_board_with_check)
                    self.msg_thread.connection_lost.connect(self.connection_lost)
                    self.msg_thread.game_started.connect(self.play_screen.handle_game_started)
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

        request=move_request(
            URL="move",
            sender=self.id,
            selected_piece=(from_x,from_y),
            new_position=(to_x,to_y)
        )
        self.socket.sendall(pickle.dumps(request))
                
    def send_possible_moves_request(self,from_x,from_y):
        print(f"Su konumdaki tas icin olasi hamleler istegi yollandi ({from_x},{from_y})")
        packet=get_possible_moves_request(URL="get_possible_moves",sender=self.id,selected_piece=(from_x,from_y))
        self.socket.sendall(pickle.dumps(packet))

    def send_chat(self,message_content):
        packet=chat_request(URL="chat",sender= "Player "+str(self.id),message=message_content)
        self.socket.sendall(pickle.dumps(packet))

    def connection_lost(self,who_id):
        QMessageBox.warning(self.window, "Connection Lost", f"Player {who_id} disconnected.")
        self.play_screen.reset_all()
        self.stack.setCurrentIndex(0)
        
        
            

                







class messagethread(QThread):
    possible_moves_received = Signal(list)
    move_received = Signal(str)
    turn_received=Signal(bool)
    chat_received=Signal(str,str)
    check_received=Signal(str)
    connection_lost=Signal(int)
    game_started=Signal()

    
    def __init__(self, socket,id):
        super().__init__()
        self.socket = socket
        self.id=id
        

    
    
    def run(self):
        while True:
            # move_result = "unsuccessful move"
            # pos_title = "from_x,from_y,to_x,to_y"
            # move_result = "move,pos_title"
            # move_result = "capture,pos_title"
            # move_result = "check,pos_title"
            # move_result = "checkmate,pos_title"


            # cases
            # move_result = "unsuccessful move"
            # move_result = "move"
            # move_result = "capture..."
            # move_result = "check..."
            # move_result = "checkmate..."
            try:
                received_pickle=self.socket.recv(4096)
                received_packet=pickle.loads(received_pickle)
                if received_packet.URL=="move":
                        print(f"moveresultttttttt{received_packet.move_result}")
                        if received_packet.move_result.startswith("move"):
                            self.move_received.emit(received_packet.move_result)
                        elif received_packet.move_result.startswith("unsuccessful move"):
                            self.move_received.emit(received_packet.move_result)
                        elif received_packet.move_result.startswith("capture"):
                            self.move_received.emit(received_packet.move_result)
                        elif received_packet.move_result.startswith("check"):
                            self.check_received.emit(received_packet.move_result)
                        elif received_packet.move_result.startswith("checkmate"):
                            self.check_received.emit(received_packet.move_result)
                        
                        if received_packet.move_result!="unsuccessful move": 
                            # sender ben miyim?
                            if received_packet.sender != self.id:
                                # rakip oynadı, sıra bende
                                self.turn_received.emit(True)
                            else:
                                # ben oynadım, sıra rakipte
                                self.turn_received.emit(False)

                if received_packet.URL=="get_possible_moves":
                    print(f"Olasi hamleler alindi: {received_packet.possible_moves}")
                    self.possible_moves_received.emit(received_packet.possible_moves)

                if received_packet.URL=="chat":
                    self.chat_received.emit(received_packet.sender,received_packet.message)

                if received_packet.URL=="connection_lost":
                    self.connection_lost.emit(received_packet.who)
                    break
                if received_packet.URL == "start_game":   
                    self.game_started.emit()
                    
                    
                
                
                    

            except Exception as e:
                print(f"[ERROR] {e}")
                break  



if __name__ == "__main__":
    game = Connect()
    game.stack.show() 
    sys.exit(game.app.exec())