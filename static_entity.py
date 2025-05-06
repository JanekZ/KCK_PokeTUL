import pygame

class StaticEntity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int,int,int]):
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

    def update(self):
        self.rect.x += self.d_x
        self.rect.y += self.d_y

class Portal(StaticEntity):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int,int,int], destination):
        super(Portal, self).__init__(x, y, width, height, color)
        self.destination = destination