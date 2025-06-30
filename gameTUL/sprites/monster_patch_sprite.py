from gameTUL.settings import WORLD_LAYERS
from gameTUL.sprites.sprite import Sprite


class MonsterPatchSprite(Sprite):
	def __init__(self, pos, surf, groups, biome, monsters, level):
		self.biome = biome
		super().__init__(pos, surf, groups, WORLD_LAYERS['main' if biome != 'sand' else 'bg'])
		self.y_sort -= 40
		self.biome = biome
		self.monsters = monsters.split(',')
		self.level = level