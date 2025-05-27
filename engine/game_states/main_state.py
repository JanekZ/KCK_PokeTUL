import constants as c
from game_state import GameState

class MainState(GameState):
    def __init__(self, layers):
        super(MainState, self).__init__(layers)
        self.next_state_name = None