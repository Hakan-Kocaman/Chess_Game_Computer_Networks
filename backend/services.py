
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.ChessPiece import game_board
from player import player_list
from dtos.responses import move_response_body, chat_response_body, get_possible_moves_response_body
from dtos.responses import response as response_dto

def chat_service(request):
    reciever_list = []

    for player in player_list:
        if player.color != request.sender:
            reciever_list.append(player.socket)
    
    response = response_dto(
                URL=request.URL,
                sender=request.sender,
                reciever_list=reciever_list,
                body=chat_response_body(
                    message=request.body.message
                    )
            )
    return response

                
def get_possible_moves_service(request):

    reciever_list = []
    for player in player_list:
        if player.color == request.sender:
            reciever_list.append(player.socket)
            break

    selected_piece = request.body.selected_piece
    selected_piece = game_board[selected_piece.position[0]][selected_piece.position[1]] 
    
    possible_moves = selected_piece.get_possible_moves()

    response = response_dto(
        URL=request.URL,
        sender=request.sender,
        reciever_list=reciever_list,
        body=get_possible_moves_response_body(
            possible_moves=possible_moves
            )
    )
    return response

def move_service(request):

    reciever_list = []
    for player in player_list:
        reciever_list.append(player.socket)

    selected_piece = request.body.get("selected_piece")
    selected_piece = game_board[selected_piece.position[0]][selected_piece.position[1]]
    
    response = response_dto(
        URL=request.URL,
        sender=request.sender,
        reciever_list=reciever_list,
        move_result= selected_piece.move(request.body.get("new_position"))
    )
    
    return response

def start_game_service():
    reciever_list = []
    for player in player_list:
        if player.color in ["white"]:
            white_player = player
        elif player.color in ["black"]:
            black_player = player
        reciever_list.append(player.socket)

    response = {
        "URL": "game_start",
        "sender": "server",
        "reciever_list": reciever_list,
        "white": white_player,
        "black": black_player
    }
    return response

def turn_change_service(current_turn):
    reciever_list = []
    for player in player_list:
        reciever_list.append(player.socket)

    response = { 
        "URL": "turn_change",
        "sender": "server",
        "reciever_list": reciever_list,
        "current_turn": current_turn
    }

def finish_game_service(winner,loser,result):
    reciever_list = []
    for player in player_list:
        reciever_list.append(player.socket)
    
    response = {
        "URL": "finish_game",
        "sender": "server",
        "reciever_list": reciever_list,
        "winner": winner,
        "loser": loser,
        "result": result
    }
