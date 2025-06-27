import pygame

import engine.constants as c

class Background(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image_path: str):
        """
        CALLING SUPER INIT:
            Calling pygame.sprite.Sprite initializer for all the functionality of parent class.

        DIMENSION SET:
            Setting width, height, x, y and x and y-axis change.

        IMAGE SET:
            Setting up image, which is a surface with correct dimension filled with color.

        RECTANGLE SET:
            Setting up rect, which is a pygame.rect used as a bounds of the object.

        :param x: Global x value
        :param y: Global y value
        :param image_path: Path of the object
        """
        super(Background, self).__init__()
        self.image = pygame.image.load(image_path)
        self.width, self.height = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = x
        self.y = y

        self.d_x = 0
        self.d_y = 0

    def update(self) -> None:
        """
        RECTANGLE X AND Y CHANGE:
            Changing the rectangle x and y, by incrementing it with correct axis speed/change.
        """
        self.rect.x += self.d_x
        self.rect.y += self.d_y
