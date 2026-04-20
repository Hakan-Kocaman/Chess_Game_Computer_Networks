import pickle
import services

def chat_controller(player_color, request_body):
    to_socket, response = services.chat_service(player_color, request_body)
    if to_socket:
        to_socket.send(pickle.dumps(response))
    return {"success": True}

def get_possible_moves_controller(player_color, request_body):
    to_socket, response = services.get_possible_moves_service(player_color, request_body)
    if to_socket:
        to_socket.send(pickle.dumps(response))
    return {"success": True}

def move_controller(player_color, request_body):
    to_socket, response = services.move_service(player_color, request_body)
    if to_socket:
        to_socket.send(pickle.dumps(response))
    return {"success": True}