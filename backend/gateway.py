
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import threading
import pickle
import socket_manager
import controllers
from logger import logger
from dtos.client_requests import move_request,chat_request,get_possible_moves_request


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
        data = client_socket.recv(4096)
        request = pickle.loads(data)

        controller_thread=threading.Thread(target=controller_handler, args=(client_socket, request))
        controller_thread.start()








