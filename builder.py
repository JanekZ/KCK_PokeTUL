import pygame
import constants as c
from static_entity import StaticEntity
from dynamic_entity import DynamicEntity

class Builder:
    def __init__(self, data: str):
        self.data = data
        self.backgrounds = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.layers = [self.backgrounds, self.buildings, self.characters]

    def build(self):
        background = StaticEntity()
        background.set_position(10, 10)
        background.set_dimensions(c.NATIVE_WIDTH-20, c.NATIVE_HEIGHT-20)
        background.set_image((255,255,255))
        background.set_rect()
        self.backgrounds.add(background)

        building = StaticEntity()
        building.set_position(10, 10)
        building.set_dimensions(20, 20)
        building.set_image((100, 100, 100))
        building.set_rect()
        self.buildings.add(building)

        building2 = StaticEntity()
        building2.set_position(50, 50)
        building2.set_dimensions(20, 20)
        building2.set_image((200, 200, 200))
        building2.set_rect()
        self.buildings.add(building2)

        character = DynamicEntity()
        character.set_position(100, 50)
        character.set_dimensions(c.CHARACTER_WIDTH, c.CHARACTER_HEIGHT)
        character.set_image((100, 200, 100))
        character.set_rect()
        self.characters.add(character)

    def get_layers(self):
        return self.layers
