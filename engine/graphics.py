import pygame
import engine.constants as c

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
        self.canvas.fill((52,75,35))

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


    def set_layers(self, layers: list) -> None:
        self.layers = layers

    def render_full_map(self, surface, player_pos):

        self.canvas.fill((0, 0, 0))
        scale = 0.1
        for layer in self.layers:
            for sprite in layer:
                if hasattr(sprite, 'image') and hasattr(sprite, 'rect'):
                    img = pygame.transform.scale(sprite.image,
                                                 (int(sprite.rect.width * scale), int(sprite.rect.height * scale)))
                    pos = (int(sprite.rect.x * scale), int(sprite.rect.y * scale))
                    self.canvas.blit(img, pos)

        if player_pos:
            px = int(player_pos[0] * scale)
            py = int(player_pos[1] * scale)
            pygame.draw.circle(self.canvas, (255, 0, 0), (px, py), 4)

        pygame.transform.scale(self.canvas, surface.get_size(), surface)
        pygame.display.update()