
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import services
from logger import logger
from dtos.responses import chat_response, get_possible_moves_response, move_response

# client gateway controllers
def chat_controller(request):
    services.chat_service(request)
    logger.info(f"Chat controller processed chat request from {request.sender}. Message: {request.message}")
    return {"success": True}

def get_possible_moves_controller(request):
    services.get_possible_moves_service(request)
    logger.info(f"Get Possible Moves controller processed request from {request.sender}. Requested piece: {request.selected_piece}")
    return {"success": True}

def move_controller(request):
    services.move_service(request)
    logger.info(f"Move controller processed move request from {request.sender}. Move details: {request.selected_piece} {request.new_position}")
    return {"success": True}




