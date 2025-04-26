import setup
import constants as c

def main():
    setup.init()
    clock = setup.get_clock()
    display = setup.get_display()
    game_states = setup.get_game_states()

    controller = setup.get_controller(display, clock, game_states, c.MAIN_SCREEN)
    controller.run()


if __name__ == "__main__":
    main()
