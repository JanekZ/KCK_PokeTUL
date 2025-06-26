import pygame
from engine.commands import *

class EventHandler:
    def __init__(self):
        """
        SETTING UP COMMANDS:
            Creating class properties that represent different commands.
        """
        self.up_command = UpCommand()
        self.down_command = DownCommand()
        self.left_command = LeftCommand()
        self.right_command = RightCommand()

    def handle_events(self, state) -> None:
        """
        EVENT LOOP:
            Every event sent to two different function, that check quit events and keyboard events.

        :param state: Current state that will resolve the event.
        """
        for event in pygame.event.get():
            self.check_quit_event(event)
            self.check_keyboard_event(event, state)

    @staticmethod
    def check_quit_event(event) -> None:
        """
        EVENT CHECK:
            Checking if quit event is called.

        :param event: Event sent to be checked.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    def check_keyboard_event(self, event, state) -> None:
        """
        EVENT TYPE CHECK:
            Checking if event type matches any of verified types.

        KEY CHECK:
            Events key is compared to all verified key to find proper command to execute.

        :param event: Event sent to be checked.
        :param state: Current state that will resolve the event.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.up_command.execute(state, c.PUSH)
            if event.key == pygame.K_DOWN:
                self.down_command.execute(state, c.PUSH)
            if event.key == pygame.K_LEFT:
                self.left_command.execute(state, c.PUSH)
            if event.key == pygame.K_RIGHT:
                self.right_command.execute(state, c.PUSH)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.up_command.execute(state, c.POP)
            if event.key == pygame.K_DOWN:
                self.down_command.execute(state, c.POP)
            if event.key == pygame.K_LEFT:
                self.left_command.execute(state, c.POP)
            if event.key == pygame.K_RIGHT:
                self.right_command.execute(state, c.POP)
