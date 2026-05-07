
class response:
    def __init__(self, URL, sender, reciever_list, body):
        self.URL = URL
        self.sender = sender
        self.reciever_list = reciever_list
        self.body = body

class move_response_body():
    def __init__(self, move_result):
        self.move_result = move_result

class chat_response_body():
    def __init__(self, message):
        self.message = message

class get_possible_moves_response_body():
    def __init__(self, possible_moves):
        self.possible_moves = possible_moves