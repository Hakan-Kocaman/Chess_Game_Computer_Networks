import threading
import pickle
import gateway as gateway
from player import player, player_list
import socket_manager
from logger import logger
from GameBoard import GameBoard


def start_server():
    global current_turn, colors
    while True:

        player_socket, address = socket_manager.server_socket.accept()
        new_player = player(player_socket, address)
        player_list.append(new_player) 
        logger.info(f"New player connected: {new_player.get_name()} from {address}")
        handle_player_connection(new_player)

        

def handle_player_connection(new_player):
    global current_turn

    initial_packet = {
        "type": "game_start", 
        "player": new_player,
        "message": f"Joined as {new_player.get_name()}",
        "game_board": GameBoard.starting_board

    }
    handshake = pickle.dumps(initial_packet)
    new_player.socket.send(handshake)   
    
    try:
        controller_thread = threading.Thread(target=gateway.handle_client, args=(new_player.socket))
        controller_thread.start()
    except Exception as e:
        logger.error(f"Error starting controller thread for {new_player.get_name()}: {e}")



if __name__ == "__main__":
    current_turn="white"

    logger.info("Starting Chess Game Server...")
    start_server()
    logger.info("Chess Game Server shut down.")




    
