import constants as c

from graphics import Graphics
from builder import Builder
from Algorithms.dll_stack import DLLStack
from movement import Movement

class GameState:
    def __init__(self):
        self.is_done = False

        self.graphics = Graphics()
        self.movement_stack = DLLStack()
        self.builder = Builder("Terrains/inside_terrain.txt")
        self.builder.build()
        self.movement_processing = Movement(self.builder.get_layers())

    def update(self):
        self.movement_processing.change_direction(self.movement_stack.head)
        self.graphics.set_layers(self.movement_processing.get_updated_layers())
        self.graphics.update()

    def render(self, display):
        self.graphics.render(display)

    def user_input(self, action: str, key: str):
        if action == c.PUSH:
            self.movement_stack.push(key)
        elif action == c.POP:
            on_top = self.movement_stack.top().value
            if on_top == key:
                self.movement_stack.pop()
            else:
                self.movement_stack.remove(key)