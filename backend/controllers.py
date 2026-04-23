import pickle
import services

def chat_controller(request):
    to_socket, response = services.chat_service(request)
    broadcast(to_socket, response)
    return {"success": True}

def get_possible_moves_controller(request):
    to_socket, response = services.get_possible_moves_service(request)
    broadcast(to_socket, response)
    return {"success": True}

def move_controller(request):
    to_socket, response = services.move_service(request)
    broadcast(to_socket, response)
    return {"success": True}

def broadcast(to_socket, response):
    if to_socket:
        for socket in to_socket:
            socket.send(pickle.dumps(response))
    return {"success": True}