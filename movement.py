import constants as c

class Movement:
    def __init__(self, layers):
        self.layers = layers

    def change_direction(self, top_node):
        direction = top_node.value if top_node is not None else c.STOP
        for layer in self.layers:
            for obj in layer:
                obj.d_x, obj.d_y = c.MOVE_TRANSLATE[direction]

    def get_updated_layers(self):
        return self.layers