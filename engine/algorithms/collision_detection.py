import pygame
from dynamic_entity import DynamicEntity

class CollisionDetection:
    def __init__(self, obj: DynamicEntity, d_xy: tuple[int, int]):
        """
        SETTING UP:
            Creation of class properties using parameters.
        CLONE:
            Clone creation with offset of d_xy, used to check for collisions.

        :param obj: Object that will be used to check for collisions.
        :param d_xy: Change in x and y-axis.
        """
        self.obj = obj
        self.d_x, self.d_y = d_xy
        self.clone = self.create_clone()

    def create_clone(self) -> DynamicEntity:
        """
        CREATION:
            New dynamic entity object is created with new x and y values with offset.

        :return: Clone of the object with offset.
        """
        new_x = self.obj.rect.x + self.d_x
        new_y = self.obj.rect.y + self.d_y
        clone = DynamicEntity(new_x, new_y, self.obj.width, self.obj.height, self.obj.color)
        return clone

    def check_collision(self, layer: pygame.sprite.Group, ) -> tuple[bool, int]:
        """
        COLLISION CHECK:
            Pygame built-in function checks if clone of character is colliding with any object from given layer.

        :param layer: Layer of objects that character can collide with.
        :return: Tuple with boolean value representing collision and number of elements that character collided with.
        """
        collisions = pygame.sprite.spritecollide(self.clone, layer, dokill=False)
        is_col = len(collisions) >= 1
        return is_col, len(collisions)

    def check_collision_with_portal(self, layer: pygame.sprite.Group, ) -> tuple:
        """
        COLLISION CHECK:
            Pygame built-in function checks if clone of character is colliding with any portal object from given layer.

        :param layer: Layer of objects that character can collide with.
        :return: Tuple with boolean value representing collision and destination of given portal.
        """
        collisions = pygame.sprite.spritecollide(self.clone, layer, dokill=False)
        is_col = len(collisions) >= 1
        destination = collisions[0].destination if is_col else None
        return is_col, destination

    def check_out_of_bounds(self, layer: pygame.sprite.Group, ) -> bool:
        """
        COLLISION CHECK:
            Manual checking if clone of character is inside given boundary.

        :param layer: Layer of bounding objects.
        :return: Tuple with boolean value representing if character is out of bounds.
        """
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

