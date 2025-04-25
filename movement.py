import constants as c
from Algorithms.collision_detection import CollisionDetection

class Movement:
    def __init__(self, layers):
        self.camera_mode = c.STATIC_CAMERA
        self.layers = layers

    def change_direction(self, top_node):
        direction = top_node.value if top_node is not None else c.STOP
        d_xy = c.MOVE_TRANSLATE[direction]
        characters = [character for character in self.layers[-1]]

        collision_detection = CollisionDetection(characters[0], self.layers[0], d_xy)
        is_collision, num_of_collisions = collision_detection.check_collision()

        if is_collision:
            if self.camera_mode == c.STATIC_CAMERA:
                for obj in self.layers[-1]:
                    obj.d_x, obj.d_y = c.MOVE_TRANSLATE[c.STOP]
        else:
            if self.camera_mode == c.STATIC_CAMERA:
                for obj in self.layers[-1]:
                    obj.d_x, obj.d_y = d_xy

    def get_updated_layers(self):
        return self.layers