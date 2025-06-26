import constants as c
import pygame


class Building(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image_path: str, building_name: str | None):
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
        super(Building, self).__init__()
        self.image = pygame.image.load(image_path)
        self.width, self.height = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = x
        self.y = y

        self.d_x = 0
        self.d_y = 0

        self.building_name = building_name

    def create_portal(self):
        off_x, off_y, width, height = c.PORTAL_OFFSET[self.building_name]
        if off_x is None or off_y is None:
            return None

        portal_x = self.x + off_x*c.TILE_WIDTH
        portal_y = self.y + off_y*c.TILE_HEIGHT

        portal = Portal(portal_x, portal_y, width, height, c.SECOND_INSIDE_SCREEN)

        return portal

    def create_front(self, front_path: str):
        front_image = pygame.image.load(front_path)
        image_width, image_height = front_image.get_size()

        image_x = self.x - (image_width - self.width)
        image_y = self.y - (image_height - self.height)

        front = Building(image_x, image_y, front_path, None)

        return front

    def update(self) -> None:
        """
        RECTANGLE X AND Y CHANGE:
            Changing the rectangle x and y, by incrementing it with correct axis speed/change.
        """
        self.rect.x += self.d_x
        self.rect.y += self.d_y

class Portal(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, destination: str):
        super(Portal, self).__init__()

        self.destination = destination

        self.image = pygame.Surface((width, height))
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

class Blockade(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        super(Blockade, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill((52,75,35))
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
