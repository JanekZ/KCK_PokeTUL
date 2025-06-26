import pygame
import constants as c
from entities.building import Building, Blockade
from entities.character import Character
from entities.background import Background

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
                new_entity = Background(entity_x, entity_y, "engine/images/outside_dupe.png")
                layers_dict[c.BACKGROUND].add(new_entity)




        """
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
        """
    return list(layers_dict.values())
