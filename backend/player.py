
import random
from logger import logger
# player.py'e ekle
import threading
player_list_lock = threading.Lock()
colors = ["white", "black"]
player_list = []
player_id_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99]
class player:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.id = player_id_list.pop(0)
        self.color = None
        player_list.append(self)
        self.determine_color()

    def determine_color(self):
        logger.debug(f"Determining color for {len(player_list)} players")
        if self == player_list[0]:
            player_list[0].color = random.choice(colors)
            return 
        elif self == player_list[1]:
            player_list[1].color = "black" if any(p.color == "white" for p in player_list) else "white"
            return 
        else: 
            self.color = "watcher"   
            return 

    def get_name(self):
        if self.color is None:
            return "Player " + str(self.id)
        return "Player " + str(self.id) + " (" + self.color + ")"
    def __del__(self):
        player_id_list.append(self.id)
        player_id_list.sort()
        self.socket.close()