import socket
import threading
import pickle

HOST = "0.0.0.0" 
PORT = 5050


connected_players={}
current_turn="white"


class ChessEngine:
    def __init__(self):
        
        self.board = "Matrix"

    def is_valid_move(self, color, start_pos, end_pos):
       
        return True 

    def update_board(self, start_pos, end_pos):
        
        pass


def broadcast():
    pass





def handle_player_connection(player_socket, address, assigned_color):
    
    
    global current_turn

    welcome_packet = {
        "type": "game_start", 
        "color": assigned_color,
        "message": f"Joined as {assigned_color}"
    }
    
    player_socket.send(pickle.dumps(welcome_packet))
    
    while True: 
        try:
            data = player_socket.recv(4096)
            if not data:
                break
                    
            
            received_packet = pickle.loads(data)
            print(f"[{assigned_color}] Packet received: {received_packet}")

            if received_packet["type"] == "move":
                start_pos = received_packet["start"]
                end_pos = received_packet["end"]
            
                if current_turn!=assigned_color:
                    pass

                if ChessEngine.is_valid_move(assigned_color,start_pos,end_pos):
                    ChessEngine.update_board(start_pos,end_pos)
                    if current_turn == "white":
                        current_turn == "black"
                    else:
                        current_turn == "white"
                    success_packet = {
                            "type": "update_board",
                            "start": start_pos,
                            "end": end_pos,
                            "next_turn": current_turn
                        }
                    broadcast(success_packet)
                else:
                    error_packet = {
                        "type": "error", 
                        "message": "Geçersiz satranç hamlesi!"
                    }
                    player_socket.send(pickle.dumps(error_packet))


            elif received_packet["type"] == "message":
                pass
        except EOFError:
            break
        except Exception as e:
            print(f"[ERROR] {assigned_color}: {e}")
            break
    if player_socket in connected_players:
        del connected_players[player_socket]
    player_socket.close()





def start_chess_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Chess server {HOST}:{PORT} listening...")
    colors = ["white", "black"]
    while True:
        #bekleme
        player_socket, address = server_socket.accept()
        
        """""
        if len(connected_players) >= 2:
            print(f"[REJECTED] {address} bağlanmaya çalıştı ancak oda dolu.")
            # İstemciye odanın dolu olduğunu bildiren bir paket yolla.
            error_packet = {"type": "error", "message": "Room is full!"}
            player_socket.send(pickle.dumps(error_packet))
            player_socket.close()
            continue
        """

        assigned_color = colors[len(connected_players)]
        connected_players[player_socket] = assigned_color
        
        player_thread = threading.Thread(target=handle_player_connection, args=(player_socket, address))
        player_thread.start()
        
        

if __name__ == "__main__":
    start_chess_server()



    
