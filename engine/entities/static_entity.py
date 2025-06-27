import pygame

import engine.constants as c

class StaticEntity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int,int,int]):
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
        :param width: Width of the object
        :param height: Height of the object
        :param color: Color of the object
        """
        super(StaticEntity, self).__init__()

        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.color = color

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

class Portal(StaticEntity):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int,int,int], destination: str):
        """
        CALLING SUPER INIT:
            Calling StaticEntity init to create proper object with all its properties.

        SETTING UP:
            Setting up portal destination as class property.

        :param destination: Text value holding destinations name.
        """
        super(Portal, self).__init__(x, y, width, height, color)

        self.destination = destination
        self.is_locked = False
