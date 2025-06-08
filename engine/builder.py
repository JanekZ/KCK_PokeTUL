import pygame
import constants as c
from static_entity import StaticEntity, Portal
from dynamic_entity import DynamicEntity
from building import Building

def build(build_file: str) -> dict:
    backgrounds = pygame.sprite.Group()
    buildings = pygame.sprite.Group()
    fronts = pygame.sprite.Group()
    portals = pygame.sprite.Group()
    characters = pygame.sprite.Group()
    layers_dict = {c.BACKGROUND: backgrounds,
                        c.BUILDING: buildings,
                        c.BUILDING_FRONT: fronts,
                        c.PORTAL: portals,
                        c.CHARACTER: characters}

    with open(build_file, "r") as f:

        new_element = Building(-50, -50, "images/DMCS_znacznik.png", c.DMCS)
        portal = new_element.create_portal()
        building_front = new_element.create_front("images/DMCS_budynek.png")

        layers_dict[c.BUILDING_FRONT].add(building_front)
        layers_dict[c.PORTAL].add(portal)
        layers_dict[c.BUILDING].add(new_element)

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
                new_element = DynamicEntity(c.CHARACTER_SCREEN_CENTER_WIDTH, c.CHARACTER_SCREEN_CENTER_HEIGHT, width, height, (r,g,b))

            layers_dict[box_type].add(new_element)

    return list(layers_dict.values())