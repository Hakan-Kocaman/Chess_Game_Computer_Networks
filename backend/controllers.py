import pickle
import services

def chat_controller(request):
    response = services.chat_service(request)
    broadcast(response)
    return {"success": True}

def get_possible_moves_controller(request):
    response = services.get_possible_moves_service(request)
    broadcast(response)
    return {"success": True}

def move_controller(request):
    response = services.move_service(request)
    broadcast(response)
    return {"success": True}

def broadcast(response):
    if response.reciever_list:
        for socket in response.reciever_list:
            socket.send(pickle.dumps(response))
    return {"success": True}