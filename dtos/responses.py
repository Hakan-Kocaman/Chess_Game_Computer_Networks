
class move_response():
    def __init__(self, URL, sender, reciever_list,move_result):
        self.URL = URL
        self.sender = sender
        self.reciever_list = reciever_list
        self.move_result = move_result

class chat_response():
    def __init__(self, URL, sender, reciever_list, message):
        self.URL = URL
        self.sender = sender
        self.reciever_list = reciever_list
        self.message = message

class get_possible_moves_response():
    def __init__(self, URL, sender, reciever_list, possible_moves):
        self.URL = URL
        self.sender = sender
        self.reciever_list = reciever_list
        self.possible_moves = possible_moves

class start_game_response():
    def __init__(self, URL, sender, reciever_list, white,black):
        self.URL = URL
        self.sender = sender
        self.reciever_list = reciever_list
        self.white = white
        self.black = black

class turn_change_response():
    def __init__(self,URL, sender, reciever_list, current_turn):
        self.URL = URL
        self.sender = sender
        self.reciever_list = reciever_list
        self.current_turn = current_turn

        
class finish_game_response():
    def __init__(self, URL, sender, reciever_list, winner,loser,result):
        self.URL = URL
        self.sender = sender
        self.reciever_list = reciever_list
        self.winner = winner
        self.loser = loser
        self.result = result