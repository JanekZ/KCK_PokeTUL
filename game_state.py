import constants as c

from graphics import Graphics
from builder import Builder
from algorithms.dll_stack import DLLStack
from directionprocessing import DirectionProcessing

class GameState:
    def __init__(self, data_file: str):
        self.is_done = False
        self.next_state_name = None

        self.graphics = Graphics()
        self.movement_stack = DLLStack()
        self.builder = Builder(data_file)
        self.builder.build()
        self.movement_processing = DirectionProcessing(self.builder.get_layers())

    def update(self):
        self.movement_processing.change_direction(self.movement_stack.head)

        if self.movement_processing.jump is True:
            self.movement_stack.clear()
            self.next_state_name = self.movement_processing.jump_destination
            self.is_done = True
            self.movement_processing.jump = False
            self.movement_processing.jump_destination = None

        self.graphics.set_layers(self.movement_processing.get_updated_layers())
        self.graphics.update()

    def render(self, display):
        self.graphics.render(display)

    def user_input(self, action: str, key: str|None = None):
        if action == c.PUSH:
            self.movement_stack.push(key)
        if action == c.POP:
            if self.movement_stack.top() is not None:
                on_top = self.movement_stack.top().value
                if on_top == key:
                    self.movement_stack.pop()
                else:
                    self.movement_stack.remove(key)