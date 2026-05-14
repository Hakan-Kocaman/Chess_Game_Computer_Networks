from abc import ABC

class response(ABC):
    def __init__(self, URL, sender):
        self.URL = URL
        self.sender = sender

class move_response(response):
    def __init__(self, URL, sender,move_result):
        super().__init__(URL, sender)

        self.move_result = move_result

class chat_response(response):
    def __init__(self, URL, sender, message):
        super().__init__(URL, sender)

        self.message = message

class get_possible_moves_response(response):
    def __init__(self, URL, sender, possible_moves):
        super().__init__(URL, sender)

        self.possible_moves = possible_moves

class start_game_response(response):
    def __init__(self, URL, sender, white,black):
        super().__init__(URL, sender)

        self.white = white
        self.black = black

class turn_change_response(response):
    def __init__(self,URL, sender, current_turn):
        super().__init__(URL, sender)

        self.current_turn = current_turn

        
class finish_game_response(response):
    def __init__(self, URL, sender, winner,loser,result):
        super().__init__(URL, sender)

        self.winner = winner
        self.loser = loser
        self.result = result


class connection_lost_response(response):
    def __init__(self, URL, sender, who):
        super().__init__(URL, sender)
        self.who = who