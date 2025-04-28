import pygame
import constants as c
from static_entity import StaticEntity, Portal
from dynamic_entity import DynamicEntity

class Builder:
    def __init__(self, build_file: str):
        self.build_file = build_file
        self.backgrounds = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.layers = [self.backgrounds, self.buildings, self.portals, self.characters]

    def build(self):
        with open(self.build_file, "r") as f:
            for row in f:
                line = row.rstrip().split(" ")
                line = [int(value) if  8 > idx >= 1 else value for idx, value in enumerate(line)]
                box_type, x, y, width, height, r, g, b = line[:8]
                if box_type in [c.BUILDING, c.BACKGROUND]:
                    new_element  = StaticEntity()
                elif box_type == c.PORTAL:
                    portal_destination = line[8]
                    new_element = Portal(portal_destination)
                else:
                    new_element = DynamicEntity()

                new_element.set_position(x, y)
                new_element.set_dimensions(width, height)
                new_element.set_image((r,g,b))
                new_element.set_rect()

                if box_type == c.BUILDING:
                    self.buildings.add(new_element)
                elif box_type == c.BACKGROUND:
                    self.backgrounds.add(new_element)
                elif box_type == c.PORTAL:
                    self.portals.add(new_element)
                elif box_type == c.CHARACTER:
                    self.characters.add(new_element)


    def get_layers(self):
        return self.layers
