from gameTUL.settings import *

class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_frect(topleft = pos)
		self.z = z
		self.y_sort = self.rect.centery
		self.hitbox = self.rect.copy()