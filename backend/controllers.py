import pickle
import services
from logger import logger

def chat_controller(request):
    response = services.chat_service(request)
    logger.info(f"Chat controller processed chat request from {request.sender}. Message: {request.body}")
    broadcast(response)
    return {"success": True}

def get_possible_moves_controller(request):
    response = services.get_possible_moves_service(request)
    logger.info(f"Get Possible Moves controller processed request from {request.sender}. Requested piece: {request.body}")
    broadcast(response)
    return {"success": True}

def move_controller(request):
    response = services.move_service(request)
    logger.info(f"Move controller processed move request from {request.sender}. Move details: {request.body}")
    broadcast(response)
    return {"success": True}

def broadcast(response):
    logger.info(f"Broadcasting response for {response.URL} to {len(response.reciever_list)} clients.")
    if response.reciever_list:
        for socket in response.reciever_list:
            socket.send(pickle.dumps(response))
    return {"success": True}