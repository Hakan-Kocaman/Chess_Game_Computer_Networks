
class request():
    def __init__(self, URL, sender, body):
        self.URL = URL
        self.sender = sender
        self.body = body

class move_request_body():
    def __init__(self, selected_piece, new_position):
        self.selected_piece = selected_piece
        self.new_position = new_position

class chat_request_body():
    def __init__(self, message):
        self.message = message

class get_possible_moves_request_body():
    def __init__(self, selected_piece):
        self.selected_piece = selected_piece