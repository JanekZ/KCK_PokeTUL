import engine.constants as c

from engine.event_handler import EventHandler
from engine.algorithms.dll_stack import DLLStack

from engine.builder import build

class Controller:
    def __init__(self, display, clock, game_states, starting_state):
        """
        SETTING UP THE MAIN FUNCTIONALITY OF THE GAME ENGINE:
            Sets up class properties using given parameters.
            Creates event handler.
            Sets up property in charge of maintaining the game loop.

        :param display: Pygame display object, main window that everything is rendered in.
        :param clock: Pygame clock object, that monitors time and sets correct and stable FPS.
        :param game_states: Dictionary with game state name as key, and not initialized game state objects as values.
        :param starting_state: Name of the first game state.
        """
        self.display = display
        self.clock = clock
        self.game_states = game_states

        self.game_state_stack = DLLStack()

        self.start_state(starting_state)
        self.state = self.game_state_stack.top().value

        self.event_handler = EventHandler()
        self.running = True

    def start_state(self, state_name) -> None:
        """
        NEW STATE START:
            Initializes a new Game State object with dictionary of Entity objects as a parameter.
            Makes a push to the stack.

        :param state_name: Name of the new state.
        """
        self.game_state_stack.push(self.game_states[state_name](build(c.STATE_DICT[state_name])))

    def run(self) -> None:
        """
        MAIN GAME LOOP:
            Runs the main loop that the game is happening in.
            Invokes all the functions that are crucial for the engine to work.
            Changing the order of those function calls can change the outcome of the loop.
        """
        while self.running:
            self.clock_tick()
            self.handle_events()
            self.update_state()
            self.render_state()

    def clock_tick(self) -> None:
        """
        CLOCK FPS:
            Regulates stable frame rate by introducing delays.
        """
        self.clock.tick(c.FPS)

    def handle_events(self) -> None:
        """
        EVENT HANDLING:
            Prompts the event handler object to check all the events that are currently happening.
        """
        self.event_handler.handle_events(self.state)

    def update_state(self) -> None:
        """
        UPDATING THE STATE:
            Prompts the state to update itself.
        CHECKING IF CHANGE OF STATE IS NEEDED:
            After updating the state, check if state status for change is set to True.
            If change is needed, previous state is set to current, and current state is set to given state.
            After change cleaning is needed, so that previous state doesn't end instantly.
        """
        self.state.update()

        if self.state.is_done:
            if self.state.next_state_name == c.NO_JUMP:
                self.game_state_stack.pop()
            else:
                self.game_state_stack.top().value.is_done = False
                self.start_state(self.state.next_state_name)

        self.state = self.game_state_stack.top().value

    def render_state(self) -> None:
        """
        RENDER THE STATE:
            Prompts the state to render itself.
        """
        self.state.render(self.display)
