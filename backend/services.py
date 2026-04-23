from player import player_list
from models import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King, game_board

def chat_service(request):
    to_socket = []
    player_color = request["from"]
    request_body = request["body"]
    for player in player_list:
        if player.color != player_color:
            to_socket.append(player.socket)
            request["body"]["message"] = request_body
            return to_socket, request

            break  # kendi taşı, dur
                
def get_possible_moves_service(request):
    # expected request_color: "white" or "black"
    # expected request_body: {selected_piece: ChessPiece}
    player_color = request["from"]
    request_body = request["body"]

    to_socket = []
    for player in player_list:
        if player.color == player_color:
            to_socket.append(player.socket)
            break

    selected_piece = request_body.get("selected_piece")
    selected_piece = game_board[selected_piece.position[0]][selected_piece.position[1]] 
    
    possible_moves = selected_piece.get_possible_moves()

    request["body"]["possible_moves"] = possible_moves

    return to_socket, request

def move_service(request):
    player_color = request["from"]
    request_body = request["body"]

    to_socket = []
    for player in player_list:
        to_socket.append(player.socket)

    selected_piece = request_body.get("selected_piece")
    selected_piece = game_board[selected_piece.position[0]][selected_piece.position[1]] 
    
    move_result = selected_piece.move(request_body.get("new_position"))

    request["body"]["move_result"] = move_result

    return to_socket, request

                
 
    