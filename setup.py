import pygame
import constants as c

from controller import Controller
from game_states.main_state import MainState
from game_states.inside_state import InsideState

def init() -> None:
    pygame.init()

def get_clock():
    return pygame.time.Clock()

def get_display():
    display = pygame.display.set_mode(c.DISPLAY_SIZE)
    return display

def get_game_states():
    game_states = {c.MAIN_SCREEN: MainState, c.INSIDE_SCREEN: InsideState}
    return game_states

def get_controller(display, clock, game_states, starting_state):
    return Controller(display, clock, game_states, starting_state)
