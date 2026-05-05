from abc import ABC

class request(ABC):
    def __init__(self, URL, sender, body):
        self.URL = URL
        self.sender = sender

    
class move_request(request):
    def __init__(self, URL, sender, selected_piece, new_position):
        super().__init__(URL, sender)

        self.selected_piece = selected_piece
        self.new_position = new_position

class chat_request(request):
    def __init__(self, URL, sender, message):
        super().__init__(URL, sender)

        self.message = message

class get_possible_moves_request(request):
    def __init__(self, URL, sender, selected_piece):
        super().__init__(URL, sender)

        self.selected_piece = selected_piece