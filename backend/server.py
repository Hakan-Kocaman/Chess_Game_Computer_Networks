import threading
import pickle
import controller
import models  
import random
import socket_manager
from chess_engine import ChessEngine

def start_server():
    global connected_players, current_turn, colors
    while True:
        #bekleme
        player_socket, address = socket_manager.server_socket.accept()
        
        if len(connected_players) >= 2:
            print(f"[REJECTED] {address} bağlanmaya çalıştı ancak oda dolu.")
            # İstemciye odanın dolu olduğunu bildiren bir paket yolla.
            error_packet = {"type": "error", "message": "Room is full!"}
            response = pickle.dumps(error_packet)
            player_socket.send(response)
            player_socket.close()
            start_server()

        assigned_color = None
        if connected_players.clear():
            assigned_color = random.choice(colors)
            connected_players[player_socket] = assigned_color
        else: 
            assigned_color = "black" if "white" in connected_players.values() else "white"
            connected_players[player_socket] = assigned_color
        

        player_thread = threading.Thread(target=handle_player_connection, args=(player_socket, address, assigned_color))
        player_thread.start()

def handle_player_connection(player_socket, address, assigned_color):
    global current_turn

    initial_packet = {
        "type": "game_start", 
        "color": assigned_color,
        "message": f"Joined as {assigned_color}"
    }
    handshake = pickle.dumps(initial_packet)
    player_socket.send(handshake)
    
    while True: 
        try:
            controller_thread = threading.Thread(target=controller.handle_client, args=(player_socket))
            controller_thread.start()
        except Exception as e:
            print(f"[ERROR] {assigned_color}: {e}")
            break
    if player_socket in connected_players:
        del connected_players[player_socket]
    player_socket.close()


if __name__ == "__main__":
    connected_players={}
    current_turn="white"
    colors = ["white", "black"]
    engine = ChessEngine()
    
    print("Starting server...")
    start_server()




    
