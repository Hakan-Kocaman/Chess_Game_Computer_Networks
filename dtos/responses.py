from abc import ABC

class response(ABC):
    def __init__(self, URL, sender, reciever_list):
        self.URL = URL
        self.sender = sender
        self.reciever_list = reciever_list

class move_response(response):
    def __init__(self, URL, sender, reciever_list,move_result):
        super().__init__(URL, sender, reciever_list)

        self.move_result = move_result

class chat_response(response):
    def __init__(self, URL, sender, reciever_list, message):
        super().__init__(URL, sender, reciever_list)

        self.message = message

class get_possible_moves_response(response):
    def __init__(self, URL, sender, reciever_list, possible_moves):
        super().__init__(URL, sender, reciever_list)

        self.possible_moves = possible_moves

class start_game_response(response):
    def __init__(self, URL, sender, reciever_list, white,black):
        super.__init__(URL, sender, reciever_list)

        self.white = white
        self.black = black

class turn_change_response(response):
    def __init__(self,URL, sender, reciever_list, current_turn):
        super().__init__(URL, sender, reciever_list)

        self.reciever_list = reciever_list
        self.current_turn = current_turn

        
class finish_game_response(response):
    def __init__(self, URL, sender, reciever_list, winner,loser,result):
        super().__init__(URL, sender, reciever_list)

        self.winner = winner
        self.loser = loser
        self.result = result