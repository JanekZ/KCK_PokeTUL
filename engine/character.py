import constants as c
import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, x = None, y= None):
        """
        CALLING SUPER INIT:
            Calling pygame.sprite.Sprite initializer for all the functionality of parent class.

        DIMENSION SET:
            Setting width, height, x, y and x and y-axis change.

        IMAGE SET:
            Setting up image, which is a surface with correct dimension filled with color.

        RECTANGLE SET:
            Setting up rect, which is a pygame.rect used as a bounds of the object.
        """
        super(Character, self).__init__()

        self.spriteFront = [
            pygame.image.load("engine/images/character_front/front_single1.png"),
            pygame.image.load("engine/images/character_front/front_single2.png"),
            pygame.image.load("engine/images/character_front/front_single3.png"),
            pygame.image.load("engine/images/character_front/front_single4.png")
        ]
        self.spriteBack = [
            pygame.image.load("engine/images/character_back/back_single1.png"),
            pygame.image.load("engine/images/character_back/back_single2.png"),
            pygame.image.load("engine/images/character_back/back_single3.png"),
            pygame.image.load("engine/images/character_back/back_single4.png")
        ]
        self.spriteLeft = [
            pygame.image.load("engine/images/character_side/side_single1.png"),
            pygame.image.load("engine/images/character_side/side_single2.png"),
            pygame.image.load("engine/images/character_side/side_single3.png"),
            pygame.image.load("engine/images/character_side/side_single4.png")
        ]

        self.spriteRight = [ pygame.transform.flip(sprite, True, False) for sprite in self.spriteLeft ]

        self.spriteDirections = {
            c.DOWN: self.spriteFront,
            c.UP: self.spriteBack,
            c.LEFT: self.spriteLeft,
            c.RIGHT: self.spriteRight
        }

        self.currentDirection = c.DOWN
        self.currentSprites = self.spriteDirections[c.DOWN]
        self.currentFrame = 0
        self.gameFramesCounter = 0
        self.frameCount = len(self.spriteBack)
        self.speedDivider = c.FPS / self.frameCount
        self.isStopped = True

        self.image = self.currentSprites[0]
        self.width, self.height = self.image.get_size()

        if x is None or y is None:
            self.x = c.CHARACTER_SCREEN_CENTER_WIDTH
            self.y = c.CHARACTER_SCREEN_CENTER_HEIGHT
        else:
            self.x = x
            self.y = y

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.d_x = 0
        self.d_y = 0


    def update(self) -> None:
        """
        RECTANGLE X AND Y CHANGE:
            Changing the rectangle x and y, by incrementing it with correct axis speed/change.
        """
        self.rect.x += self.d_x
        self.rect.y += self.d_y
        self.update_position()
        self.update_sprite()

    def update_position(self) -> None:
        """
        GLOBAL VALUE CHANGE:
             Changing the global x and y, by incrementing it with correct axis speed/change.
        """
        self.x += self.d_x
        self.y += self.d_y

    def update_sprite(self) -> None:
        """
        SPRITE ANIMATION MAINTENANCE
            Changing sprite images to create animation.
        """
        self.gameFramesCounter += 0 if self.isStopped else 1

        if self.gameFramesCounter == self.speedDivider:
            self.gameFramesCounter = 0
            self.currentFrame += 1
        if self.currentFrame == self.frameCount:
            self.currentFrame = 0

        self.image = self.currentSprites[ self.currentFrame ]


    def set_direction(self, direction: str) -> None:
        """

        """
        if direction == c.STOP:
            self.isStopped = True
            self.image = self.currentSprites[0]
        elif direction != self.currentDirection:
            self.isStopped = False
            self.currentSprites = self.spriteDirections[direction]
            self.currentDirection = direction
            self.image = self.currentSprites[0]
        else:
            self.isStopped = False

