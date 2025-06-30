from gameTUL.sprites.sprite import Sprite
from gameTUL.settings import *

class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
		self.frame_index, self.frames = 0, frames
		super().__init__(pos, frames[self.frame_index], groups, z)

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt):
		self.animate(dt)