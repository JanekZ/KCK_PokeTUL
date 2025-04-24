import pygame

class EventHandler:
    def __init__(self):
        ...


    def handle_events(self):
        for event in pygame.event.get():
            self.check_quit_event(event)
            self.check_keyboard_event(event)

    @staticmethod
    def check_quit_event(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    def check_keyboard_event(self, event):
        ...
