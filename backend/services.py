
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.GameBoard import GameBoard as game_board
from player import player_list
import global_variables
from logger import logger
import pickle
from dtos.server_responses import move_response, get_possible_moves_response, chat_response, start_game_response, turn_change_response, finish_game_response

def chat_service(request):
    reciever_list = []

    for player in player_list:
        if player.color != request.sender:
            reciever_list.append(player.socket)
    
    response = chat_response(
                URL=request.URL,
                sender=request.sender,
                message=request.message
            )
    
    broadcast(response, reciever_list)
                
def get_possible_moves_service(request):

    reciever_list = []
    for player in player_list:
        if player.color == request.sender:
            reciever_list.append(player.socket)
            break

    selected_piece = request.selected_piece
    selected_piece = game_board[selected_piece[0]][selected_piece[1]] 
    
    possible_moves = selected_piece.get_possible_moves()

    response = get_possible_moves_response(
        URL=request.URL,
        sender=request.sender,
        possible_moves=possible_moves
    )
    broadcast(response, reciever_list)


def move_service(request):

    reciever_list = []
    for player in player_list:
        reciever_list.append(player.socket)

    selected_piece = request.selected_piece
    selected_piece = game_board[selected_piece[0]][selected_piece[1]]

    if request.sender != global_variables.current_turn:
        return

    if request.sender != request.selected_piece.color:
        return
    
    response = move_response(
        URL=request.URL,
        sender=request.sender,
        move_result= selected_piece.move(request.new_position)
    )
    broadcast(response, reciever_list)

    if response.move_result.startswith("checkmate"):
        finish_game_service(request.sender, "black" if request.sender == "white" else "white" ,response.move_result)
        return

    turn_change_service()

def start_game_service():
    reciever_list = []
    for player in player_list:
        if player.color in ["white"]:
            white_player = player.id
        elif player.color in ["black"]:
            black_player = player.id
        reciever_list.append(player.socket)

    response = start_game_response( 
        URL="start_game",
        sender="server",
        white=white_player,
        black=black_player
    )
    broadcast(response, reciever_list)


def turn_change_service():
    reciever_list = []
    for player in player_list:
        reciever_list.append(player.socket)

    global_variables.current_turn = "white" if global_variables.current_turn == "black" else "black"

    response = turn_change_response(
        URL="turn_change",
        sender="server",
        current_turn=global_variables.current_turn
    )
    broadcast(response, reciever_list)

def finish_game_service(winner,loser,result):
    reciever_list = []
    for player in player_list:
        reciever_list.append(player.socket)
    
    response = finish_game_response(
        URL="finish_game",
        sender="server",
        winner=winner,
        loser=loser,
        result=result
    )
    broadcast(response, reciever_list)


def broadcast(response, reciever_list):
    logger.info(f"Broadcasting response for {response.URL} to {len(reciever_list)} clients.")
    if reciever_list:
        for socket in reciever_list:
            socket.send(pickle.dumps(response))
