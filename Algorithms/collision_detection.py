import pygame
from dynamic_entity import DynamicEntity

class CollisionDetection:
    def __init__(self, obj: DynamicEntity, layer: pygame.sprite.Group, d_xy: tuple[int, int]):
        self.obj = obj
        self.layer = layer
        self.d_x, self.d_y = d_xy
        self.clone = self.create_clone()

    def create_clone(self) -> DynamicEntity:
        clone = DynamicEntity()
        new_x = self.obj.rect.x + self.d_x
        new_y = self.obj.rect.y + self.d_y
        clone.set_position(new_x, new_y)
        clone.set_dimensions(self.obj.width, self.obj.height)
        clone.set_image(self.obj.color)
        clone.set_rect()
        return clone

    def check_collision(self) -> tuple[bool, int]:
        collisions = pygame.sprite.spritecollide(self.clone, self.layer, dokill=False)
        is_col = len(collisions) >= 1
        return is_col, len(collisions)

