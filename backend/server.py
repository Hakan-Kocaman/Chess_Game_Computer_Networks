import threading
import pickle
from backend.controllers import start_game_controller
import gateway as gateway
from player import player, player_list
import socket_manager
from logger import logger
from models.GameBoard import game_board

game_states = ["waiting", "game", "result"]

def start_server():
    global current_turn, game_state, game_states
    while True:
        player_socket, address = socket_manager.server_socket.accept()
        new_player = player(player_socket, address)
        player_list.append(new_player) 
        logger.info(f"New player connected: {new_player.get_name()} from {address}")
        handle_player_connection(new_player)

        

def handle_player_connection(new_player):
    global current_turn, game_state, game_states

    initial_packet = {
        "URL": "game_start", 
        "player": new_player,
        "board": game_board,
        "state": game_state,
        "message": f"Joined as {new_player.get_name()}"
    }
    handshake = pickle.dumps(initial_packet)
    new_player.socket.send(handshake) 

    if len(player_list) > 1 and game_state == game_states[0]:  
        success = start_game_controller()
        if success:
            game_state = game_states[1] 
            logger.info("Two players connected. Starting the game.")
    
    try:
        controller_thread = threading.Thread(target=gateway.handle_client, args=(new_player.socket))
        controller_thread.start()
    except Exception as e:
        logger.error(f"Error starting controller thread for {new_player.get_name()}: {e}")



if __name__ == "__main__":
    current_turn="white"
    game_state = game_states[0]

    logger.info("Starting Chess Game Server...")
    start_server()
    logger.info("Chess Game Server shut down.")




    
