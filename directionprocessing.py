import constants as c
from algorithms.collision_detection import CollisionDetection

class DirectionProcessing:
    def __init__(self, layers):
        self.camera_mode = c.MOVING_CAMERA
        self.layers = layers
        self.jump = False
        self.jump_destination = None

    def change_direction(self, top_node):
        direction = top_node.value if top_node is not None else c.STOP
        d_xy = c.MOVE_TRANSLATE[direction]
        characters = [character for character in self.layers[c.CHARACTERS_LAYER]]

        collision_detection = CollisionDetection(characters[0], d_xy)

        is_collision_with_portal, destination = collision_detection.check_collision_with_portal(self.layers[c.PORTAL_LAYER])
        if is_collision_with_portal:
            self.jump = True
            self.jump_destination = destination

        is_collision_with_building, num_of_collisions = collision_detection.check_collision(self.layers[c.BUILDINGS_LAYER])
        is_out_of_bounds = collision_detection.check_out_of_bounds(self.layers[c.BACKGROUND_LAYER])
        
        if is_collision_with_building or is_out_of_bounds or is_collision_with_portal:
            if self.camera_mode == c.STATIC_CAMERA:
                for obj in self.layers[c.CHARACTERS_LAYER]:
                    obj.d_x, obj.d_y = c.MOVE_TRANSLATE[c.STOP]

            if self.camera_mode == c.MOVING_CAMERA:
                for layer in self.layers[:c.CHARACTERS_LAYER]:
                    for obj in layer:
                        obj.d_x, obj.d_y = c.MOVE_TRANSLATE[c.STOP]
        else:
            if self.camera_mode == c.STATIC_CAMERA:
                for obj in self.layers[c.CHARACTERS_LAYER]:
                    obj.d_x, obj.d_y = d_xy
            if self.camera_mode == c.MOVING_CAMERA:
                for layer in self.layers[:c.CHARACTERS_LAYER]:
                    for obj in layer:
                        obj.d_x, obj.d_y = -d_xy[0], -d_xy[1]

    def get_updated_layers(self):
        return self.layers