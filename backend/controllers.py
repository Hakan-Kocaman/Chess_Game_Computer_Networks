import pickle
import services
from logger import logger
from dtos.responses import chat_response, get_possible_moves_response, move_response


# client gateway controllers
def chat_controller(request):
    request= move_response( # converting dict to specific response object
        URL=request.URL, # URL -> "chat"
        sender=request.sender,
        reciever_list=request.reciever_list,
        message=request.message
    )
    response = services.chat_service(request)
    logger.info(f"Chat controller processed chat request from {request.sender}. Message: {request.body}")
    broadcast(response)
    return {"success": True}

def get_possible_moves_controller(request):
    request= get_possible_moves_response( # converting dict to specific response object
        URL=request.URL, # URL -> "get_possible_moves"
        sender=request.sender,
        reciever_list=request.reciever_list,
        selected_piece=request.selected_piece
    )
    response = services.get_possible_moves_service(request)
    logger.info(f"Get Possible Moves controller processed request from {request.sender}. Requested piece: {request.body}")
    broadcast(response)
    return {"success": True}

def move_controller(request):
    request= move_response( # converting dict to specific response object
        URL=request.URL, # URL -> "move"
        sender=request.sender,
        reciever_list=request.reciever_list,
        selected_piece=request.selected_piece,
        new_position=request.new_position
    )
    response = services.move_service(request)
    logger.info(f"Move controller processed move request from {request.sender}. Move details: {request.body}")
    broadcast(response)
    return {"success": True}



# server controllers
def start_game_controller():
    response = services.start_game_service()
    logger.info(f"Game Started By Server. Broadcasting start game response to all clients.")
    broadcast(response)
    return {"success": True}

def turn_change_controller(current_turn):
    response = services.turn_change_service(current_turn)
    logger.info(f"Turn is now on {current_turn}.")
    broadcast(response)
    return {"success": True}

def broadcast(response):
    logger.info(f"Broadcasting response for {response.URL} to {len(response.reciever_list)} clients.")
    if response.reciever_list:
        for socket in response.reciever_list:
            socket.send(pickle.dumps(response))
    return {"success": True}