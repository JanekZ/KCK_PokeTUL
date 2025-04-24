import constants as c

from graphics import Graphics
from builder import Builder

class GameState:
    def __init__(self):
        self.is_done = False
        self.graphics = Graphics()

        self.builder = Builder("Empty")
        self.builder.build()
        self.set_graphics(self.builder.get_layers())

    def update(self):
        self.graphics.update()

    def render(self, display):
        self.graphics.render(display)

    def set_graphics(self, layers: list):
        self.graphics.set_layers(layers)