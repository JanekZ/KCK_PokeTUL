import engine.constants as c
from engine.algorithms.collision_detection import CollisionDetection
from engine.entities.character import Character

class MovementProcessor:
    def __init__(self, camera_mode: str) -> None:
        """
        SETTING UP:
            Camera mode states what kind of movement has to be done.
            Layers are set using given parameter.

        STATUS INDICATORS
            Jump and jump destination show if change is needed.

        :param camera_mode: mode of the camera in current game state.
        """
        self.camera_mode = camera_mode
        self.jump = False
        self.jump_destination = None

    def change_direction(self, top_node, layers: list) -> None:
        """
        DIRECTION SET:
            Direction gets extracted from node. Then it gets translated to tuple with x and y-axis change.

        CHARACTER EXTRACTION:
            Character need to be extracted from layer (pygame.sprite.Group), but it can't be indexed, so workaround
            is needed.

        COLLISION DETECTOR INITIALIZATION:
            Collision detection object is initialized with character and x and y-axis change as parameters. At
            initialization clone of character is created with offset of given d_xy.

        PORTAL COLLISION DETECTION:
            Collision detector function is called to check if there is a collision with a portal and gets the destination.
            Jump is resolved properly.

        BUILDING COLLISION AND OUT OF BOUND DETECTION:
            Collision detector function is called to check if there is a collision with a building or if the character
            is about to get ouf of bounds of background.
            If collision is detected, all movement is stopped.

        :param top_node: Node containing direction.
        :param layers: list containing all sprite groups
        """
        direction = top_node.value if top_node is not None else c.STOP
        d_xy = c.MOVE_TRANSLATE[direction]

        characters = [character for character in layers[c.CHARACTERS_LAYER]]
        character = characters[0]
        character.set_direction(direction)

        collision_detector = CollisionDetection(character, d_xy)

        is_collision_with_portal, destination = collision_detector.check_collision_with_portal(layers[c.PORTAL_LAYER])
        if is_collision_with_portal:
            self.jump = True
            self.jump_destination = destination

        is_collision_with_building, num_of_collisions = collision_detector.check_collision(layers[c.BUILDINGS_LAYER])
        is_out_of_bounds = collision_detector.check_out_of_bounds(layers[c.BACKGROUND_LAYER])

        count = 0
        for obj in layers[c.BUILDING_FRONT_LAYER]:
            obj_seen = collision_detector.check_out_of_bounds([obj])
            if not obj_seen:
                count += 1

        is_seen = count == 0
        if not is_seen:
            layers[c.FX_LAYER].empty()
            layers[c.FX_LAYER].add(Character(seen = False))
        else:
            layers[c.FX_LAYER].empty()
        if is_collision_with_building or is_out_of_bounds or is_collision_with_portal:
            if self.camera_mode == c.STATIC_CAMERA:
                for obj in layers[c.CHARACTERS_LAYER]:
                    obj.d_x, obj.d_y = c.MOVE_TRANSLATE[c.STOP]

            if self.camera_mode == c.MOVING_CAMERA:
                for layer in layers[:c.CHARACTERS_LAYER] + layers[c.CHARACTERS_LAYER+1:]:
                    for obj in layer:
                        obj.d_x, obj.d_y = c.MOVE_TRANSLATE[c.STOP]
        else:
            if self.camera_mode == c.STATIC_CAMERA:
                for obj in layers[c.CHARACTERS_LAYER]:
                    obj.d_x, obj.d_y = d_xy
            if self.camera_mode == c.MOVING_CAMERA:
                for layer in layers[:c.CHARACTERS_LAYER] + layers[c.CHARACTERS_LAYER+1:]:
                    for obj in layer:
                        obj.d_x, obj.d_y = -d_xy[0], -d_xy[1]

    def get_destination(self) -> str:
        """
        JUMP DESTINATION:
            Function return jump destination of the newest collision with portal.
            To ensure no mismatch between portals and their jump destination, reset of jump destination is needed.
        :return: Returns jump destination
        """
        temp = self.jump_destination
        self.jump_destination = None
        self.jump = False
        return temp
