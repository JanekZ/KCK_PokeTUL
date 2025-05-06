from static_entity import StaticEntity

class DynamicEntity(StaticEntity):
    def __init__(self, x, y, width, height, color):
        super(DynamicEntity, self).__init__(x, y, width, height, color)

    def update(self):
        super(DynamicEntity, self).update()
        self.update_position_global()

    def update_position_global(self):
        self.x += self.d_x
        self.y += self.d_y
