from gameTUL.sprites.sprite import Sprite

class CollidableSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.inflate(0, -self.rect.height * 0.6)