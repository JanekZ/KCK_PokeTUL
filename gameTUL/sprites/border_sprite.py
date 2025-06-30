from gameTUL.sprites.sprite import Sprite

class BorderSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy()