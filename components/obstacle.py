from random import randint
import pygame

fly_pic_1 = "graphics/Fly/Fly1.png"
fly_pic_2 = "graphics/Fly/Fly2.png" 
snail_pic_1 = "graphics/snail/snail1.png"
snail_pic_2 = "graphics/snail/snail2.png"

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load(fly_pic_1).convert_alpha()
			fly_2 = pygame.image.load(fly_pic_2).convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
		else:
			snail_1 = pygame.image.load(snail_pic_1).convert_alpha()
			snail_2 = pygame.image.load(snail_pic_2).convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()