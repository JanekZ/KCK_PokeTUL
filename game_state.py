import constants as c

from graphics import Graphics

class GameState:
    def __init__(self):
        self.is_done = False
        self.graphics = Graphics()

    def update(self):
        self.graphics.update()

    def render(self, display):
        self.graphics.render(display)

