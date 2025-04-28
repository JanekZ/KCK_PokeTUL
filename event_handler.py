import pygame
from commands import *

class EventHandler:
    def __init__(self):
        self.up_command = UpCommand()
        self.down_command = DownCommand()
        self.left_command = LeftCommand()
        self.right_command = RightCommand()


    def handle_events(self, state):
        for event in pygame.event.get():
            self.check_quit_event(event)
            self.check_keyboard_event(event, state)

    @staticmethod
    def check_quit_event(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    def check_keyboard_event(self, event, state):
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
