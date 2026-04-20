from player import player_list
from models import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King, game_board

def chat_service(player_color, request_body):
    for player in player_list:
        if player.color != player_color:
            to_socket = player.socket
            return to_socket, {"from": player_color, "message": request_body}

            break  # kendi taşı, dur
                
def get_possible_moves_service(player_color, request_body):
    # expected request_body: {selected_piece: ChessPiece}
    to_socket = None
    for player in player_list:
        if player.color == player_color:
            to_socket = player.socket
            break

    selected_piece = request_body.get("selected_piece")
    selected_piece = game_board[selected_piece.position[0]][selected_piece.position[1]] 
    
    possible_moves = selected_piece.get_possible_moves(player_color)

    return to_socket, {"possible_moves": possible_moves}

def move_service(player_color, request_body):
    to_socket = None
    # Burada gelen hareket isteğini işleyin, geçerli olup olmadığını kontrol edin ve ardından hamleyi gerçekleştirin.
    move_result = process_move(player_color, request_body)
    return to_socket, {"move_result": move_result}

                
 
    