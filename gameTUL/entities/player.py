import pygame
from gameTUL.entities.entity import Entity
from gameTUL.support import vector


class Player(Entity):
	def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
		super().__init__(pos, frames, groups, facing_direction)
		self.collision_sprites = collision_sprites
		self.noticed = False

	def input(self):
		keys = pygame.key.get_pressed()
		input_vector = vector()
		if keys[pygame.K_UP]:
			input_vector.y -= 1
		if keys[pygame.K_DOWN]:
			input_vector.y += 1
		if keys[pygame.K_LEFT]:
			input_vector.x -= 1
		if keys[pygame.K_RIGHT]:
			input_vector.x += 1
		self.direction = input_vector.normalize() if input_vector else input_vector

	def move(self, dt):
		self.rect.centerx += self.direction.x * self.speed * dt
		self.hitbox.centerx = self.rect.centerx
		self.collisions('horizontal')

		self.rect.centery += self.direction.y * self.speed * dt
		self.hitbox.centery = self.rect.centery
		self.collisions('vertical')

	def collisions(self, axis):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if axis == 'horizontal':
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
				else:
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery

	def update(self, dt):
		self.y_sort = self.rect.centery
		if not self.blocked:
			self.input()
			self.move(dt)
		self.animate(dt)