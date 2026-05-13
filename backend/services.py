
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import global_variables
from player import player_list
from models.GameBoard import game_board
from models.ChessPiece import ChessPiece
from models.Bishop import Bishop
from models.King import King
from models.Knight import Knight
from models.Pawn import Pawn
from models.Queen import Queen
from models.Rook import Rook
from logger import logger
import pickle
from dtos.server_responses import move_response, get_possible_moves_response, chat_response, start_game_response, turn_change_response, finish_game_response

def chat_service(request):
    reciever_list = [] 

    for player in player_list:
        if player.id != request.sender:
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
        if player.id == (request.sender):
            reciever_list.append(player.socket)
            break

    selected_piece = request.selected_piece
    selected_piece = game_board.board[selected_piece[0]][selected_piece[1]] 
    logger.info(f"Selected piece: {selected_piece.color} + {selected_piece.__class__.__name__} + {selected_piece.position} ")
    
    possible_moves = selected_piece.get_possible_moves()

    response = get_possible_moves_response(
        URL=request.URL,
        sender=request.sender,
        possible_moves=possible_moves
    )
    print(f"Olasi hamleler gonderildi: {game_board.board}")
    broadcast(response, reciever_list)


def move_service(request):

    reciever_list = []
    for player in player_list:
        reciever_list.append(player.socket)

    
    selected_piece = (game_board.board[request.selected_piece[0]][request.selected_piece[1]])

    logger.info(f"Selected piece: {selected_piece.color} + {selected_piece.__class__.__name__} + {selected_piece.position} to {request.new_position}")

    if isinstance(selected_piece, Pawn):
        selected_piece = Pawn(selected_piece.color, request.new_position)
        game_board.board[request.new_position[0]][request.new_position[1]] = selected_piece
    elif isinstance(selected_piece, Rook):
        selected_piece = Rook(selected_piece.color, request.new_position)
        game_board.board[request.new_position[0]][request.new_position[1]] = selected_piece
    elif isinstance(selected_piece, Knight):
        selected_piece = Knight(selected_piece.color, request.new_position)
        game_board.board[request.new_position[0]][request.new_position[1]] = selected_piece
    elif isinstance(selected_piece, Bishop):
        selected_piece = Bishop(selected_piece.color, request.new_position)
        game_board.board[request.new_position[0]][request.new_position[1]] = selected_piece
    elif isinstance(selected_piece, Queen):
        selected_piece = Queen(selected_piece.color, request.new_position)
        game_board.board[request.new_position[0]][request.new_position[1]] = selected_piece
    elif isinstance(selected_piece, King):
        selected_piece = King(selected_piece.color, request.new_position)
        game_board.board[request.new_position[0]][request.new_position[1]] = selected_piece


    
    #eski konumu none yap
    game_board.board[request.selected_piece[0]][request.selected_piece[1]] = None

    sender_player = None
    for player in player_list:
        if player.id == int(request.sender):
            sender_player = player
            break

    if selected_piece == None:
        logger.info(f"Move service processed gate 1 move request from {request.sender}. Move details: {request.selected_piece} {request.new_position}")
        return

    if sender_player.color != global_variables.current_turn:
        logger.info(f"Move service processed gate 2 move request from {request.sender}. Move details: {request.selected_piece} {request.new_position}")
        return


    
    response = move_response(
        URL=request.URL,
        sender=request.sender,
        move_result= selected_piece.move(request.new_position)
    )
    broadcast(response, reciever_list)

    if response.move_result.startswith("checkmate"):
        finish_game_service(sender_player.color, "black" if sender_player.color == "white" else "white" ,response.move_result)
        return

    turn_change_service()

def start_game_service():
    white_player = None
    black_player = None

    reciever_list = []
    for player in player_list:
        if player.color == "white":
            white_player = player.id
        elif player.color =="black":
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
            socket.sendall(pickle.dumps(response))
