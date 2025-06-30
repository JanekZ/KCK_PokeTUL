import pygame
from gameTUL.settings import COLORS, BATTLE_LAYERS


class MonsterNameSprite(pygame.sprite.Sprite):
	def __init__(self, pos, monster_sprite, groups, font):
		super().__init__(groups)
		self.monster_sprite = monster_sprite
		self.z = BATTLE_LAYERS['name']

		text_surf = font.render(monster_sprite.monster.name, False, COLORS['black'])
		padding = 10

		self.image = pygame.Surface((text_surf.get_width() + 2 * padding, text_surf.get_height() + 2 * padding))
		self.image.fill(COLORS['white'])
		self.image.blit(text_surf, (padding, padding))
		self.rect = self.image.get_frect(midtop = pos)

	def update(self, _):
		if not self.monster_sprite.groups():
			self.kill()