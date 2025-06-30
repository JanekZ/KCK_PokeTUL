from random import uniform
from gameTUL.settings import *
from gameTUL.timer import Timer


class MonsterSprite(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, monster, index, pos_index, entity, apply_attack, create_monster):
		# data
		self.index = index
		self.pos_index = pos_index
		self.entity = entity
		self.monster = monster
		self.frame_index, self.frames, self.state = 0, frames, 'idle'
		self.animation_speed = ANIMATION_SPEED + uniform(-1, 1)
		self.z = BATTLE_LAYERS['monster']
		self.highlight = False
		self.target_sprite = None
		self.current_attack = None
		self.apply_attack = apply_attack
		self.create_monster = create_monster

		# sprite setup
		super().__init__(groups)
		self.image = self.frames[self.state][self.frame_index]
		self.rect = self.image.get_frect(center = pos)

		# timers
		self.timers = {
			'remove highlight': Timer(300, func = lambda: self.set_highlight(False)),
			'kill': Timer(600, func = self.destroy)
		}

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		if self.state == 'attack' and self.frame_index >= len(self.frames['attack']):
			self.apply_attack(self.target_sprite, self.current_attack, self.monster.get_base_damage(self.current_attack))
			self.state = 'idle'

		self.adjusted_frame_index = int(self.frame_index % len(self.frames[self.state]))
		self.image = self.frames[self.state][self.adjusted_frame_index]

		if self.highlight:
			white_surf = pygame.mask.from_surface(self.image).to_surface()
			white_surf.set_colorkey('black')
			self.image = white_surf

	def set_highlight(self, value):
		self.highlight = value
		if value:
			self.timers['remove highlight'].activate()

	def activate_attack(self, target_sprite, attack):
		self.state = 'attack'
		self.frame_index = 0
		self.target_sprite = target_sprite
		self.current_attack = attack
		self.monster.reduce_energy(attack)

	def delayed_kill(self, new_monster):
		if not self.timers['kill'].active:
			self.next_monster_data = new_monster
			self.timers['kill'].activate()

	def destroy(self):
		if self.next_monster_data:
			self.create_monster(*self.next_monster_data)
		self.kill()

	def update(self, dt):
		for timer in self.timers.values():
			timer.update()
		self.animate(dt)
		self.monster.update(dt)