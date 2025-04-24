import pygame
import constants as c

from static_entity import StaticEntity
from builder import Builder

class Graphics:
    def __init__(self) -> None:
        self.canvas = pygame.Surface(c.NATIVE_SIZE)

        builder = Builder("empty")
        builder.build()

        self.layers = builder.get_layers()

        self.update()

    def render(self, display):
        self.canvas.fill((0,0,0))

        for layer in self.layers:
            layer.draw(self.canvas)

        if c.SCALE >= 1:
            pygame.transform.scale(self.canvas, c.DISPLAY_SIZE, display)
        else:
            display.blit(self.canvas, c.TOP_LEFT)
        pygame.display.update()

    def update(self):
        for layer in self.layers:
            layer.update()

