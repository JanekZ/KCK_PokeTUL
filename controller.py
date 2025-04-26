import pygame.time

import constants as c

from event_handler import EventHandler

class Controller:
    def __init__(self, display, clock, game_states, starting_state):
        self.display = display
        self.clock = clock
        self.game_states = game_states
        self.previous_state = None
        self.state = self.game_states[starting_state]()
        self.event_handler = EventHandler()
        self.running = True


    def run(self):
        while self.running:
            self.clock_tick()
            self.handle_events()
            self.update_state()
            self.render_state()

    def clock_tick(self):
        self.clock.tick(c.FPS)

    def handle_events(self):
        self.event_handler.handle_events(self.state)

    def update_state(self):
        self.state.update()
        if self.state.is_done and self.previous_state is None:
            self.previous_state = self.state
            self.previous_state.is_done = False
            self.state = self.game_states[self.previous_state.next_state_name]()
        elif self.state.is_done:
            self.state = self.previous_state
            self.previous_state = None


    def render_state(self):
        self.state.render(self.display) 
