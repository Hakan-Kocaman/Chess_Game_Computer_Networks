import pickle
import services
from logger import logger
from dtos.responses import chat_response, get_possible_moves_response, move_response

# client gateway controllers
def chat_controller(request):
    request= chat_response( # converting dict to specific response object
        URL=request.URL, # URL -> "chat"
        sender=request.sender,
        reciever_list=request.reciever_list,
        message=request.message
    )
    services.chat_service(request)
    logger.info(f"Chat controller processed chat request from {request.sender}. Message: {request.body}")
    return {"success": True}

def get_possible_moves_controller(request):
    request= get_possible_moves_response( # converting dict to specific response object
        URL=request.URL, # URL -> "get_possible_moves"
        sender=request.sender,
        reciever_list=request.reciever_list,
        selected_piece=request.selected_piece
    )
    services.get_possible_moves_service(request)
    logger.info(f"Get Possible Moves controller processed request from {request.sender}. Requested piece: {request.body}")
    return {"success": True}

def move_controller(request):
    request= move_response( # converting dict to specific response object
        URL=request.URL, # URL -> "move"
        sender=request.sender,
        reciever_list=request.reciever_list,
        selected_piece=request.selected_piece,
        new_position=request.new_position
    )
    services.move_service(request)
    logger.info(f"Move controller processed move request from {request.sender}. Move details: {request.body}")
    return {"success": True}




