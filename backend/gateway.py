
import sys
import os

from backend import server
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import threading
import pickle
import socket_manager
import controllers
from logger import logger
from dtos.client_requests import move_request,chat_request,get_possible_moves_request
from dtos.server_responses import connection_lost_response
from player import player_list, player_id_list
from services import reset_server_service

# request= {
#     "URL": determines the service,
#     "sender": sender of the request,
#     .....
# }

server_socket = socket_manager.server_socket

controller_list = {
   "chat": controllers.chat_controller,
   "get_possible_moves": controllers.get_possible_moves_controller,
   "move": controllers.move_controller
}

def controller_handler(client_socket, request):
    if client_socket:
        try:
            requested_controller = controller_list.get(request.URL)
            if requested_controller:
                logger.info(f"Received request for {request.URL} from {request.sender}")
                response = requested_controller(request)    
                if response != {"success": True}:
                    logger.error(f"Controller {request.URL} did not return a response for request from {request.sender}. Response: {response}")    
            else:
                client_socket.send(pickle.dumps({"error": "unknown service"}))
                logger.error(f"Unknown service requested from {request.sender}: {request.URL}")
        except Exception as e:
                logger.error(f"Error receiving data from client: {e}")

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                logger.info("Client disconnected")
                break
            
            request = pickle.loads(data)
            # Not: Her paket için yeni thread açmak oyun anında sıra kaymalarına 
            # sebep olabilir ama şu an çalışıyorsa dokunma.
            controller_handler(client_socket, request)
            
        except Exception as e:
            logger.error(f"Error receiving data from client: {e}")
            break


    
    
    found_player = None
    for p in player_list:
        if p.socket == client_socket:
            found_player = p
            client_socket.close()
            player_list.remove(p)
            player_id_list.append(p.id) 
            break
            
    
    if found_player is not None:
        response = connection_lost_response(
            URL="connection_lost",
            sender=None,
            who=found_player.id
        )
        

    for player in player_list:
        try:
            player.socket.sendall(pickle.dumps(response))
        except Exception as e:
            logger.error(f"Error sending connection lost response to player {player.id}: {e}")


    for player in player_list:
        try:
            player.__del__()
        except Exception as e:
            logger.error(f"Error closing player socket: {e}")


    
    
    try:
        reset_server_service()
    except Exception as e:
        logger.error(f"Server resetlenirken hata oluştu: {e}")
    
        

        








