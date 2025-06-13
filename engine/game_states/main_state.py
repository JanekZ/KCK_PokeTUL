import engine.constants as c
from engine.game_state import GameState

class MainState(GameState):
    def __init__(self, layers):
        super(MainState, self).__init__(layers)
        self.next_state_name = None
