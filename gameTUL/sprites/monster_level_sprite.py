import pygame

from gameTUL.settings import BATTLE_LAYERS, COLORS
from gameTUL.support import draw_bar


class MonsterLevelSprite(pygame.sprite.Sprite):
	def __init__(self, entity, pos, monster_sprite, groups, font):
		super().__init__(groups)
		self.monster_sprite = monster_sprite
		self.font = font
		self.z = BATTLE_LAYERS['name']

		self.image = pygame.Surface((60,26))
		self.rect = self.image.get_frect(topleft = pos) if entity == 'player' else self.image.get_frect(topright = pos)
		self.xp_rect = pygame.FRect(0,self.rect.height - 2,self.rect.width,2)

	def update(self, _):
		self.image.fill(COLORS['white'])

		text_surf = self.font.render(f'Lvl {self.monster_sprite.monster.level}', False, COLORS['black'])
		text_rect = text_surf.get_frect(center = (self.rect.width / 2, self.rect.height / 2))
		self.image.blit(text_surf, text_rect)

		draw_bar(self.image, self.xp_rect, self.monster_sprite.monster.xp, self.monster_sprite.monster.level_up, COLORS['black'], COLORS['white'], 0)

		if not self.monster_sprite.groups():
			self.kill()