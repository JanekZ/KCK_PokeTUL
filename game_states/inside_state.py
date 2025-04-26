from game_state import GameState

class InsideState(GameState):
    def __init__(self):
        super(InsideState, self).__init__("terrains/inside_terrain.txt")