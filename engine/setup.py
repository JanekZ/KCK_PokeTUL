import pygame
import engine.constants as c

from engine.controller import Controller
# List of all the states
from engine.game_states.main_state import MainState
from engine.game_states.inside_state import InsideState
from engine.game_states.second_inside_state import SecondInsideState


def init() -> None:
    """
    PYGAME INITIALIZATION:
        Function call initializes all import pygame modules that will be needed for proper functionality of the code.
    """
    pygame.init()

def get_clock() -> pygame.time.Clock:
    """
    CLOCK INITIALIZATION:
        Only returns initialized clock object.

    :return: Pygame Clock object responsible for maintaining stable frame rate.
    """
    return pygame.time.Clock()

def get_display() -> pygame.surface.Surface:
    """
    DISPLAY INITIALIZATION:
        Only returns display initialized with display size taken from constants.py

    :return: Pygame Surface object that everything will be rendered on.
    """
    display = pygame.display.set_mode(c.DISPLAY_SIZE)
    return display

def get_game_states() -> dict:
    """
    GAME STATES DICTIONARY:
        Creation of dictionary containing game state name as key and not yet initialized game state object as value.

    :return: Dictionary containing all the game states.
    """
    game_states = {c.MAIN_SCREEN: MainState, c.INSIDE_SCREEN: InsideState, c.SECOND_INSIDE_SCREEN: SecondInsideState}
    return game_states

def get_controller(display, clock, game_states, starting_state):
    """
    CONTROLLER INITIALIZATION:
        Only returns controller object initialized with given parameters.

    :param display: Pygame display object, main window that everything is rendered in.
    :param clock: Pygame clock object, that monitors time and sets correct and stable FPS.
    :param game_states: Dictionary with game state name as key, and not initialized game state objects as values.
    :param starting_state: Name of the first game state.

    :return: Controller object responsible for the engine functionality.
    """
    return Controller(display, clock, game_states, starting_state)
