from gameTUL.settings import BATTLE_LAYERS, ANIMATION_SPEED
from gameTUL.sprites.animated_sprite import AnimatedSprite


class AttackSprite(AnimatedSprite):
	def __init__(self, pos, frames, groups):
		super().__init__(pos, frames, groups, BATTLE_LAYERS['overlay'])
		self.rect.center = pos

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		if self.frame_index < len(self.frames):
			self.image = self.frames[int(self.frame_index)]
		else:
			self.kill()

	def update(self, dt):
		self.animate(dt)