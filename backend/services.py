from player import player_list
from models import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King, game_board

def chat_service(player_color, request_body):
    for player in player_list:
        if player.color != player_color:
            to_socket = player.socket
            return to_socket, {"from": player_color, "message": request_body}

def get_possible_moves_service(player_color, request_body):
    # expected request_body: {selected_piece: ChessPiece}
    to_socket = None
    for player in player_list:
        if player.color == player_color:
            to_socket = player.socket
            break

    selected_piece = request_body.get("selected_piece")

    possible_moves= []

    if selected_piece.get("color") != player_color:
        return to_socket, {"error": "Selected piece does not belong to the player."}
    
    if isinstance(selected_piece, Pawn):
        pass
    elif isinstance(selected_piece, Rook):
        for x in range(1,7):
            if selected_piece.position[0] + x < 8 and game_board[selected_piece.position[0] + x][selected_piece.position[1]] is None:
                possible_moves.append((selected_piece.position[0] + x, selected_piece.position[1]))
            elif selected_piece.position[0] + x >= 8 or game_board[selected_piece.position[0] + x][selected_piece.position[1]].color != player_color:
                possible_moves.append((selected_piece.position[0] + x, selected_piece.position[1]))
                break              
        for x in range(1,7):
            if selected_piece.position[0] - x >= 0 and game_board[selected_piece.position[0] - x][selected_piece.position[1]] is None:
                possible_moves.append((selected_piece.position[0] - x, selected_piece.position[1]))  
            elif selected_piece.position[0] - x < 0 or game_board[selected_piece.position[0] - x][selected_piece.position[1]].color != player_color:
                possible_moves.append((selected_piece.position[0] - x, selected_piece.position[1]))
                break
        for y in range(1,7):
            if selected_piece.position[1] + y < 8 and game_board[selected_piece.position[0]][selected_piece.position[1] + y] is None:
                possible_moves.append((selected_piece.position[0], selected_piece.position[1] + y))
            elif selected_piece.position[1] + y >= 8 or game_board[selected_piece.position[0]][selected_piece.position[1] + y].color != player_color:
                possible_moves.append((selected_piece.position[0], selected_piece.position[1] + y))
                break
        for y in range(1,7):
            if selected_piece.position[1] - y >= 0 and game_board[selected_piece.position[0]][selected_piece.position[1] - y] is None:
                possible_moves.append((selected_piece.position[0], selected_piece.position[1] - y))
            elif selected_piece.position[1] - y < 0 or game_board[selected_piece.position[0]][selected_piece.position[1] - y].color != player_color:
                possible_moves.append((selected_piece.position[0], selected_piece.position[1] - y))
                break

    elif isinstance(selected_piece, Knight):
        pass
    elif isinstance(selected_piece, Bishop):
        pass
    elif isinstance(selected_piece, Queen):
        pass
    elif isinstance(selected_piece, King):
        pass


    




    return to_socket, {"possible_moves": possible_moves}

def move_service(player_color, request_body):
    to_socket = None
    # Burada gelen hareket isteğini işleyin, geçerli olup olmadığını kontrol edin ve ardından hamleyi gerçekleştirin.
    move_result = process_move(player_color, request_body)
    return to_socket, {"move_result": move_result}

                
 
    