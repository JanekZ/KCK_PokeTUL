import pygame
import constants as c
from static_entity import StaticEntity, Portal
from dynamic_entity import DynamicEntity

def build(build_file: str) -> dict:
    backgrounds = pygame.sprite.Group()
    buildings = pygame.sprite.Group()
    portals = pygame.sprite.Group()
    characters = pygame.sprite.Group()
    layers_dict = {c.BACKGROUND: backgrounds,
                        c.BUILDING: buildings,
                        c.PORTAL: portals,
                        c.CHARACTER: characters}

    with open(build_file, "r") as f:
        for row in f:
            line = row.rstrip().split(" ")
            line = [int(value) if  8 > idx >= 1 else value for idx, value in enumerate(line)]
            box_type, x, y, width, height, r, g, b = line[:8]

            if box_type in [c.BUILDING, c.BACKGROUND]:
                new_element = StaticEntity(x, y, width, height, (r,g,b))
            elif box_type == c.PORTAL:
                portal_destination = line[8]
                new_element = Portal(x, y, width, height, (r,g,b), portal_destination)
            else:
                new_element = DynamicEntity(x, y, width, height, (r,g,b))

            layers_dict[box_type].add(new_element)


    return list(layers_dict.values())