import pygame
import constants as c

class StaticEntity(pygame.sprite.Sprite):
    def __init__(self):
        super(StaticEntity, self).__init__()

        self.width = 0
        self.height = 0
        self.image = None
        self.rect = None
        self.color = []

        self.x = 0
        self.y = 0
        self.d_x = 0
        self.d_y = 0

    def update(self):
        self.update_position()

    def update_position(self):
        self.rect.x += self.d_x
        self.rect.y += self.d_y

    def set_dimensions(self, width: int, height: int):
        self.width = width
        self.height = height

    def set_image(self, color: tuple[int, int, int]):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.color = color

    def set_rect(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def set_color(self, color: tuple[int, int, int]):
        self.color = color

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y

class Portal(StaticEntity):
    def __init__(self, destination):
        super(Portal, self).__init__()
        self.destination = destination