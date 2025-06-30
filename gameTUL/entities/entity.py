from gameTUL.settings import *

class Entity(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, facing_direction):
		super().__init__(groups)
		self.z = WORLD_LAYERS['main']

		# graphics
		self.frame_index, self.frames = 0, frames
		self.facing_direction = facing_direction

		# movement
		self.direction = vector()
		self.speed = 250
		self.blocked = False

		# sprite setup
		self.image = self.frames[self.get_state()][self.frame_index]
		self.rect = self.image.get_frect(center = pos)
		self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)

		self.y_sort = self.rect.centery

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

	def get_state(self):
		moving = bool(self.direction)
		if moving:
			if self.direction.x != 0:
				self.facing_direction = 'right' if self.direction.x > 0 else 'left'
			if self.direction.y != 0:
				self.facing_direction = 'down' if self.direction.y > 0 else 'up'
		return f"{self.facing_direction}{'' if moving else '_idle'}"

	def change_facing_direction(self, target_pos):
		relation = vector(target_pos) - vector(self.rect.center)
		if abs(relation.y) < 30:
			self.facing_direction = 'right' if relation.x > 0 else 'left'
		else:
			self.facing_direction = 'down' if relation.y > 0 else 'up'

	def block(self):
		self.blocked = True
		self.direction = vector(0,0)

	def unblock(self):
		self.blocked = False