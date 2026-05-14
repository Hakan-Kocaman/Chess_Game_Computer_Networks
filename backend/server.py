import threading
import pickle
from services import start_game_service
import gateway as gateway
from player import player, player_list,player_id_list
import socket_manager
from logger import logger
import global_variables
from models.GameBoard import game_board



def start_server():
    global current_turn, game_state, game_states
    while True:
        player_socket, address = socket_manager.server_socket.accept()
        new_player = player(player_socket, address)
        logger.info(f"New player connected: {new_player.get_name()} from {address}")
        handle_player_connection(new_player)


def handle_player_connection(new_player):
    starting_board = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"], # siyah taşlar
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
    ["·", "·", "·", "·", "·", "·", "·", "·"], # Boş kareler
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],        
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"], # beyaz taşlar
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
    ]
    global current_turn

    initial_packet = {
        "URL": "initial",
        "sender": "server",
        "player_id": new_player.id, 
        "player_color": new_player.color,
        "game_board": starting_board,                            #Hosgeldin paketine baslangic tahtasi eklendi
        "state": global_variables.game_state,
    }
    handshake = pickle.dumps(initial_packet)
    new_player.socket.sendall(handshake) 

    if len(player_list) > 1 and global_variables.game_state != global_variables.game_states[1]:  
        start_game_service()
        global_variables.game_state = global_variables.game_states[1] 
        logger.info("Two players connected. Starting the game.")
    
    try:
        controller_thread = threading.Thread(target=gateway.handle_client, args=(new_player.socket,))
        controller_thread.start()
    except Exception as e:
        logger.error(f"Error starting controller thread for {new_player.get_name()}: {e}")


def reset_server_all():
    global current_turn, game_state, game_states
    global_variables.current_turn = "white"
    global_variables.game_states = ["waiting", "game"]
    global_variables.game_state = global_variables.game_states[0]
    player_list.clear()
    player_id_list.clear()
    player_id_list.extend(range(1, 99))  
    game_board.__init__()

    


if __name__ == "__main__":
    logger.info("Starting Chess Game Server...")
    start_server()
    logger.info("Chess Game Server shut down.")




    
