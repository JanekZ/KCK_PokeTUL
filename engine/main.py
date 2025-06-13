import setup
import engine.constants as c

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
    controller.run()

if __name__ == "__main__":
    """
    FUNCTION CALL:
        Calls the main function only if the python file is run directly.
    """
    main()
