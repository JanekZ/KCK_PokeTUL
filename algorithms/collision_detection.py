import pygame
from dynamic_entity import DynamicEntity

class CollisionDetection:
    def __init__(self, obj: DynamicEntity, d_xy: tuple[int, int]):
        self.obj = obj
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

    def check_collision(self, layer: pygame.sprite.Group, ) -> tuple[bool, int]:
        collisions = pygame.sprite.spritecollide(self.clone, layer, dokill=False)
        is_col = len(collisions) >= 1
        return is_col, len(collisions)

    def check_collision_with_portal(self, layer: pygame.sprite.Group, ) -> tuple:
        collisions = pygame.sprite.spritecollide(self.clone, layer, dokill=False)
        is_col = len(collisions) >= 1
        destination = collisions[0].destination if is_col else None
        return is_col, destination

    def check_out_of_bounds(self, layer: pygame.sprite.Group, ) -> bool:
        is_col, _ = self.check_collision(layer)
        boundaries = [i for i in layer]
        boundary = boundaries[0]

        if not is_col:
            return True
        if self.clone.rect.x < boundary.rect.x or self.clone.rect.x + self.clone.width > boundary.rect.x + boundary.width:
            return True
        if self.clone.rect.y < boundary.rect.y or self.clone.rect.y + self.clone.height > boundary.rect.y + boundary.height:
            return True

        return False

