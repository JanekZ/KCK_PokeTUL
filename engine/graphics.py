import pygame
import constants as c

class Graphics:
    def __init__(self, layers: list):
        """
        SETTING UP:
            Pygame Surface initialized with native screen size is used to create canvas.
            Layers will have all the elements that need to be rendered.
        """
        self.canvas = pygame.Surface(c.NATIVE_SIZE)
        self.layers = layers

    def render(self, display) -> None:
        """
        SCREEN CLEARING:
            Canvas gets filled with black color to hide previous frame.

        DRAWING:
            All layers are drawn on the canvas.

        SCALING:
            With scaled display every element has to be transformed.

        :param display: Pygame Surface object that all the elements get rendered on.
        """
        self.canvas.fill((0,0,0))

        for layer in self.layers:
            layer.draw(self.canvas)

        if c.SCALE > 1:
            pygame.transform.scale(self.canvas, c.DISPLAY_SIZE, display)
        else:
            display.blit(self.canvas, c.TOP_LEFT)
        pygame.display.update()

    def update(self) -> None:
        """
        UPDATE LOOP:
            Calls every element to update itself.
        """
        for layer in self.layers:
            layer.update()

# GETTERS AND SETTERS

    def set_layers(self, layers: list) -> None:
        self.layers = layers
