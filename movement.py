import constants as c
from algorithms.collision_detection import CollisionDetection

class Movement:
    def __init__(self, layers):
        self.camera_mode = c.STATIC_CAMERA
        self.layers = layers

    def change_direction(self, top_node):
        direction = top_node.value if top_node is not None else c.STOP
        d_xy = c.MOVE_TRANSLATE[direction]
        characters = [character for character in self.layers[c.CHARACTERS_LAYER]]

        collision_detection = CollisionDetection(characters[0], d_xy)
        is_collision, num_of_collisions = collision_detection.check_collision(self.layers[c.BUILDINGS_LAYER])
        is_out_of_bounds = collision_detection.check_out_of_bounds(self.layers[c.BACKGROUND_LAYER])
        if is_collision or is_out_of_bounds:
            if self.camera_mode == c.STATIC_CAMERA:
                for obj in self.layers[c.CHARACTERS_LAYER]:
                    obj.d_x, obj.d_y = c.MOVE_TRANSLATE[c.STOP]
        else:
            if self.camera_mode == c.STATIC_CAMERA:
                for obj in self.layers[c.CHARACTERS_LAYER]:
                    obj.d_x, obj.d_y = d_xy

    def get_updated_layers(self):
        return self.layers