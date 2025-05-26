import constants as c
from game_state import GameState

class MainState(GameState):
    def __init__(self):
        super(MainState, self).__init__("engine/terrains/main_terrain.txt")
        self.next_state_name = None