import pygame
from pygame.math import Vector2 as vector
from gameTUL.settings import BATTLE_LAYERS, COLORS
from gameTUL.support import draw_bar


class MonsterStatsSprite(pygame.sprite.Sprite):
	def __init__(self, pos, monster_sprite, size, groups, font):
		super().__init__(groups)
		self.monster_sprite = monster_sprite
		self.image = pygame.Surface(size)
		self.rect = self.image.get_frect(midbottom = pos)
		self.font = font
		self.z = BATTLE_LAYERS['overlay']

	def update(self, _):
		self.image.fill(COLORS['white'])

		for index, (value, max_value) in enumerate(self.monster_sprite.monster.get_info()):
			color = (COLORS['red'], COLORS['blue'], COLORS['gray'])[index]
			if index < 2: # health and energy
				text_surf = self.font.render(f'{int(value)}/{max_value}', False, COLORS['black'])
				text_rect = text_surf.get_frect(topleft = (self.rect.width * 0.05,index * self.rect.height / 2))
				bar_rect = pygame.FRect(text_rect.bottomleft + vector(0,-2), (self.rect.width * 0.9, 4))

				self.image.blit(text_surf, text_rect)
				draw_bar(self.image, bar_rect, value, max_value, color, COLORS['black'], 2)
			else: # initiative
				init_rect = pygame.FRect((0, self.rect.height - 2), (self.rect.width, 2))
				draw_bar(self.image, init_rect, value, max_value, color, COLORS['white'], 0)

		if not self.monster_sprite.groups():
			self.kill()