import pygame
import constants as c
from static_entity import StaticEntity
from dynamic_entity import DynamicEntity

class Builder:
    def __init__(self, data: str):
        self.data = data
        self.buildings = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.layers = [self.buildings, self.characters]

    def build(self):
        building = StaticEntity()
        building.set_position(0, 0)
        building.set_dimensions(50, 50)
        building.set_image((100, 100, 100))
        building.set_rect()
        self.buildings.add(building)

        building2 = StaticEntity()
        building2.set_position(50, 50)
        building2.set_dimensions(50, 50)
        building2.set_image((200, 200, 200))
        building2.set_rect()
        self.buildings.add(building2)

        character = DynamicEntity()
        character.set_position(50, 50)
        character.set_dimensions(50, 50)
        character.set_image((100, 200, 100))
        character.set_rect()
        self.characters.add(character)

    def get_layers(self):
        return self.layers
