import os

import engine.setup as setup
import engine.constants as c

from engine.utils.auth_screen import login_screen
from engine.utils.login_session import load_session

from database.utils.auth import Auth

auth = Auth()

def main() -> None:
    """
    SETUP FUNCTIONS:
        Calls the setup.py functions to initialize variables responsible for correct setup of controller object.
    CONTROLLER RUN:
        Prompts the controller object to start the main game loop.
    """
    setup.init()
    clock = setup.get_clock()
    display = setup.get_display()
    game_states = setup.get_game_states()
    controller = setup.get_controller(display, clock, game_states, c.MAIN_SCREEN)

    session_id = load_session()

    if session_id is None or not auth.validate_session(session_id):
        session_id = login_screen(display, clock)

        if session_id is None:
            print("Niepoprawna lub wygasła sesja.")
            return

    controller.run()

if __name__ == "__main__":
    """
    FUNCTION CALL:
        Calls the main function only if the python file is run directly.
    """
    main()
