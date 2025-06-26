import pygame

import engine.constants as c

from engine.entities.building import Building, Blockade
from engine.entities.character import Character
from engine.entities.background import Background

from engine.utils.fix_path import fix_path

def build(build_file: str) -> dict:
    backgrounds = pygame.sprite.Group()
    buildings = pygame.sprite.Group()
    fronts = pygame.sprite.Group()
    portals = pygame.sprite.Group()
    characters = pygame.sprite.Group()
    fx = pygame.sprite.Group()
    layers_dict = {c.BACKGROUND: backgrounds,
                   c.CHARACTER: characters,
                   c.BUILDING: buildings,
                   c.PORTAL: portals,
                   c.BUILDING_FRONT: fronts,
                   c.FX: fx}

    with open(build_file, "r") as f:
        for row in f:
            entity = row.rstrip().split()
            entity_type = entity[0]
            entity_x = int(entity[1])
            entity_y = int(entity[2])

            if entity_type == c.BUILDING:
                building_type = entity[3]
                new_building = Building(entity_x, entity_y, c.BUILDING_FILE_DICTIONARY[building_type][0], building_type)
                building_front = new_building.create_front(c.BUILDING_FILE_DICTIONARY[building_type][1])
                layers_dict[c.BUILDING_FRONT].add(building_front)
                portal = new_building.create_portal()
                if portal is not None:
                    layers_dict[c.PORTAL].add(portal)
                layers_dict[c.BUILDING].add(new_building)
            elif entity_type == c.BLOCKADE:
                width = int(entity[3])
                height = int(entity[4])
                new_blockade = Blockade(entity_x, entity_y, width, height)
                layers_dict[c.BUILDING].add(new_blockade)

            elif entity_type == c.CHARACTER:
                new_character = Character()
                layers_dict[c.CHARACTER].add(new_character)

            else:
                new_entity = Background(entity_x, entity_y, fix_path("images/outside_dupe.png"))
                layers_dict[c.BACKGROUND].add(new_entity)
    return list(layers_dict.values())
