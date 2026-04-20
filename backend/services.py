from player import player_list
from models import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King, game_board

def chat_service(player_color, request_body):
    for player in player_list:
        if player.color != player_color:
            to_socket = player.socket
            return to_socket, {"from": player_color, "message": request_body}

def func(directions, selected_piece, possible_moves):
    for dx, dy in directions:
            for step in range(1, 8):
                nx = selected_piece.position[0] + dx * step
                ny = selected_piece.position[1] + dy * step
            
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break  # tahtadan çıktı
            
                target = game_board[nx][ny]
            
                if target is None:
                    possible_moves.append((nx, ny))  # boş kare, devam
                elif target.color != player_color:
                    possible_moves.append((nx, ny))  # düşman, yiye dur
                    break
                else:
                    break  # kendi taşı, dur
                
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
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        func(directions, selected_piece, possible_moves)

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

                
 
    