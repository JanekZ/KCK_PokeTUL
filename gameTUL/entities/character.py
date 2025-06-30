from random import choice
from gameTUL.entities.entity import Entity
from gameTUL.monster import Monster
from gameTUL.support import check_connections
from gameTUL.timer import Timer
from gameTUL.support import vector


class Character(Entity):
	def __init__(self, pos, frames, groups, facing_direction, character_data, player, create_dialog, collision_sprites, radius, nurse, notice_sound):
		super().__init__(pos, frames, groups, facing_direction)
		self.character_data = character_data
		self.player = player
		self.create_dialog = create_dialog
		self.collision_rects = [sprite.rect for sprite in collision_sprites if sprite is not self]
		self.nurse = nurse
		self.monsters = {i: Monster(name, lvl) for i, (name, lvl) in character_data['monsters'].items()} if 'monsters' in character_data else None

		# movement
		self.has_moved = False
		self.can_rotate = True
		self.has_noticed = False
		self.radius = int(radius)
		self.view_directions = character_data['directions']

		self.timers = {
			'look around': Timer(1500, autostart = True, repeat = True, func = self.random_view_direction),
			'notice': Timer(500, func = self.start_move)
		}
		self.notice_sound = notice_sound

	def random_view_direction(self):
		if self.can_rotate:
			self.facing_direction = choice(self.view_directions)

	def get_dialog(self):
		return self.character_data['dialog'][f"{'defeated' if self.character_data['defeated'] else 'default'}"]

	def raycast(self):
		if check_connections(self.radius, self, self.player) and self.has_los() and not self.has_moved and not self.has_noticed:
			self.player.block()
			self.player.change_facing_direction(self.rect.center)
			self.timers['notice'].activate()
			self.can_rotate = False
			self.has_noticed = True
			self.player.noticed = True
			self.notice_sound.play()

	def has_los(self):
		if vector(self.rect.center).distance_to(self.player.rect.center) < self.radius:
			collisions = [bool(rect.clipline(self.rect.center, self.player.rect.center)) for rect in self.collision_rects]
			return not any(collisions)

	def start_move(self):
		relation = (vector(self.player.rect.center) - vector(self.rect.center)).normalize()
		self.direction = vector(round(relation.x), round(relation.y))

	def move(self, dt):
		if not self.has_moved and self.direction:
			if not self.hitbox.inflate(10,10).colliderect(self.player.hitbox):
				self.rect.center += self.direction * self.speed * dt
				self.hitbox.center = self.rect.center
			else:
				self.direction = vector()
				self.has_moved = True
				self.create_dialog(self)
				self.player.noticed = False

	def update(self, dt):
		for timer in self.timers.values():
			timer.update()

		self.animate(dt)
		if self.character_data['look_around']:
			self.raycast()
			self.move(dt)