import threading
import pickle
from services import start_game_service
import gateway as gateway
from player import player, player_list
import socket_manager
from logger import logger
import global_variables



def start_server():
    global current_turn, game_state, game_states
    while True:
        player_socket, address = socket_manager.server_socket.accept()
        new_player = player(player_socket, address)
        player_list.append(new_player) 
        logger.info(f"New player connected: {new_player.get_name()} from {address}")
        handle_player_connection(new_player)

        

def handle_player_connection(new_player):
    starting_board = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"], # Siyah taşlar
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
    ["·", "·", "·", "·", "·", "·", "·", "·"], # Boş kareler
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"], # Beyaz taşlar
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
    ]
    global current_turn

    initial_packet = {
        "URL": "initial",
        "sender": "server",
        "player": new_player,
        "game_board": starting_board,                            #Hosgeldin paketine baslangic tahtasi eklendi
        "state": global_variables.game_state,
        "message": f"Joined as {new_player.get_name()}"
    }
    handshake = pickle.dumps(initial_packet)
    new_player.socket.send(handshake) 

    if len(player_list) > 1 and global_variables.game_state != global_variables.game_states[1]:  
        start_game_service()
        global_variables.game_state = global_variables.game_states[1] 
        logger.info("Two players connected. Starting the game.")
    
    try:
        controller_thread = threading.Thread(target=gateway.handle_client, args=(new_player.socket,))
        controller_thread.start()
    except Exception as e:
        logger.error(f"Error starting controller thread for {new_player.get_name()}: {e}")



if __name__ == "__main__":
    logger.info("Starting Chess Game Server...")
    start_server()
    logger.info("Chess Game Server shut down.")




    
