import pygame
import constants as c

class Graphics:
    def __init__(self) -> None:
        self.canvas = pygame.Surface(c.NATIVE_SIZE)
        self.layers = []

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

    def set_layers(self, layers: list):
        self.layers = layers
