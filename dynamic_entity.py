import pygame
import constants as c
from static_entity import StaticEntity


class DynamicEntity(StaticEntity):
    def __init__(self):
        super(DynamicEntity, self).__init__()
        self.d_x = 0
        self.d_y = 0

    def update(self):
        super(DynamicEntity, self).update()
        self.update_position_global()

    def update_position_global(self):
        self.x += self.d_x
        self.y += self.d_y
