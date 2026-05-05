
class move_request():
    def __init__(self, URL, sender, selected_piece, new_position):
        self.URL = URL
        self.sender = sender
        self.selected_piece = selected_piece
        self.new_position = new_position

class chat_request():
    def __init__(self, URL, sender, message):
        self.URL = URL
        self.sender = sender
        self.message = message

class get_possible_moves_request():
    def __init__(self, URL, sender, selected_piece):
        self.URL = URL
        self.sender = sender
        self.selected_piece = selected_piece