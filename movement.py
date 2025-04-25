import constants as c
import Algorithms.collision_detection

class Movement:
    def __init__(self, layers):
        self.camera_mode = c.STATIC_CAMERA
        self.layers = layers

    def change_direction(self, top_node):
        direction = top_node.value if top_node is not None else c.STOP

        if self.camera_mode == c.STATIC_CAMERA:
            for obj in self.layers[-1]:
                obj.d_x, obj.d_y = c.MOVE_TRANSLATE[direction]

    def get_updated_layers(self):
        return self.layers