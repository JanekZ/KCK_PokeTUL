import constants as c

from event_handler import EventHandler

class Controller:
    def __init__(self, display, clock, game_states, starting_state):
        self.display = display
        self.clock = clock
        self.game_states = game_states
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
        self.event_handler.handle_events()

    def update_state(self):
        self.state.update()
        if self.state.is_done:
            self.previous_state = self.state
            self.state = None 

    def render_state(self):
        self.state.render(self.display) 
