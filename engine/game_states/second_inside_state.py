from game_state import GameState

class SecondInsideState(GameState):
    def __init__(self):
        super(SecondInsideState, self).__init__("engine/terrains/second_inside_terrain.txt")