from static_entity import StaticEntity

class DynamicEntity(StaticEntity):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        """
        CALLING SUPER INIT:
            Calling StaticEntity init to create proper object with all its properties.
        """
        super(DynamicEntity, self).__init__(x, y, width, height, color)

    def update(self) -> None:
        """
        CALLING SUPER UPDATE:
            Calling StaticEntity update() for proper update

        GLOBAL POSITION UPDATE:
            Calling function to update global position.
        """
        super(DynamicEntity, self).update()
        self.update_position_global()

    def update_position_global(self) -> None:
        """
        GLOBAL VALUE CHANGE:
             Changing the global x and y, by incrementing it with correct axis speed/change.
        """
        self.x += self.d_x
        self.y += self.d_y
