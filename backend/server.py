import threading
import pickle
import backend.gateway as gateway
import models 
from player import player, player_list
import random
import socket_manager


def start_server():
    global current_turn, colors
    while True:
        #bekleme
        if len(player_list) >= 2:
            print(f"[REJECTED] {address} bağlanmaya çalıştı ancak oda dolu.")
            # İstemciye odanın dolu olduğunu bildiren bir paket yolla.
            error_packet = {"type": "error", "message": "Room is full!"}
            response = pickle.dumps(error_packet)
            player_socket.send(response)
            player_socket.close()
            start_server()

        player_socket, address = socket_manager.server_socket.accept()
        assigned_color = None
        if player_list.clear():
            assigned_color = random.choice(colors)
        else: 
            assigned_color = "black" if "white" in player_list.values() else "white"

        new_player = player(player_socket, assigned_color)
        player_list.append(new_player) 

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
            controller_thread = threading.Thread(target=gateway.handle_client, args=(player_socket))
            controller_thread.start()
        except Exception as e:
            print(f"[ERROR] {assigned_color}: {e}")
            break
    if player_socket in player_list:
        del player_list[player_socket]
    player_socket.close()


if __name__ == "__main__":
    current_turn="white"
    colors = ["white", "black"]
    
    print("Starting server...")
    start_server()




    
