import engine.constants as c

from engine.graphics import Graphics
from engine.algorithms.dll_stack import DLLStack
from engine.movement_processor import MovementProcessor
from engine.ui import draw_ui
import pygame


class GameState:
    def __init__(self, layers: dict):

        self.show_map = False #the minimap is hidden by default.
        """
        STATUS:
            Class properties used for showing the current status of the state.
            Show if the state is done, ready to change to another state.
            Name of the state that will be next.

        IMPORTANT OBJECTS:
            Objects needed for proper functionality of the game state.
            Graphics object that updates and renders and holds all elements.
            DLLStack object needed to maintain fluid change of movements direction.
            MovementProcessor object that handles the change in direction.

        :param layers: Dictionary of all the objects that need to be rendered on screen.
        """
        self.is_done = False
        self.next_state_name = None

        self.graphics = Graphics(layers)
        self.movement_stack = DLLStack()

        self.movement_processor = MovementProcessor(c.MOVING_CAMERA)

    def update(self) -> None:
        """
        DIRECTION CHANGE:
            Movement processor changes the direction to direction of head element in stack.

        STATE CHANGE CHECK:
            If change is needed movement stack is cleared to avoid errors.
            Next state name is set using movement processor that checks what portal character collided with.
            State status is changed to done.
            Lastly cleaning is needed to avoid instant change of game state after coming back.

        SETTING AND UPDATING LAYERS:
            Graphics layers are updates using layers kept by movement processor.
            Graphics object updates all the layers.
        """
        jump = False
        self.movement_processor.change_direction(self.movement_stack.head, self.graphics.layers)
        if self.movement_processor.jump is True:
            self.movement_stack.clear()
            self.next_state_name = self.movement_processor.get_destination()
            self.is_done = True

        self.graphics.update()

    def render(self, display) -> None:
        """
        RENDER:
            Prompts graphics object to render all the layers to display given using parameters.

        :param display: Pygame Surface object used as display to show all elements.
        """
        if self.show_map:
            characters = [c for c in self.graphics.layers[4]]
            if characters:
                character = characters[0]
                player_pos = (character.rect.x, character.rect.y)
            else:
                player_pos = (0, 0)

            self.graphics.render_full_map(display, player_pos)
        else:
            self.graphics.render(display)
            dummy_pos = (0, 0)
            draw_ui(display, dummy_pos, show_menu=True)
            pygame.display.update()

    def user_input(self, action: str, key: str|None = None) -> None:
        """
        EXECUTION:
            Action value is checked to find what kind of action has to be executed.
            PUSH: Adds new direction change on top of the stack.
            POP: Checks what direction has to be removed, if top element has it, it gets deleted.
                 Otherwise, all appearances of this direction are deleted from the stack.

        :param action: Text value representing what action has to be executed.
        :param key: Text value used for more accurate execution of given action.
        """
        if action == c.PUSH:
            self.movement_stack.push(key)
        if action == c.POP:
            if self.movement_stack.top() is not None:
                on_top = self.movement_stack.top().value
                if on_top == key:
                    self.movement_stack.pop()
                else:
                    self.movement_stack.remove(key)
